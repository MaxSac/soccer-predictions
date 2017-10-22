
# coding: utf-8

# In[11]:

import json
from pandas.io.json import json_normalize
exec(open('downloader.py').read())


# In[12]:

class getInfo():
    def __init__(self, data, day):
        self.data = data
        self.day = day
        
    def mergeMatchGames(self):
        storage = pd.DataFrame()
        for x in range(9):
            match = self.data[x]
            Match = pd.DataFrame({
                    'Team1': [self.getTeam1Name(match)],
                    'Team2': [self.getTeam2Name(match)],
                    'HalftimeResult': [self.getHalfResult(match)],
                    'FinalResult': [self.getEndResult(match)],
                    'GoalTimeTeam1': [self.getGoalTimeTeam1(match)],
                    'GoalTimeTeam2': [self.getGoalTimeTeam2(match)],
                    'Spectators': [self.getSpectators(match)],
                    'DateTime': [self.getDateTime(match)],
                    'Weekday': [self.getDateTime(match).dayofweek],
                    'Hour': [self.getDateTime(match).hour],
                    'PeanltyTeam1': [self.getPenaltyTeam1(match)],
                    'PenaltyTeam2': [self.getPenaltyTeam2(match)],
                    'ScorerTeam1': [self.getScorerTeam1(match)],
                    'ScorerTeam2': [self.getScorerTeam2(match)],
                    'OwnGoalTeam1': [self.getOwnGoalTeam1(match)],
                    'OwnGoalTeam2': [self.getOwnGoalTeam2(match)],
                    'OvertimeGoalTeam1': [self.getOvertimeGoalTeam1(match)],
                    'OvertimeGoalTeam2': [self.getOvertimeGoalTeam2(match)],
                    'Matchday': [self.getMatchday(self.day)]
                })
            storage = storage.append(Match)
        return storage
   
    def getTeam1Name(self,match):
        return match['Team1']['TeamName']
    
    def getTeam2Name(self,match):
        return match['Team2']['TeamName']
    
    def getHalfResult(self,match):
        return [match['MatchResults'][0]['PointsTeam1'], match['MatchResults'][0]['PointsTeam2']]

    def getEndResult(self,match):
        return [match['MatchResults'][1]['PointsTeam1'], match['MatchResults'][1]['PointsTeam2']]
    
    def mergeInfoTeam(self, match, Info, teamNumber):
        info = np.array([])
        team = np.array([])
        for x in match['Goals']:
            team = np.append(team, x['ScoreTeam'+str(teamNumber)])
            info = np.append(info, x[Info])
        team = team[info != np.array(None)]
        info = info[info != np.array(None)]
        if(len(info)==0):
            return np.array([0])
        elif(len(team)>1):
            mask = np.append(team[0], team[1:]-team[:-1]).astype(bool)
            return info[mask]
        else:
            mask = team[0].astype(bool)
            return info[mask]
    
    def getGoalTimeTeam1(self, match):
        return self.mergeInfoTeam(match, 'MatchMinute', 1).astype(int)
    
    def getGoalTimeTeam2(self, match):
        return self.mergeInfoTeam(match, 'MatchMinute', 2).astype(int)
    
    def getPenaltyTeam1(self, match):
        return self.mergeInfoTeam(match, 'IsPenalty', 1).astype(bool)
    
    def getPenaltyTeam2(self, match):
        return self.mergeInfoTeam(match, 'IsPenalty', 2).astype(bool)
    
    def getOwnGoalTeam1(self, match):
        return self.mergeInfoTeam(match, 'IsOwnGoal', 1).astype(bool)
    
    def getOwnGoalTeam2(self, match):
        return self.mergeInfoTeam(match, 'IsOwnGoal', 2).astype(bool)
    
    def getOvertimeGoalTeam1(self, match):
        return self.mergeInfoTeam(match, 'IsOvertime', 1).astype(bool)
    
    def getOvertimeGoalTeam2(self, match):
        return self.mergeInfoTeam(match, 'IsOvertime', 2).astype(bool)
    
    def getScorerTeam1(self, match):
        return self.mergeInfoTeam(match, 'GoalGetterName', 1)
    
    def getScorerTeam2(self, match):
        return self.mergeInfoTeam(match, 'GoalGetterName', 2)
    
    def getSpectators(self,match):
        return match['NumberOfViewers']
    
    def getDateTime(self,match):
        return pd.to_datetime(match['MatchDateTime'], unit='ns', errors='ignore', box=True)
    
    def getMatchday(self, day):
        return day


# In[15]:

class converter(downloader, getInfo):
    def __init__(self):
        self.status = None
        self.lastConvMatchday = self.readLastConvMatchday()
    
    def readLastConvMatchday(self):
        info = self.loadInfo()
        if('lastConvMatchday' in info):
            self.lastConvMatchday = info['lastConvMatchday']
        else:
            self.lastConvMatchday = downloader().beginHistory()
            self.updateInfo({'lastConvMatchday': self.lastConvMatchday})
        return self.lastConvMatchday
            
    def saveLastConvMatchday(self):
        '''update the last load matchday from info.txt file'''
        self.updateInfo({'lastConvMatchday': self.lastConvMatchday})
    
    def raiseMatchday(self):
        if(self.lastConvMatchday[1]>=34):
            self.lastConvMatchday[1] = 1
            self.lastConvMatchday[0] += 1
            print('Now loading season', self.lastConvMatchday[0])
        else:
            self.lastConvMatchday[1] += 1
            print(self.lastConvMatchday)
    
    def loadMatchday(self, year, day):
        season_day = (str(year) + '/' + str(day))
        with open(season_day+'.json', 'r') as f:#(str(year)+'/'+ str(day) + 
            return json.load(f)
    
    def convertMatchday(self, year, day):
        jsonData = self.loadMatchday(year, day)
        pandasData = getInfo(jsonData, day).mergeMatchGames()
        return pandasData
    
    def saveMatchday(self, data, year, day):
        file = './data/'+str(year)
        if(os.path.isfile(file)== True):
            loadData = pd.read_pickle(file)
            loadData = loadData.append(data)
            loadData.to_pickle(file)
        else:
            data.to_pickle(file)
                
    def updateSeason(self):
        downloader().getUpdate()
        lastConv = np.array(self.readLastConvMatchday())
        lastDown = np.array(self.readLastLoadMatchday())
#        print((lastDown < lastConv))
        if((lastDown <= lastConv).sum()!=2):
#            print(lastDown<=lastConv)
            data = self.convertMatchday(self.lastConvMatchday[0], self.lastConvMatchday[1])
            self.saveMatchday(data, self.lastConvMatchday[0], self.lastConvMatchday[1])
            self.raiseMatchday()
            self.saveLastConvMatchday()
#            print(self.lastConvMatchday)
            self.updateSeason()
        else:
            print('Everything up to date')
    


# In[17]:

converter().updateSeason()
