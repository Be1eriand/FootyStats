# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from models import *
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import logging
import sys, traceback

from sqlalchemy.sql.expression import and_

logger = logging.getLogger('FootyWire')
logger.setLevel(logging.INFO)

ifh = logging.FileHandler('Pipeline.log')
ifh.setLevel(logging.INFO)
logger.addHandler(ifh)


class FootystatsPipeline:

    def __init__(self, sql_db):
        self.sql_db = sql_db

        logger.info('Initialising db with %s' % self.sql_db)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(sql_db= 'sqlite:///:memory:' #'sqlite:///.\\Database\\FootyStats.sqlite'  #.\Database
                   )

    def open_spider(self, spider):

        logger.info('Open Spider')

        self.engine = create_engine(self.sql_db)
        connection = self.engine.connect()

        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)

        self.DBSession = sessionmaker(bind=self.engine)

        self.session = self.DBSession(bind=connection)

    def close_spider(self, spider):

        self.session.close()

    def process_item(self, item, spider):

        try :
            self.processMatchItem(item)
            logger.info('Footywire ID (%d) has been processed' % (item['fwID']))
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()

            logger.error('Unable to process Footywire ID (%d)' %
                         (item['fwID']))
            logger.error('Match Item:')
            logger.error(item)
            logger.error('Exception is :')
            logger.error(e)
            logger.error('Traceback is:')
            logger.error(traceback.print_exception(exc_type,
                                                    exc_value,
                                                    exc_traceback,
                                                    limit=10))

        return item

    def processPlayer(self, playerInfo):

        try:
            FirstName, LastName = playerInfo['name'].split(' ')
        except ValueError: # if they have a split surname ie De Gooey, Van Berlo, Van der Brink
            Name = {}
            Name = playerInfo['name'].split(' ')
            FirstName = Name[0]
            Name = Name[1:len(Name)+1]
            LastName = ' '.join(Name)

        player = Player(First_Name=FirstName,
                        Last_Name=LastName,
                        Link_Name=playerInfo['link'])

        qText = 'Link_Name==\'{Link}\''.format(Link=playerInfo['link'])

        result = self.processQuery(player, qText)

        return result.id

    def processGround(self, ground):

        if ground == '': #return -1 as blank ground should not be entered into the database. probably missing in the scrape
            return -1

        grnd = Ground(Name=ground)

        qText = 'Name==\"{name}\"'.format(name=ground) # Double quotes matter - Bloody Cazaly's stadium

        result = self.processQuery(grnd, qText)

        return result.id

    def processClub(self, clubInfo):

        if clubInfo == '':  #return -1 as blank Club should not be entered into the database. probably missing in the scrape
            return -1

        club = Club(Club_Name=clubInfo)

        qText = 'Club_Name==\'{ClubName}\''.format(ClubName=clubInfo)

        result = self.processQuery(club, qText)

        return result.id

    def processCoach(self, coachInfo):

        if (coachInfo == '') or (coachInfo == None):  #return -1 as blank Coach Name should not be entered into the database. probably missing in the scrape
            return -1

        FirstName, LastName = coachInfo.split(' ')

        coach = Coach(First_Name=FirstName, Last_Name=LastName)

        qText = 'First_Name==\"{First_Name}\" and Last_Name==\"{Last_Name}\"'.format(First_Name=FirstName, Last_Name=LastName) #Double Quotes matter

        result = self.processQuery(coach, qText)

        return result.id

    def processQuery(self, object, queryText):

        query = self.session.query(type(object)).filter(text(queryText)).all()

        if len(query) == 0:
            self.session.add(object)
            self.session.commit()
        elif len(query) != 1:  #Should never return more than one result
            raise ValueError('Query of {classType} has more than one'.format(classType=type(object))) #Is this the best way?
        else:
            object = query[0]

        return object


    def insertItemintoDB(self, object, item):

        for Key, Value in item.items():

            setattr(object, Key, Value)

        self.session.add(object)
        self.session.commit()

        return object

    def processScores(self, scores):

        score = Match_Scores()

        score = self.insertItemintoDB(score, scores)

        return score.id

    def processBasicStats(self, bStats):

        stats = Basic_Stats()

        stats = self.insertItemintoDB(stats, bStats)

        return stats.id

    def processAdvancedStats(self, aStats):

        stats = Advance_Stats()

        stats = self.insertItemintoDB(stats, aStats)

        return stats.id

    def processTeam(self, TeamName, TeamCoach, TeamStats):

        coachID = self.processCoach(TeamCoach)
        clubID = self.processClub(TeamName)

        team = Team(ClubID=clubID, CoachID=coachID)

        for key, value in TeamStats.items():
            setattr(team, key, value)

        self.session.add(team)
        self.session.commit()

        return team.id

    def processFixture(self, teamInfo, fixtureInfo):

        fixture = Fixture()

        for key, value in fixtureInfo.items():
            setattr(fixture, key, value)

        for key, value in teamInfo.items():
            setattr(fixture, key, value)

        self.session.add(fixture)
        self.session.commit()

        return fixture

    def processTeamList(self, teamID, playerID, bStatsID, aStatsID):

        teamList = Team_List(
                            PlayerID = playerID,
                            TeamID = teamID,
                            BasicStats = bStatsID,
                            AdvancedStats = aStatsID
                            )

        if aStatsID is not None:
            qText = 'PlayerID=%d and TeamID=%d and BasicStats=%d and AdvancedStats=%s' % (
                playerID, teamID, bStatsID, aStatsID)
        else:
            qText = 'PlayerID=%d and TeamID=%d and BasicStats=%d' % (
                playerID, teamID, bStatsID)

        teamList = self.processQuery(teamList, qText)

        return teamList

    def processClubList(self, clubID, playerID):

        clubList = Club_List(PlayerID=playerID, ClubID=clubID)

        qText = 'PlayerID=%d and ClubID=%d' % (playerID, clubID)
        clubList = self.processQuery(clubList, qText)

        return clubList

    def processMatchItem(self, item):

        ground = item['Ground']
        self.processGround(ground)

        #Home Team
        HomeScoreID = self.processScores(item['HomeTeamScore'])
        HomeClubID = self.processClub(item['HomeTeamName'])
        HomeCoachID = self.processCoach(item['HomeTeamCoach'])
        HomeTeamID = self.processTeam(item['HomeTeamName'],
                                        item['HomeTeamCoach'],
                                        item['HomeTeamStats'])

        #away Team
        AwayScoreID = self.processScores(item['AwayTeamScore'])
        AwayClubID = self.processClub(item['AwayTeamName'])
        AwayCoachID = self.processCoach(item['AwayTeamCoach'])
        AwayTeamID = self.processTeam(item['AwayTeamName'],
                                        item['AwayTeamCoach'],
                                        item['AwayTeamStats'])

        #Home Team Players
        player_stats = item['HomeTeamPlayers_Stats']
        if 'HomeTeamPlayers_AdvStats' in item:
            player_adv_stats = item['HomeTeamPlayers_AdvStats']
        else:
            player_adv_stats = None

        self.processPlayerStats(HomeTeamID, HomeClubID, player_stats,
                                player_adv_stats)

        #Away Team Players
        player_stats = item['AwayTeamPlayers_Stats']
        if 'AwayTeamPlayers_AdvStats' in item:
            player_adv_stats = item['AwayTeamPlayers_AdvStats']
        else:
            player_adv_stats = None

        self.processPlayerStats(AwayTeamID, AwayClubID, player_stats,
                                player_adv_stats)


    def processPlayerStats(self, teamID, clubID, playerStats, playerStatsAdv):

        for stat in playerStats:

            playerID = self.processPlayer(stat)
            playerStatID = self.processBasicStats(stat)
            playerStatsAdvID = None

            TL = self.processTeamList(teamID, playerID, playerStatID, playerStatsAdvID)
            CL = self.processClubList(clubID, playerID)

            if (TL is None) or (CL is None):
                logger.error('Unable to process Club List or Team List')
                return False


            if playerStatsAdv is not None:
                for stat in playerStatsAdv:
                    playerID = self.processPlayer(stat)
                    playerStatsAdvID = self.processAdvancedStats(stat)

                    self.session.query(Team_List).filter(
                        and_(Team_List.TeamID == teamID,
                             Team_List.PlayerID == playerID)).update(
                                 {'AdvancedStats': playerStatsAdvID},
                                 synchronize_session="fetch")

        return True
