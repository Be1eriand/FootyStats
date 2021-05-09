from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Date, DateTime, Float, Boolean, Text, Time)
#from scrapy.utils.project import get_project_settings

Base = declarative_base()

class Advance_Stats(Base):

    __tablename__ = "AdvanceStats"

    id = Column(Integer, primary_key=True)
    Contested_Possessions = Column(Integer)
    Uncontested_Possession = Column(Integer)
    Effective_Disposals = Column(Integer)
    Disposal_Efficiency = Column(Float)
    Contested_Marks = Column(Integer)
    Goal_Assists = Column(Integer)
    Marks_Inside_50 = Column(Integer)
    One_Percenters = Column(Integer)
    Bounces = Column(Integer)
    Centre_Clearances = Column(Integer)
    Stoppage_Clearances = Column(Integer)
    Score_Invlovement = Column(Integer)
    Metres_Gained = Column(Integer)
    Turnovers = Column(Integer)
    Intercepts = Column(Integer)
    Tackles_inside_50 = Column(Integer)
    Time_on_ground = Column(Integer)

class Basic_Stats(Base):

    __tablename__ = "BasicStats"

    id = Column(Integer, primary_key=True)
    Kicks = Column(Integer)
    Handballs = Column(Integer)
    Disposals = Column(Integer)
    Marks = Column(Integer)
    Goals = Column(Integer)
    Behinds = Column(Integer)
    Tackles = Column(Integer)
    Hitouts = Column(Integer)
    Goal_Assists = Column(Integer)
    Inside_50 = Column(Integer)
    Clearances = Column(Integer)
    Clangers = Column(Integer)
    Rebound_50 = Column(Integer)
    Frees_For = Column(Integer)
    Frees_Against = Column(Integer)
    AFLFantasy = Column(Integer)
    SuperCoach = Column(Integer)

class Player(Base):

    __tablename__ = 'PlayerDetails'

    id = Column(Integer, primary_key=True)
    First_Name = Column(String)
    Last_Name = Column(String)
    Link_Name = Column(String)

    team = relationship("Team_List", back_populates="player")
    clublist = relationship('Club_List', back_populates='players')


class Club(Base):

    __tablename__ = 'ClubDetails'

    id = Column(Integer, primary_key=True)
    Club_Name = Column(String)
    City = Column(String)
    State = Column(String)
    Home_ground = Column(String)

    playerlist = relationship('Club_List', back_populates='clubs')


class Coach(Base):

    __tablename__ = 'CoachDetails'

    id = Column(Integer, primary_key=True)
    First_Name = Column(String)
    Last_Name = Column(String)


class Ground(Base):

    __tablename__ = 'Ground'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    City = Column(String)
    State = Column(String)


class Fixture(Base):

    __tablename__ = 'Fixture'

    fwID  = Column(Integer, primary_key=True)
    Round = Column(String)
    Ground = Column(String)
    HomeTeamID = Column(Integer, ForeignKey('TeamDetails.id'))
    AwayTeamID = Column(Integer, ForeignKey('TeamDetails.id'))
    HomeScoresID = Column(Integer,ForeignKey('MatchScores.id'))
    AwayScoresID = Column(Integer, ForeignKey('MatchScores.id'))
    MatchDate = Column(Date)
    MatchTime = Column(DateTime)
    Attendance = Column(Integer)

    HomeScores = relationship("Match_Scores", foreign_keys=[HomeScoresID])
    AwayScores = relationship("Match_Scores", foreign_keys=[AwayScoresID])
    HomeTeam = relationship("Team", foreign_keys=[HomeTeamID])
    AwayTeam = relationship("Team", foreign_keys=[AwayTeamID])


class Match_Scores(Base):

    __tablename__ = 'MatchScores'

    id = Column(Integer, primary_key=True)
    Q1 = Column(String)
    Q2 = Column(String)
    Q3 = Column(String)
    Q4 = Column(String)
    FinalScore = Column(Integer)


class Team(Base):

    __tablename__ = 'TeamDetails'

    id = Column(Integer, primary_key=True)
    ClubID = Column(Integer, ForeignKey('ClubDetails.id'))
    CoachID = Column(Integer, ForeignKey('CoachDetails.id'))
    HomeAway = Column(String)
    Kicks = Column(Integer) #Team Stats
    Handballs = Column(Integer)
    Disposals = Column(Integer)
    KicktoHandballRatio = Column(Float)
    Marks = Column(Integer)
    Tackles = Column(Integer)
    Hitouts = Column(Integer)
    FreesFor = Column(Integer)
    FreesAgainst = Column(Integer)
    GoalsKicked = Column(Integer)
    BehindsKicked = Column(Integer)
    RushedBehinds = Column(Integer)
    ScoringShots = Column(Integer)
    Conversion = Column(Float)
    DisposalsPerGoal = Column(Float)
    DispsPerScoringShot = Column(Float)


    club = relationship('Club')
    coach = relationship('Coach')

    players = relationship('Team_List', back_populates='teamlist')


class Team_List(Base):

    __tablename__ = 'TeamList'

    PlayerID = Column(Integer, ForeignKey('PlayerDetails.id'), primary_key=True)
    TeamID = Column(Integer, ForeignKey('TeamDetails.id'), primary_key=True)
    BasicStats = Column(Integer, ForeignKey('BasicStats.id'))
    AdvancedStats = Column(Integer, ForeignKey('AdvanceStats.id'))

    basicstats = relationship('Basic_Stats')
    advancedstats = relationship('Advance_Stats')
    teamlist = relationship("Team", back_populates="players")
    player = relationship("Player", back_populates="team")


class Club_List(Base):

    __tablename__ = 'ClubList'

    ClubID = Column(Integer,
                         ForeignKey('ClubDetails.id'),
                         primary_key=True)
    PlayerID = Column(Integer,
                             ForeignKey('PlayerDetails.id'),
                             primary_key=True)
    Start_year = Column(Date)
    End_year = Column(Date)

    clubs = relationship('Club',  back_populates='playerlist')
    players = relationship('Player', back_populates='clublist')
