from FootyStats.spiders import FootywireSpider
from pipelines import FootystatsPipeline
from models import *
import pytest
from os import path, remove
from datetime import datetime, date
import time


@pytest.fixture
def FwS():
    return FootywireSpider()


@pytest.fixture
def Pipe():
    return FootystatsPipeline('sqlite:///FootyStats.sqlite')


if path.exists('./FootyStats.sqlite'):
    remove('./FootyStats.sqlite')


def test_init():

    Pipe = FootystatsPipeline('sqlite:///FootyStats.sqlite')

    assert isinstance(Pipe, FootystatsPipeline)
    assert Pipe.sql_db == 'sqlite:///FootyStats.sqlite'


def test_openSpider(Pipe, FwS):

    Pipe.open_spider(FwS)

    assert Pipe.engine is not None
    assert Pipe.DBSession is not None
    assert Pipe.session is not None


def test_processQuery(Pipe, FwS):

    Pipe.open_spider(FwS)

    coach = Coach(First_Name='Simon', Last_Name='Goodwin')
    qText = 'First_Name==\'Simon\' and Last_Name==\'Goodwin\''

    result = Pipe.processQuery(coach, qText)

    assert result is not None
    assert result.id != 0
    assert (result.First_Name == 'Simon') and (result.Last_Name == 'Goodwin')


def test_processPlayer(Pipe, FwS):

    Pipe.open_spider(FwS)

    info = {
        'B': 1.0,
        'CG': 10.0,
        'CL': 3.0,
        'D': 30.0,
        'FA': 4.0,
        'FF': 4.0,
        'G': 0.0,
        'GA': 1.0,
        'HB': 14.0,
        'HO': 0.0,
        'I50': 4.0,
        'K': 16.0,
        'M': 5.0,
        'R50': 0.0,
        'T': 8.0,
        'link': 'pp-geelong-cats--joel-selwood',
        'name': 'Joel Selwood'
    }

    result = Pipe.processPlayer(info)

    assert result == 1


def test_processPlayerSplitSurname(Pipe, FwS):

    Pipe.open_spider(FwS)

    info = {
        'AFLFantasy': 90,
        'Behinds': 3,
        'Clangers': 2,
        'Clearances': 0,
        'Disposals': 16,
        'Frees_Against': 1,
        'Frees_For': 1,
        'Goal_Assists': 2,
        'Goals': 4,
        'Handballs': 5,
        'Hitouts': 0,
        'Inside_50': 2,
        'Kicks': 11,
        'Marks': 6,
        'Rebound_50': 0,
        'SuperCoach': 99,
        'Tackles': 1,
        'link': 'pp-collingwood-magpies--jordan-de-goey',
        'name': 'Jordan De Goey'
    }

    result = Pipe.processPlayer(info)

    assert result > 0


def test_processPlayer_duplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    info = {
        'B': 1.0,
        'CG': 10.0,
        'CL': 3.0,
        'D': 30.0,
        'FA': 4.0,
        'FF': 4.0,
        'G': 0.0,
        'GA': 1.0,
        'HB': 14.0,
        'HO': 0.0,
        'I50': 4.0,
        'K': 16.0,
        'M': 5.0,
        'R50': 0.0,
        'T': 8.0,
        'link': 'pp-geelong-cats--joel-selwood',
        'name': 'Joel Selwood'
    }

    result1 = Pipe.processPlayer(info)
    result2 = Pipe.processPlayer(info)

    assert result2 == result1

def test_processGround(Pipe, FwS):

    Pipe.open_spider(FwS)

    ground = 'MCG'

    result = Pipe.processGround(ground)

    assert result == 1


def test_processGroundDuplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    ground = 'MCG'

    result1 = Pipe.processGround(ground)
    result2 = Pipe.processGround(ground)

    assert result2 == result1


def test_processGroundNoGround(Pipe, FwS):

    Pipe.open_spider(FwS)

    ground = ''

    result = Pipe.processGround(ground)

    assert result == -1


def test_processGroundEscaped(Pipe, FwS):

    Pipe.open_spider(FwS)

    ground = "Cazaly's Stadium"

    result = Pipe.processGround(ground)

    assert result > 0


def test_processClub(Pipe, FwS):

    Pipe.open_spider(FwS)

    club = 'Melbourne'

    result = Pipe.processClub(club)

    assert result == 1


