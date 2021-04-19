from FootyStats.spiders import FootywireSpider
import pytest


@pytest.fixture
def FwS():
    return FootywireSpider()

def test_getFootyWireID(FwS):

    FootyWireID = 10359
    url = 'https://www.footywire.com/afl/footy/ft_match_statistics?mid=10359'

    result = FwS.getFootyWireID(url)

    assert result == FootyWireID


def test_getMatchInfo(FwS):

    #test without attendance
    info = {}
    info['Date'] = '10/04/2021'
    info['Time'] = '7:25 PM AEST'
    info['Ground'] = 'MCG'
    info['Round'] = 'Round 4'
    info['Attendance'] = 0

    table = '<table border = "0" cellspacing = "0" cellpadding = "0" width = "525"><tbody> <tr> <td width = "525" valign = "top" height = "30" align = "left" class = "hltitle"> Collingwood defeated by GWS</td></tr><tr> <td class = "lnorm" height = "22"> Round 4, MCG </td> </tr><tr> <td class = "lnorm" height = "22">Saturday, 10th April 2021, 7:25 PM AEST </td> </tr>'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']


def test_getMatchInfowithA(FwS):
    #test with attendance
    info = {}
    info['Date'] = '10/04/2021'
    info['Time'] = '7:25 PM AEST'
    info['Ground'] = 'MCG'
    info['Round'] = 'Round 4'
    info['Attendance'] = 29866

    table = '<table border = "0" cellspacing = "0" cellpadding = "0" width = "525"><tbody> <tr> <td width = "525" valign = "top" height = "30" align = "left" class = "hltitle"> Collingwood defeated by GWS</td></tr><tr> <td class = "lnorm" height = "22"> Round 4, MCG, Attendance: 29866</td> </tr><tr> <td class = "lnorm" height = "22">Saturday, 10th April 2021, 7:25 PM AEST </td> </tr>'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']


def test_getMatchInfoNoGA(FwS):
    #test - no ground, attendance
    info = {}
    info['Date'] = '10/08/2002'
    info['Time'] = ''
    info['Ground'] = ''
    info['Round'] = 'Round 19'
    info['Attendance'] = 0

    table = '<table border = "0" cellspacing = "0" cellpadding = "0" width = "525"><tbody > <tr > <td width = "525" valign = "top" height = "30" align = "left" class = "hltitle" >Carlton defeated by Port Adelaide</td > </tr ><tr > <td class = "lnorm" height = "22" > Round 19, Saturday, 10th August 2002 </td> </tr ><tr > <td class = "lnorm" height = "22" > &nbsp</td></tr><tr> <td class = "lnorm" height = "22" ><b> Brownlow Votes: </b>3: < a href = "pp-carlton-blues--craig-bradley" > C Bradley < /a > , 2: < a href = "pp-port-adelaide-power--roger-james" > R James </a> , 1: <a href = "pp-carlton-blues--sam-cranage"> S Cranage </a> </td></tr></tbody > </table >'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']


def test_getMatchInfoNoTime(FwS):
    info = {}
    info['Date'] = '22/04/2006'
    info['Time'] = ''
    info['Ground'] = 'Gabba'
    info['Round'] = 'Round 4'
    info['Attendance'] = 30266

    table = '<table border="0" cellspacing="0" cellpadding="0" width="525"><tbody><tr><td width="525" valign="top" height="30" align="left" class="hltitle">Brisbane defeated by Richmond</td></tr><tr><td class="lnorm" height="22">Round 4, Gabba, Attendance: 30266</td></tr><tr><td class="lnorm" height="22">Saturday, 22nd April 2006</td></tr><tr><td class="lnorm" height="22"><b>Brownlow Votes:</b>3: <a href="pp-richmond-tigers--matthew-richardson">M Richardson</a>, 2: <a href="pp-richmond-tigers--greg-tivendale">G Tivendale</a>, 1: <a href="pp-brisbane-lions--jonathan-brown">J Brown</a></td></tr></tbody></table>'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']


