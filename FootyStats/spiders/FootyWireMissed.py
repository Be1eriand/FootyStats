import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from FootyStats.items import FootyMatchItem
import re
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError

StatKeys = {
    'K':'Kicks',
    'HB':'Handballs',
    'D':'Disposals',
    'M':'Marks',
    'G':'Goals',
    'B':'Behinds',
    'T':'Tackles',
    'HO':'Hitouts',
    'I50':'Inside_50',
    'CL':'Clearances',
    'CG':'Clangers',
    'R50':'Rebound_50',
    'FF':'Frees_For',
    'FA':'Frees_Against',
    'AF':'AFLFantasy',
    'SC':'SuperCoach',
    '1%': 'One_Percenters',
    'BO': 'Bounces',
    'CCL': 'Centre_Clearances',
    'CM': 'Contested_Marks',
    'CP': 'Contested_Possessions',
    'DE%': 'Disposal_Efficiency',
    'ED': 'Effective_Disposals',
    'GA': 'Goal_Assists',
    'ITC': 'Intercepts',
    'MG': 'Metres_Gained',
    'MI5': 'Marks_Inside_50',
    'SCL': 'Stoppage_Clearances',
    'SI': 'Score_Invlovement',
    'T5': 'Tackles_inside_50',
    'TO': 'Turnovers',
    'TOG%': 'Time_on_ground',
    'UP': 'Uncontested_Possession'
}

def load_requests():

    footy_list = []

    try:
        file = open('missed.txt', 'r')

        lines = file.readlines()

        for line in lines:
            split = {}
            split = line.split(': ')
            footy_list.append(split[1].strip())

    except:
        footy_list = None

    return footy_list


class FootywireSingle(Spider):
    name = 'FWMissed'
    allowed_domains = ['footywire.com']
    base_url = 'https://www.footywire.com/afl/footy/'


    def start_requests(self):

        missed = load_requests()

        if missed == None:
            print('Missed it')

        urls =[]
        for item in missed:
            url = self.base_url + 'ft_match_statistics?' + item
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseFixture)


    def parseFixture(self, response):

        MatchItem = FootyMatchItem(
            fwID=0,
            MatchDate='',
            MatchTime = '',
            Ground='',
            Round='',
            Attendance = 0,
            HomeTeamName='',
            HomeTeamCoach='',
            HomeTeamScore=None,
            HomeTeamStats=None,
            HomeTeamPlayers_Stats=None,
            AwayTeamName='',
            AwayTeamCoach='',
            AwayTeamScore=None,
            AwayTeamStats= None,
            AwayTeamPlayers_Stats=None,
        )

        MatchInfoTbl, ScoresTbl, HomeTeamTbl, AwayTeamTbl, TeamStatsTbl = self.getMatchTables(response)

        MatchItem['fwID'] = self.getFootyWireID(response.url)
        MatchItem['MatchDate'], MatchItem['MatchTime'], MatchItem['Ground'], MatchItem['Round'], MatchItem['Attendance'] = self.getMatchInfo(MatchInfoTbl)
        MatchItem['HomeTeamScore'], MatchItem['AwayTeamScore'], MatchItem['HomeTeamName'], MatchItem['AwayTeamName'] = self.processScores(ScoresTbl)
        MatchItem['HomeTeamCoach'], MatchItem['HomeTeamPlayers_Stats'] = self.processTeam(HomeTeamTbl)
        MatchItem['AwayTeamCoach'], MatchItem['AwayTeamPlayers_Stats'] = self.processTeam(AwayTeamTbl)
        MatchItem['HomeTeamStats'], MatchItem['AwayTeamStats'] = self.processTeamStats(TeamStatsTbl)

        notice = Selector(response=response).css('.notice').get() #does the page have the advance stats notice

        if notice is None:
            yield MatchItem
        else:
            advancedStatsUrl = Selector(text=notice).xpath('//@href').get()
            request = scrapy.Request(response.urljoin(advancedStatsUrl), self.parseAdvanceStats, cb_kwargs=dict(item=MatchItem))
            yield request

    def parseAdvanceStats(self, response, item):

        pageTbl = Selector(response=response).xpath('//*[@id="frametable2008"]//tr[3]//table')[2]
        HomeTeamTbl = Selector(text=pageTbl.get()).xpath('//table')[5].get()
        AwayTeamTbl = Selector(text=pageTbl.get()).xpath('//table')[9].get()

        item['HomeTeamCoach'], item['HomeTeamPlayers_AdvStats'] = self.processTeam(HomeTeamTbl)
        item['AwayTeamCoach'], item['AwayTeamPlayers_AdvStats'] = self.processTeam(AwayTeamTbl)

        return item

    def getMatchTables(self, response):

        MatchInfoTbl = ''
        HomeTeamTbl = ''
        AwayTeamTbl = ''
        TeamStatsTbl = ''
        ScoresTbl =''

        pageTbl = Selector(response=response).xpath('//*[@id="frametable2008"]//tr[3]//table')[2]
        MatchInfoTbl = pageTbl.css('.lnormtop').xpath('./table/tr/td[1]/table').get()
        ScoresTbl = pageTbl.css('.lnormtop').xpath('./table/tr/td[3]/table').get()
        soup = BeautifulSoup(pageTbl.get(), 'lxml') #Stuff FootyWire and it's ever changing formatting
        team_tables = soup.find_all('td', class_='tbtitle')
        HomeTeamTbl = repr(team_tables[0].find_parent('table'))
        AwayTeamTbl = repr(team_tables[1].find_parent('table'))
        TeamStatsTbl = repr(team_tables[2].find_parent('table'))

        return MatchInfoTbl, ScoresTbl, HomeTeamTbl, AwayTeamTbl, TeamStatsTbl

    def getFootyWireID(self, url):

        return int(re.sub('\D', '', url.split('=')[1]))

    def getMatchInfo(self, table):

        Soup = BeautifulSoup(table, 'lxml')

        td_list = Soup.find_all('td')

        ground = ''
        rnd = ''
        attendance = 0
        dt = ''

        for row in td_list:

            if row.string is not None:
                if (re.search('Round', row.string) is not None) or (re.search('Final', row.string) is not None):

                    try:
                        row_items = row.string.strip('\n').split(',')
                        rnd = row_items[0].strip(' ')
                        row_items = row_items[1:len(row_items)+1]
                        dt = ','.join(row_items)

                        parse(dt)

                    except ParserError:

                        row_items = row.string.strip('\n').split(',')
                        #We're going to assume Round is at the beginning
                        rnd = row_items[0].strip(' ')

                        #match gound
                        ground = row_items[1].strip(' ')

                        if len(row_items) == 3:
                            attendance = int(re.sub('\D', '', row_items[2]))
                else:
                    try:
                        parse(row.string)

                        dt = row.string

                    except ParserError:
                        pass

        matchDay, matchDate, matchTime = self.processDate(dt)

        return matchDate, matchTime, ground, rnd, attendance

    def processDate(self, dt):

        d_list = {}
        d_list = dt.split(',')

        day = d_list[0]

        split_list = {}
        split_list = d_list[1].strip(' ').split(' ')
        split_list[0] = re.sub('\D', '', split_list[0])

        d_list[1] = ' '.join(split_list)

        d = datetime.strptime(d_list[1], '%d %B %Y')
        if len(d_list) == 3:
            sp_t = {}
            sp_t = d_list[2].strip(' ').split(' ')
            if len(sp_t) == 3:
                sp_t = sp_t[0:2]
            t = ' '.join(sp_t)
        else:
            t =''

        return day, d.strftime('%d/%m/%Y'), t

    def processScores(self, table):

        rows = Selector(text=table).xpath('//tr')
        HSc = Selector(text=rows[1].get()).xpath('//td/text()').getall()  #Get the Home scores
        ASc = Selector(text=rows[2].get()).xpath('//td/text()').getall()  #Get the Away scores

        HomeTeam = Selector(text=rows[1].get()).xpath('//a/text()').get()  #Get the Home Team Name
        AwayTeam = Selector(text=rows[2].get()).xpath('//a/text()').get()  #Get the Away Team Name

        HomeScores = {}
        AwayScores = {}

        quarters = ('Q1', 'Q2', 'Q3', 'Q4', 'FinalScore')

        for (Q, H, A) in zip(quarters, HSc, ASc):
            HomeScores[Q] = H.strip(' \n')
            AwayScores[Q] = A.strip(' \n')

        return HomeScores, AwayScores, HomeTeam, AwayTeam

    def processTeam(self, table):

        cText = Selector(text=table).xpath('//table//td/a').get() #2019 hack - No coach info "What is it with FootyWire?"
        coach = Selector(text=cText).xpath('//text()').get()

        try:

            player_table = Selector(text=table).xpath('//table')[2].get()

        except IndexError: # Infuriating that the formatting keeps changing

            player_table = Selector(text=table).xpath('//table').get()

        player_row = Selector(text=player_table).xpath('//tr').getall()

        stats_row = Selector(text=player_row[0].replace('\n', '')).xpath('//text()').getall()

        if stats_row[0] != 'Player': #Wish they wouldn't change the formatting

            player_table = Selector(text=table).xpath('//table')[4].get()

            player_row = Selector(text=player_table).xpath('//tr').getall()

            stats_row = Selector(text=player_row[0].replace('\n', '')).xpath('//text()').getall()

        stats = ()
        stats = stats_row[1:len(stats_row)+1]

        player_row = player_row[1:len(player_row)]

        Players = []

        for row in player_row:
            player_stats = []
            player_stats = self.processPlayersStat(row, stats)

            Players.append(player_stats)

        return coach, Players


    def processPlayersStat(self, row, stats):

        PS = Selector(text=row).xpath('//td/text()').getall()
        name = Selector(text=row).xpath('//a/text()').get()
        link = Selector(text=row).xpath('//a/@href').get()

        player_stats = {}

        player_stats['name'] = name
        player_stats['link'] = link

        for (s, p) in zip(stats, PS):

            x = re.sub('[^0123456789\.]', '', p)
            player_stats[StatKeys[s]] = self.FloatOrInt(x)

        return player_stats

    def processTeamStats(self, table):

        TS_rows = []
        TS_rows = Selector(text=table).xpath('//tr').getall()

        TS_rows = TS_rows[2:len(TS_rows)-1]

        HomeTeam = {}
        AwayTeam = {}

        for row in TS_rows:

            Home, label, Away = Selector(text=row).xpath('//td/text()').getall()
            label = re.sub('[^0-9a-zA-Z]', '', label)

            if label != 'Statistic':
                #process into int or float
                Home = re.sub('[^0123456789\.]', '', Home)
                Away = re.sub('[^0123456789\.]', '', Away)

                HomeTeam[label] = self.FloatOrInt(Home)
                AwayTeam[label] = self.FloatOrInt(Away)

        return HomeTeam, AwayTeam

    def FloatOrInt(self, x):

        if x == '':  #FootyWire you're killing me here. change from '' to -1 to imply N/A
            x = '-1'

        if re.search('\.',x) is None:
            return int(x)
        else:
            return float(x)