def test_processClub_duplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    club = 'North Melbourne'

    result1 = Pipe.processClub(club)
    result2 = Pipe.processClub(club)

    assert result2 == result1


def test_processCoach(Pipe, FwS):

    Pipe.open_spider(FwS)

    coach = 'Simon Goodwin'

    result = Pipe.processCoach(coach)

    assert result == 1

def test_processCoachEscape(Pipe, FwS):

    Pipe.open_spider(FwS)

    coach = "Peter O'Donohue"

    result = Pipe.processCoach(coach)

    assert result == 1


def test_processCoach_duplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    coach = 'Simon Goodwin'

    result1 = Pipe.processCoach(coach)
    result2 = Pipe.processCoach(coach)

    assert result2 == result1


def test_processCoachNoCoachInfo(Pipe, FwS):

    Pipe.open_spider(FwS)

    coach = None

    result = Pipe.processCoach(coach)

    assert result == -1


def test_processScores(Pipe, FwS):

    Pipe.open_spider(FwS)

    scores = {
        'FinalScore': '84',
        'Q1': '2.1',
        'Q2': '3.5',
        'Q3': '8.7',
        'Q4': '12.12'
    }

    result = Pipe.processScores(scores)

    assert result == 1


def test_insertItemintoDB(Pipe, FwS):

    Pipe.open_spider(FwS)

    stats = {
        'AFLFantasy': 120,
        'Behinds': 0.0,
        'Clangers': 0.0,
        'Clearances': 1.0,
        'Disposals': 4.0,
        'Frees_Against': 0.0,
        'Frees_For': 1.0,
        'Goals': 0.0,
        'Goal_Assists': 0.0,
        'Handballs': 3.0,
        'Hitouts': 0.0,
        'Inside_50': 1.0,
        'Kicks': 1.0,
        'Marks': 1.0,
        'Rebound_50': 0.0,
        'SuperCoach': 102,
        'Tackles': 1.0,
        'link': 'pp-fremantle-dockers--adam-cerra',
        'name': 'Adam Cerra'
    }

    stat = Basic_Stats()
    result = Pipe.insertItemintoDB(stat, stats)

    assert result is not None
    assert result.id > 0

def test_processBasicStatsShortened(Pipe, FwS):

    Pipe.open_spider(FwS)

    stats = [{
        'AFLFantasy': 86.0,
        'Behinds': 0.0,
        'Disposals': 22.0,
        'Frees_Against': 1.0,
        'Frees_For': 0.0,
        'Goals': 1.0,
        'Goals_Assists': 0.0,
        'Handballs': 11.0,
        'Hitouts': 1.0,
        'Inside_50': 4.0,
        'Kicks': 11.0,
        'Marks': 5.0,
        'SuperCoach': 90.0,
        'Tackles': 3.0,
        'link': 'pp-adelaide-crows--tyson-edwards',
        'name': 'Tyson Edwards'
    }]

    result = Pipe.processBasicStats(stats[0])

    assert result > 0


def test_processBasicStats(Pipe, FwS):

    Pipe.open_spider(FwS)

    stats = [{
        'AFLFantasy': 120,
        'Behinds': 0.0,
        'Clangers': 0.0,
        'Clearances': 1.0,
        'Disposals': 4.0,
        'Frees_Against': 0.0,
        'Frees_For': 1.0,
        'Goals': 0.0,
        'Goal_Assists': 0.0,
        'Handballs': 3.0,
        'Hitouts': 0.0,
        'Inside_50': 1.0,
        'Kicks': 1.0,
        'Marks': 1.0,
        'Rebound_50': 0.0,
        'SuperCoach': 102,
        'Tackles': 1.0,
        'link': 'pp-fremantle-dockers--adam-cerra',
        'name': 'Adam Cerra'
    }]

    result = Pipe.processBasicStats(stats[0])

    assert result > 0


def test_processAdvanceStats(Pipe, FwS):

    Pipe.open_spider(FwS)

    stats = [{
        'Bounces': 0,
        'Centre_Clearances': 5,
        'Contested_Marks': 0,
        'Contested_Possessions': 13,
        'Disposal_Efficiency': 72.7,
        'Effective_Disposals': 24,
        'Goal_Assists': 2,
        'Intercepts': 2,
        'Marks_Inside_50': 1,
        'Metres_Gained': 436,
        'One_Percenters': 0,
        'Score_Invlovement': 9,
        'Stoppage_Clearances': 2,
        'Tackles_inside_50': 0,
        'Time_on_ground': 78,
        'Turnovers': 4,
        'Uncontested_Possession': 20,
        'link': 'pp-western-bulldogs--jackson-macrae',
        'name': 'J Macrae'
    }]

    result = Pipe.processAdvancedStats(stats[0])

    assert result > 0

