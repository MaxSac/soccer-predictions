
# coding: utf-8

# # First Test

# In[68]:

from urllib.request import urlopen, Request
import json
from pandas.io.json import json_normalize
from pprint import pprint
from datetime import date
import os

class leauge(team, season):
    def __init__(self):
        self.lastLoadMatchday = None
    
    def downloadMatchDay(self, year, day):
        ''' Download the Json file and save it in the season folder.
        
        First of all it looks if a folder with the same name already exist. 
        Following it creates an folder if it doesn't. Afterwords it download
        the JSOON-file and save the download.
        
        Parameters : 
        year = int or stirng
            The seasonyear of the observable event.
        day = int or string
            The matchday of the observable event.
        '''
        if not os.path.exists(str(year)):
            os.makedirs(str(year))
        season_day = (str(year) + '/' + str(day))
        request = Request('https://www.openligadb.de/api/getmatchdata/bl1/'+season_day)
        response = json.loads(urlopen(request).read().decode('utf-8'))
        # Save the Download in File season_day.json
        with open(season_day + '.json', 'w') as f:
             json.dump(response, f)
        
    def loadMatchDay(self, year, day):    
        ''' Load the JSON file from your local disk.
        
        Parameters : 
        year = int or stirng
            The seasonyear of the observable event.
        day = int or string
            The matchday of the observable event.
        Returns:
            The data form the file.
        '''
        season_day = (str(year) + '/' + str(day))
        with open(season_day+'.json', 'r') as f:#(str(year)+'/'+ str(day) + 
            return json.load(f)
    
    def loadRek(self):
        if self.loadMatchDay(self.lastLoadMatchday[0], self.lastLoadMatchday[1])[8]['MatchIsFinished']==0:
            print('Finished')
            return 1
        else:
            if (self.lastLoadMatchday[1]>=34):
                self.lastLoadMatchday[1] = 1
                self.lastLoadMatchday[0] += 1
                print('Now loading season', self.lastLoadMatchday[0])
            else:
                self.lastLoadMatchday[1] +=1
            print('loading ...')
            self.downloadMatchDay(self.lastLoadMatchday[0], self.lastLoadMatchday[1])
            self.loadRek()
            return 0
        
    def getUpdate(self):
        ''' Load all data to the newest one.
        
        '''
        if(self.lastLoadMatchday == None):
            firstEntryYear = 2013
            firstEntryDay = 1
            self.lastLoadMatchday = [firstEntryYear, firstEntryDay]
            pprint('Download all scores till season: ' + str(firstEntryYear) + '/' + str(firstEntryYear+1))
        
        self.downloadMatchDay(self.lastLoadMatchday[0], self.lastLoadMatchday[1])
        self.loadRek()
        print(self.lastLoadMatchday)
    
    def printResults(self, year, day):
        Data = self.loadMatchDay(year, day)
        for x in range(len(Data)):
            print(Data[x]['Team1']['TeamName'], Data[x]['MatchResults'][1]['PointsTeam1'], ':'
                  , Data[x]['MatchResults'][1]['PointsTeam2'], Data[x]['Team2']['TeamName'])
        
#season_day = '2016/30'
#request = Request('https://www.openligadb.de/api/getmatchdata/bl1/'+season_day)
#response = urlopen(request).read().decode('utf-8')
#data = json.loads(response)
#data[0]['Goals'][1]


# In[70]:

Bundesliga = leauge()


# In[72]:

Bundesliga.downloadMatchDay(2016,31)
Bundesliga.loadMatchDay(2016,31)
Bundesliga.getUpdate()


# In[160]:

Bundesliga.lastUpdate > date(2014 ,7 ,8)


# In[14]:

class iterationDays:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return 1
        else:
            print('FUUUUUU')
            return 0
test = iterationDays(34)
while(test.next()==True):
    print('loading ...')


# In[ ]:




# In[65]:

class iterationDays:
    def __init__(self, matchFinished):
        self.mF = matchFinished
        self.day = 0
        self.year = 0
        
    def __iter__(self):
        return self

    def next(self):
        if self.mF[self.day + self.year*4] == True:
            if (self.day>33):
                self.day = 0
                self.year += 1
            else:
                self.day += 1
            print('day = ', self.day, 'year', self.year)
            return 1
        else:
            print('FUUUUUU')
            return 0


# In[ ]:



