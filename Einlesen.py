
# coding: utf-8

# # First Test

# In[3]:

from urllib.request import urlopen, Request
import json
from pandas.io.json import json_normalize
from pprint import pprint
from datetime import date
import os



class leauge():
    def __init__(self):
        self.lastLoadMatchday = None
    
    def saveLastLoadMatchday(self):
        ''' Save the lastLoadMatchday'''
        if(self.lastLoadMatchday[1] <=1):
            lastLoadMatchday = [self.lastLoadMatchday[0]-1, 34]
        else:
            lastLoadMatchday = [self.lastLoadMatchday[0],self.lastLoadMatchday[1]-1]
        with open('info.json', 'w') as file:
            file.write(json.dumps({'LastLoadMatchday': lastLoadMatchday}))
            
    def readLastLoadMatchday(self):
        '''Read the last lastLoadMatchday '''
        with open('info.json') as file:
            dataLoaded = json.load(file)
        return dataLoaded['LastLoadMatchday']
    
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
            self.saveLastLoadMatchday()
            self.loadRek()
            return 0
        
    def getUpdate(self):
        ''' Load all data to the newest one.
            First of all, it looks if there is a file with the 
            information from the last load Matchday. If doesn't
            it load the files from the first day it knew.
        '''
        if(self.lastLoadMatchday == None):
            if(os.path.isfile('info.json') == True):
                self.lastLoadMatchday = self.readLastLoadMatchday()
            else:
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

