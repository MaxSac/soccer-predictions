import os.path

def doMergeDict(dict1, dict2):
    mergeDict = dict1
    for key in dict1.keys():
        if(not key in dict2.keys()):
            mergeDict[key] = dict1[key]
        else:
            mergeDict[key] = np.append(mergeDict[key], dict2[key])
    for key in dict2.keys():
        if(not key in dict1.keys()):
            mergeDict[key] = dict2[key]
    return mergeDict

class season:
    def calcDayPlayed(self):
        """ Calculate the played matchdays with help of the json-files.
        
        Returns:
            The last played compelted matchday.
        """
        matchday = 1
        while(os.path.exists(str(self.season)+'/'+str(matchday)+'.json')==True): 
            matchday +=1
        return matchday-1

    def loadTeams(self):
        ''' Return a array with the names of the teams which 
            played in this season.
        '''
        data = leauge.loadMatchDay(self, self.season, 1)
        teams = []
        for x in range(len(data)):
            teams = np.append(teams, 
                              ([data[x]['Team1']['TeamName'], 
                                data[x]['Team2']['TeamName']]))
        with open('info.json', 'r') as file:
            json_data = json.load(file)
        json_data.update({'season'+str(self.season): {'teams':teams.tolist()}})
        pprint(json_data)
        with open('info.json', 'w') as file:
            file.write(json.dumps(json_data))
        return teams
    
    def loadScores(self, matchDay):
        ''' Load the halftime-/final-result, spectators, 
            goaldifference from the selected matchday
        
        Parameters:
        matchDay: int
            This should be the day, where the informations are about.
            
        Returns:
        score: dict
            With scalar values of the matchday
        '''
        data = leauge.loadMatchDay(self, self.season, matchDay)
        score = {'home': 'Team1', 'away': 'Team2'}
        for key in score.keys():
            result = dict()
            halftime = dict()
            spectators = dict()
            difference = dict()
            matchday = dict()
            for x in range(len(data)):
                if (key == 'home'): 
                    result[data[x]['Team1']['TeamName']] = data[x]['MatchResults'][1]['PointsTeam1'] 
                    halftime[data[x]['Team1']['TeamName']] = data[x]['MatchResults'][0]['PointsTeam1'] 
                    spectators[data[x]['Team1']['TeamName']] = data[x]['NumberOfViewers']
                    difference[data[x]['Team1']['TeamName']] = data[x]['MatchResults'][1]['PointsTeam1'] - data[x]['MatchResults'][1]['PointsTeam2'] 
                    matchday[data[x]['Team1']['TeamName']] = matchDay
                    a =zip(['result', 'halftime', 'spectators', 'difference', 'matchday'],[result, halftime, spectators, difference, matchday])
                elif (key == 'away'):
                    result[data[x]['Team2']['TeamName']] = data[x]['MatchResults'][1]['PointsTeam2'] 
                    halftime[data[x]['Team2']['TeamName']] = data[x]['MatchResults'][0]['PointsTeam2'] 
                    difference[data[x]['Team2']['TeamName']] = data[x]['MatchResults'][1]['PointsTeam2'] - data[x]['MatchResults'][1]['PointsTeam1'] 
                    matchday[data[x]['Team2']['TeamName']] = matchDay
                    a = zip(['result', 'halftime', 'difference', 'matchday'],[result, halftime, difference, matchday])
            score[key] = dict(a)
        return score
        
    def scoresSeason(self):
        ''' Make out of the scalar values from a single load values 
            an nd.array with the stats from beginning up to date. For 
            more information about the values, look to leaque.loadScores().
        
        Returns:
        season: dict
            A dict full of informations, about the game stats. 
        '''
        season = dict()
        for key in self.loadScores(1).keys():
            storage = dict()
            for x in range(self.currentMatchDay-1):
                for keyII in self.loadScores(x+1)[key].keys():
                    if(x==0):
                        storage[keyII] = self.loadScores(x+1)[key][keyII]
                    else:
                        storage[keyII] = doMergeDict(storage[keyII], 
                                                     self.loadScores(x+1)[key][keyII])
                season[key] = storage
        return season
    
    def loadPaarings(self, matchDay):
        ''' Preferce an numpy array, because search is easily. An example:
        a = np.array([[1,2],[3,4]])
        [1,2] == a
        array([[ True,  True],
               [False, False]], dtype=bool)
        '''
        data = leauge.loadMatchDay(self, self.season, matchDay)
        parings = np.array([[[data[0]['Team1']['TeamName']], [data[0]['Team2']['TeamName']]]])
        for x in range(len(data)-1):
            parings = np.append(parings, 
                                [[[data[x+1]['Team1']['TeamName']], 
                                  [data[x+1]['Team2']['TeamName']]]],
                                axis=0)
        return np.squeeze(parings)

    def paaringsSeason(self):
        matchPaarungen = [self.loadPaarings(1)]
        for x in range(self.currentMatchDay):
            matchPaarungen = np.append(matchPaarungen, 
                                       [self.loadPaarings(x+1)], 
                                       axis=0)
        return np.squeeze(matchPaarungen)
    
    def calcPoints(self, typ='total'):
        ''' Returns the points of the actuell season.
        Parameters:
        typ = 'total'/'away'/'home'
        Returns:
        points 
            Dict of teamname and an array of Points
        '''
        points = dict()
        if(typ=='total'):
            typ = 'home'
            home = self.calcPoints('home')
            typ = 'away'
            away = self.calcPoints('away')
            for team in self.teams:
                points[team] = np.append(home[team], away[team]) 
                matchday = np.append(self.scores['home']['matchday'][team], 
                                     self.scores['away']['matchday'][team])
                points[team] = np.squeeze(np.array([x for (y,x) in sorted(zip(matchday,points[team]))]))
            return points
        for x in self.teams:
            diff = np.array(self.scores[typ]['difference'][x])
            win = diff > 0
            draw = diff == 0
            loose = diff < 0
            for a in zip([win, draw, loose], [3,1,0]):
                diff[a[0]] = a[1]
            points[x] = diff 
        return points
    
    def calcTable(self, typeOfTable='total', matchday = 1):
        points = np.array([])
        scores = np.array([])
        team =  np.array([])
        threeWays = np.array([])
        for teams in self.teams:
            points = np.append(points, np.sum(self.calcPoints(typeOfTable)[teams]))
            threeWays = np.append(threeWays, dict(zip(['win','draw','loose'],
                                                      [np.sum(self.calcPoints(typeOfTable)[teams]==3), 
                                                       np.sum(self.calcPoints(typeOfTable)[teams]==1), 
                                                       np.sum(self.calcPoints(typeOfTable)[teams]==0)])))
            if(typeOfTable=='total'):
                scores = np.append(scores, np.sum(self.scores['home']['difference'][teams]) + np.sum(self.scores['away']['difference'][teams]))
            else:
                scores = np.append(scores, np.sum(self.scores[typeOfTable]['difference'][teams]))
            team = np.append(team, teams)
        mask = np.lexsort((scores, points))[::-1] #flip the list from 18 to 1, to 1 to 18
        table = dict()
        for x in mask:
            table[x+1] = dict(zip(['club','points', 'score', 'threeWays'],
                                  [team[mask[x]], points[mask[x]], scores[mask[x]], threeWays[mask[x]]]))
        return table
    
    def matchSearch(self, team1, team2, order=False):
        """ Search after a game
        Parameters: 
            
        Returns:
        
        """
        mask = self.matchPaarings == [str(team1), str(team2)]
        matchDay = lambda x : np.sum(mask[x][:][:], axis=1)
        response = []
        for x in range(self.currentMatchDay):
            if(np.argwhere(np.array(matchDay(x))==2)>=0):
                response = [x, np.argwhere(np.array(matchDay(x))==2).reshape(1)]
        if(order==True):
            response = [[response], [self.matchSearch(team2, team1)]]
        return np.array(response)
    
    def __init__(self, season):    
        self.season = season
        self.currentMatchDay = self.calcDayPlayed()   # Return the last completed matchday
        self.teams = self.loadTeams()                 # list of all teams which played in this season
        self.scores = self.scoresSeason()
        self.matchPaarings = self.paaringsSeason()
            # Ein array an welchen Spieltach welche manschaft gegen Welche gespielt hatt.
        
exec(open('Einlesen.py').read())
