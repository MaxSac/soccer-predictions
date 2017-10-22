
# coding: utf-8

# # First Test

# In[1]:

from urllib.request import urlopen, Request
import json
from pandas.io.json import json_normalize
import os
import datetime


class downloader():
    def __init__(self):
        self.firstEntryYear = 2013
        self.firstEntryDay = 1
        self.lastLoadMatchday = None
        
    def beginHistory(self):
        '''Beginn der Datenbank'''
        return [self.firstEntryYear, self.firstEntryDay]
    
    def writeInfo(self, info=None):
        '''Save information as a Dict in a .txt file'''
        with open('info.txt', 'w') as outfile:  
            json.dump(info, outfile)
    
    def loadInfo(self):
        '''load info.txt file, if not exist return none'''
        if(os.path.isfile('./info.txt')==True):
            with open('info.txt') as json_file:  
                data = json.load(json_file)
            return data
        else:
            return {'createdOn': 2017}
    
    def updateInfo(self, newInfo):
        '''load the information from the file and add/replace new one.'''
        info = self.loadInfo()
        for x in newInfo.keys():
            info[x] = newInfo[x]
        self.writeInfo(info)
        
    def readLastLoadMatchday(self):
        '''read the last load matchday in the info.txt file, if not exist
        set the actuell matchday to the first one.'''
        info = self.loadInfo()
        if('lastLoadMatchday' in info):
            self.lastLoadMatchday = info['lastLoadMatchday']
        else:
            self.lastLoadMatchday = self.beginHistory()
            self.updateInfo({'lastLoadMatchday': self.lastLoadMatchday})
        return self.lastLoadMatchday
    
    def saveLastLoadMatchday(self):
        '''update the last load matchday from info.txt file'''
        self.updateInfo({'lastLoadMatchday': self.lastLoadMatchday})
    
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
        self.readLastLoadMatchday()
        self.downloadMatchDay(self.lastLoadMatchday[0], self.lastLoadMatchday[1])
        self.loadRek()


# In[2]:

# downloader().getUpdate()


# In[ ]:



