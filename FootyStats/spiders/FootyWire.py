import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from FootyStats.items import FootyMatchItem
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time
from dateutil.parser import parse, ParserError


class FootywireSpider(CrawlSpider):
    name = 'FootyWire'
    allowed_domains = ['footywire.com']
    start_urls = ['https://www.footywire.com/afl/footy/ft_match_list?year=1965']
    base_url = 'https://www.footywire.com/afl/footy/'

    rules = (
        Rule(LinkExtractor(allow=('ft_match_list\?year=',), deny=('round','finals'))),
        Rule(LinkExtractor(allow=('ft_match_statistics',)), callback='parseFixtures')
        )
            

    def parseFixtures(self, response):

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
        MatchItem['HomeTeamScore'], MatchItem['AwayTeamScore'] = self.processScores(ScoresTbl) 
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
        HomeTeamTbl = Selector(text=pageTbl.get()).xpath('//table')[5].get()
        AwayTeamTbl = Selector(text=pageTbl.get()).xpath('//table')[9].get()
        TeamStatsTbl = Selector(text=pageTbl.get()).xpath('//table')[13].get()

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
            t = d_list[2].strip(' ')
        else:
            t =''

        return day, d.strftime('%d/%m/%Y'), t

    def processScores(self, table):

        rows = Selector(text=table).xpath('//tr')
        HSc = Selector(text=rows[1].get()).xpath('//td/text()').getall()
        ASc = Selector(text=rows[2].get()).xpath('//td/text()').getall()

        quarters = ('Q1', 'Q2', 'Q3', 'Q4', 'FinalScore')

        HomeScores = {}
        AwayScores = {}

        for (Q, H, A) in zip(quarters, HSc, ASc):
            HomeScores[Q] = H.strip(' \n')
            AwayScores[Q] = A.strip(' \n')

        return HomeScores, AwayScores

    def processTeam(self, table):

        coach = Selector(text=table).xpath('//table//td/a/text()').get()

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

            if re.search('.',x) is None:
                player_stats[s] = int(x)
            else:
                player_stats[s] = float(x)

        if 'AF' in stats:
            player_stats.pop('AF')
            player_stats.pop('SC')

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
            HomeTeam[label] = Home
            AwayTeam[label] = Away

        return HomeTeam, AwayTeam