def test_processFixture(Pipe, FwS):

    Pipe.open_spider(FwS)

    fixtureInfo = {
        'Attendance': 20986,
        'Ground': 'Marvel Stadium',
        'MatchDate': datetime.strptime('03/04/2021', '%d/%m/%Y').date(),
        'MatchTime': datetime.strptime('4:35 PM',
                                       '%H:%M %p'),
        'Round': 'Round 3',
        'fwID': 10349
    }

    teamInfo = {
        'HomeTeamID' : 1,
        'AwayTeamID' : 2,
        'HomeScoresID' : 1,
        'AwayScoresID'  : 2
    }

    result = Pipe.processFixture(teamInfo, fixtureInfo)

    assert result.fwID == fixtureInfo['fwID']
    assert result.HomeTeamID == teamInfo['HomeTeamID']
    assert result.AwayTeamID == teamInfo['AwayTeamID']
    assert result.HomeScoresID == teamInfo['HomeScoresID']
    assert result.AwayScoresID == teamInfo['AwayScoresID']
    assert result.Ground == fixtureInfo['Ground']
    assert result.MatchDate == fixtureInfo['MatchDate']
    assert result.MatchTime == fixtureInfo['MatchTime']
    assert result.Round == fixtureInfo['Round']
    assert result.Attendance == fixtureInfo['Attendance']


def test_processTeam(Pipe, FwS):

    Pipe.open_spider(FwS)

    TeamStats = {
        'BehindsKicked': 10,
        'Clangers': 54,
        'Clearances': 33,
        'Conversion': 66.7,
        'Disposals': 443,
        'DisposalsPerGoal': 20.14,
        'DispsPerScoringShot': 13.42,
        'FreesAgainst': 18,
        'FreesFor': 22,
        'GoalAssists': 19,
        'GoalsKicked': 22,
        'Handballs': 188,
        'Hitouts': 22,
        'In50sGoal': 39.3,
        'In50sPerScoringShot': 1.70,
        'In50sScore': 57.1,
        'Inside50s': 56,
        'Inside50sPerGoal': 2.55,
        'Kicks': 255,
        'KicktoHandballRatio': 1.36,
        'Marks': 136,
        'Rebound50s': 44,
        'RushedBehinds': 1,
        'ScoringShots': 33,
        'Tackles': 54
                   }
    TeamCoach = 'John Worsfold'
    TeamName = 'Essendon'

    result = Pipe.processTeam(TeamName, TeamCoach, TeamStats)

    assert result > 0


def test_processTeamList(Pipe, FwS):

    Pipe.open_spider(FwS)

    teamID = 1
    playerID = 1
    bStatsID = 1
    aStatsID = 1

    result = Pipe.processTeamList(teamID, playerID, bStatsID, aStatsID)

    assert result is not None


def test_processTeamListDuplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    teamID = 1
    playerID = 1
    bStatsID = 1
    aStatsID = 1

    result1 = Pipe.processTeamList(teamID, playerID, bStatsID, aStatsID)
    result2 = Pipe.processTeamList(teamID, playerID, bStatsID, aStatsID)

    assert result1 is not None
    assert result2 is not None
    assert result1 == result2


def test_processTeamListNoAdvStats(Pipe, FwS):

    Pipe.open_spider(FwS)

    teamID = 1
    playerID = 1
    bStatsID = 1
    aStatsID = None

    result = Pipe.processTeamList(teamID, playerID, bStatsID, aStatsID)

    assert result is not None


def test_processClubList(Pipe, FwS):

    Pipe.open_spider(FwS)

    clubID = 1
    playerID = 1

    result = Pipe.processClubList(clubID, playerID)

    assert result is not None


def test_processClubListDuplicate(Pipe, FwS):

    Pipe.open_spider(FwS)

    clubID = 1
    playerID = 1

    result1 = Pipe.processClubList(clubID, playerID)
    result2 = Pipe.processClubList(clubID, playerID)

    assert result1 is not None
    assert result2 is not None
    assert result1 == result2