def test_getMatchInfoFinalsv2(FwS):
    info = {}
    info['Date'] = '04/09/1999'
    info['Time'] = ''
    info['Ground'] = ''
    info['Round'] = 'Qualifying Final'
    info['Attendance'] = 0

    table = '<table border="0" cellspacing="0" cellpadding="0" width="525"><tbody><tr><td width="525" valign="top" height="30" align="left" class="hltitle">North Melbourne defeats Port Adelaide</td></tr><tr><td class="lnorm" height="22">Qualifying Final, Saturday, 4th September 1999</td></tr><tr><td class="lnorm" height="22">&nbsp;</td></tr></tbody></table>'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']

def test_getMatchInfoFinalsv1(FwS):
    info = {}
    info['Date'] = '30/09/2017'
    info['Time'] = '2:30 PM AEST'
    info['Ground'] = 'MCG'
    info['Round'] = 'Grand Final'
    info['Attendance'] = 100021

    table = '<table border="0" cellspacing="0" cellpadding="0" width="525"><tbody><tr><td width="525" valign="top" height="30" align="left" class="hltitle">Adelaide defeated by Richmond</td></tr><tr><td class="lnorm" height="22">Grand Final, MCG, Attendance: 100021</td></tr><tr><td class="lnorm" height="22">Saturday, 30th September 2017, 2:30 PM AEST</td></tr><tr><td class="lnorm" height="22">Adelaide Betting Odds: Win 1.75, Line -7 @ 1.95</td></tr><tr><td class="lnorm" height="22">Richmond Betting Odds: Win 2.25, Line +6 @ 1.95</td></tr></tbody></table>'

    date, time, ground, rnd, attendance = FwS.getMatchInfo(table)

    assert date == info['Date']
    assert time == info['Time']
    assert ground == info['Ground']
    assert rnd == info['Round']
    assert attendance == info['Attendance']


def test_processDate(FwS):

    dt = 'Saturday, 10th April 2021, 7:25 PM AEST'
    day = 'Saturday'
    d = '10/04/2021'
    t = '7:25 PM AEST'

    day_r, d_r, t_r = FwS.processDate(dt)

    assert day_r == day
    assert d_r == d
    assert t_r == t


def test_processScores(FwS):

    table = '<table border="0" cellspacing="0" cellpadding="0" width="466" id="matchscoretable">\n<tr>\n<th class="leftbold" height="30" width="140">Team\n</th><th width="59" align="center">Q1\n</th><th width="59" align="center">Q2\n</th><th width="59" align="center">Q3\n</th><th width="59" align="center">Q4\n</th><th width="59" align="center">Final\n</th></tr>\n<tr>\n<td class="leftbold" height="28"><a href="th-collingwood-magpies">Collingwood</a></td>\n<td align="center">1.2 \n</td><td align="center">4.5 \n</td><td align="center">7.6 \n</td><td align="center">9.6 \n</td><td align="center">60\n</td></tr>\n<tr>\n<td class="leftbold" height="28"><a href="th-greater-western-sydney-giants">GWS</a></td>\n<td align="center">2.2 \n</td><td align="center">6.3 \n</td><td align="center">10.3 \n</td><td align="center">14.6 \n</td><td align="center">90\n</td></tr>\n</table>'

    HomeScores = {}
    AwayScores = {}

    HomeScores['Q1'] = '1.2'
    HomeScores['Q2'] = '4.5'
    HomeScores['Q3'] = '7.6'
    HomeScores['Q4'] = '9.6'
    HomeScores['FinalScore'] = '60'

    AwayScores['Q1'] = '2.2'
    AwayScores['Q2'] = '6.3'
    AwayScores['Q3'] = '10.3'
    AwayScores['Q4'] = '14.6'
    AwayScores['FinalScore'] = '90'

    Score_Home, Score_Away = FwS.processScores(table)

    assert Score_Home == HomeScores
    assert Score_Away == AwayScores
    

