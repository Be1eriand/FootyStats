# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FootystatsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FootyMatchItem(Item):

    fwID = Field()
    MatchDate = Field()
    MatchTime = Field()
    Ground = Field()
    Round = Field()
    Attendance = Field()
    HomeTeamName = Field()
    HomeTeamCoach = Field()
    HomeTeamScore = Field()
    HomeTeamStats = Field()
    HomeTeamPlayers_Stats = Field()
    HomeTeamPlayers_AdvStats = Field()
    AwayTeamName = Field()
    AwayTeamCoach = Field()
    AwayTeamScore = Field()
    AwayTeamStats = Field()
    AwayTeamPlayers_Stats = Field()
    AwayTeamPlayers_AdvStats = Field()

class TeamScore(Item):

    Q1 = Field()
    Q2 = Field()
    Q3 = Field()
    Q4 = Field()
    FinalScore = Field()

class TeamStats(Item):

    Kicks = Field()
    Handballs = Field()
    Disposals = Field()
    KicktoHandballR = Field()
    Marks = Field()
    Tackles = Field()
    Hitouts = Field()
    FreesFor = Field()
    FreesAgainst = Field()
    GoalsKicked = Field()
    GoalAssists = Field()
    BehindsKicked = Field()
    RushedBehinds = Field()
    ScoringShots = Field()
    Conversion = Field()
    DispsPerGoal = Field()
    DispsPerSS = Field()
    Clearances = Field()
    Clangers = Field()
    Rebound_50s = Field()
    Inside_50s = Field()
    In50sPerSS = Field()
    In50sPerGoal = Field()
    PercentIn50sScore = Field()
    PercentIn50sGoal = Field()

class Player_Stats(Item):

    Name = Field()
    fwID = Field()
    Kicks = Field()
    Handball= Field()	
    Disposals= Field()	
    Marks = Field()
    Goals = Field()
    Behinds = Field()
    Tackles = Field()	
    Hitouts = Field()
    GoalAssists = Field()
    Iinside50 = Field()
    Clearances = Field()
    Clangers = Field()	
    Rebound50 = Field()
    FreesFor = Field()	
    FreesAgainst = Field()