def test_processPlayersStat(FwS):

    table = '<tr><td align="left" height="18"><a href="pp-collingwood-magpies--steele-sidebottom" title="Steele Sidebottom">Steele Sidebottom</a></td><td class="statdata">21</td><td class="statdata">9</td><td class="statdata">30</td><td class="statdata">8</td><td class="statdata">0</td><td class="statdata">0</td><td class="statdata">2</td><td class="statdata">0</td><td class="statdata">0</td><td class="statdata">6</td><td class="statdata">3</td><td class="statdata">7</td><td class="statdata">1</td><td class="statdata">1</td><td class="statdata">2</td><td class="statdata">108</td><td class="statdata">79</td></tr>'

    player_stats = {}
    player_stats['name'] = 'Steele Sidebottom'
    player_stats['link'] =  'pp-collingwood-magpies--steele-sidebottom'
    player_stats['K'] = 21
    player_stats['HB'] = 9
    player_stats['D'] = 30
    player_stats['M'] = 8
    player_stats['G'] = 0
    player_stats['B'] = 0
    player_stats['T'] = 2
    player_stats['HO'] = 0
    player_stats['GA'] = 0
    player_stats['I50'] = 6
    player_stats['CL'] = 3
    player_stats['CG'] = 7
    player_stats['R50'] = 1
    player_stats['FF'] = 1
    player_stats['FA'] = 2

    stats = ('K', 'HB',	'D', 'M', 'G', 'B', 'T', 'HO', 'GA', 'I50', 'CL', 'CG', 'R50', 'FF', 'FA', 'AF', 'SC')

    PS = FwS.processPlayersStat(table, stats)

    assert PS == player_stats


def test_processPlayersStatwithouAF(FwS):

    row = '<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td align="left" height="18"><a href="pp-fremantle-dockers--peter-bell" title="Peter Bell">Peter Bell</a></td>\n<td class="statdata">9</td>\n<td class="statdata">23</td>\n<td class="statdata">32</td>\n<td class="statdata">4</td>\n<td class="statdata">0</td>\n<td class="statdata">0</td>\n<td class="statdata">5</td>\n<td class="statdata">0</td>\n<td class="statdata">1</td>\n<td class="statdata">0</td>\n</tr>'
    stats = ('K', 'HB', 'D', 'M', 'G', 'B', 'T', 'HO', 'FF', 'FA')

    player_stats = {}
    player_stats['name'] = 'Peter Bell'
    player_stats['link'] = 'pp-fremantle-dockers--peter-bell'
    player_stats['K'] = 9
    player_stats['HB'] = 23
    player_stats['D'] = 32
    player_stats['M'] = 4
    player_stats['G'] = 0
    player_stats['B'] = 0
    player_stats['T'] = 5
    player_stats['HO'] = 0
    player_stats['FF'] = 1
    player_stats['FA'] = 0

    PS = FwS.processPlayersStat(row, stats)

    assert PS == player_stats


def test_processTeamStats(FwS):

    table = '<table border="0" cellspacing="0" cellpadding="0" width="575">\n<tr><td height="28" align="center" colspan="5" class="tbtitle"><a name="hd"></a>Head to Head</td></tr>\n<tr>\n<td rowspan="28" class="tabbdr" style="width:1px"></td>\n<td width="190" class="bnorm" height="28">Richmond</td>\n<td width="193" class="bnorm">Statistic</td>\n<td width="190" class="bnorm">Carlton</td>\n<td rowspan="28" class="tabbdr" style="width:1px"></td>\n</tr><tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">155</td>\n<td class="statdata">Kicks</td>\n<td class="statdata">188</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">122</td>\n<td class="statdata">Handballs</td>\n<td class="statdata">114</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">277</td>\n<td class="statdata">Disposals</td>\n<td class="statdata">302</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">1.27</td>\n<td class="statdata">Kick to Handball Ratio</td>\n<td class="statdata">1.65</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">57</td>\n<td class="statdata">Marks</td>\n<td class="statdata">69</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">52</td>\n<td class="statdata">Tackles</td>\n<td class="statdata">23</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">41</td>\n<td class="statdata">Hitouts</td>\n<td class="statdata">26</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">18</td>\n<td class="statdata">Frees For</td>\n<td class="statdata">24</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">24</td>\n<td class="statdata">Frees Against</td>\n<td class="statdata">18</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">16</td>\n<td class="statdata">Goals Kicked</td>\n<td class="statdata">12</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">12</td>\n<td class="statdata">Goal Assists</td>\n<td class="statdata">5</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">8</td>\n<td class="statdata">Behinds Kicked</td>\n<td class="statdata">8</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">1</td>\n<td class="statdata">Rushed Behinds</td>\n<td class="statdata">1</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">25</td>\n<td class="statdata">Scoring Shots</td>\n<td class="statdata">21</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">64.0%</td>\n<td class="statdata">Conversion</td>\n<td class="statdata">57.1%</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">17.31</td>\n<td class="statdata">Disposals Per Goal</td>\n<td class="statdata">25.17</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">11.08</td>\n<td class="statdata">Disps Per Scoring Shot</td>\n<td class="statdata">14.38</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">30</td>\n<td class="statdata">Clearances</td>\n<td class="statdata">33</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">50</td>\n<td class="statdata">Clangers</td>\n<td class="statdata">51</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">41</td>\n<td class="statdata">Rebound 50s</td>\n<td class="statdata">29</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">48</td>\n<td class="statdata">Inside 50s</td>\n<td class="statdata">54</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">1.92</td>\n<td class="statdata">In50s Per Scoring Shot</td>\n<td class="statdata">2.57</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">3.00</td>\n<td class="statdata">Inside 50s Per Goal</td>\n<td class="statdata">4.50</td>\n</tr>\n<tr bgcolor="#ffffff" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#ffffff\';">\n<td height="25" class="statdata">50.0%</td>\n<td class="statdata">% In50s Score</td>\n<td class="statdata">37.0%</td>\n</tr>\n<tr bgcolor="#f2f4f7" onmouseover="this.bgColor=\'#cbcdd0\';" onmouseout="this.bgColor=\'#f2f4f7\';">\n<td height="25" class="statdata">33.3%</td>\n<td class="statdata">% In50s Goal</td>\n<td class="statdata">22.2%</td>\n</tr>\n<tr><td colspan="5" class="tabbdr" style="height:1px"></td></tr>\n\n</table>'

    HomeTeam={}
    AwayTeam={}

    HomeTeam['Kicks'] = '155'
    AwayTeam['Kicks'] = '188'

    result_HT, result_AT = FwS.processTeamStats(table)

    assert result_HT is not None
    assert result_AT is not None
    assert result_HT['Kicks'] == HomeTeam['Kicks']
    assert result_AT['Kicks'] == AwayTeam['Kicks']


def test_processAdvancedPlayersStat(FwS):

    table = '<tr><td align="left" height="18"><a href="pp-richmond-tigers--jack-graham" title="Jack Graham">J Graham</a></td><td class="statdata">8</td><td class="statdata">26</td><td class="statdata">26</td><td class="statdata">78.8</td><td class="statdata">0</td><td class="statdata">1</td><td class="statdata">0</td><td class="statdata">0</td><td class="statdata">0</td><td class="statdata">2</td><td class="statdata">3</td><td class="statdata">7</td><td class="statdata">836</td><td class="statdata">7</td><td class="statdata">2</td><td class="statdata">0</td><td class="statdata">76</td></tr>'

    player_stats = {}
    player_stats['name'] = 'J Graham'
    player_stats['link'] =  'pp-richmond-tigers--jack-graham'
    player_stats['CP']= 8
    player_stats['UP']=26
    player_stats['ED']=26
    player_stats['DE%']=78.8 #need to handle decimals
    player_stats['CM']=0
    player_stats['GA']=1
    player_stats['MI5']=0
    player_stats['1%']=0
    player_stats['BO']=0
    player_stats['CCL']=2
    player_stats['SCL']=3
    player_stats['SI']=7
    player_stats['MG']=836
    player_stats['TO']=7
    player_stats['ITC']=2
    player_stats['T5']=0
    player_stats['TOG%']=76

    stats = ('CP','UP','ED','DE%','CM','GA','MI5','1%','BO','CCL','SCL','SI','MG','TO','ITC','T5','TOG%')

    PS = FwS.processPlayersStat(table, stats)

    assert PS == player_stats
