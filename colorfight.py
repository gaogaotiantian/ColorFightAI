import requests
import json
import os
import random

hostUrl   = 'https://colorfight.herokuapp.com/'
#hostUrl   = 'http://localhost:8000/'

def CheckToken(token):
    headers = {'content-type': 'application/json'}
    r = requests.post(hostUrl + 'checktoken', data=json.dumps({'token':token}), headers = headers)
    if r.status_code == 200:
        return r.json()
    return None

class Cell:
    def __init__(self, cellData):
        self.owner      = cellData['o']
        self.attacker   = cellData['a']
        self.isTaking   = cellData['c'] == 1
        self.x          = cellData['x']
        self.y          = cellData['y']
        self.occupyTime = cellData['ot']
        self.attackTime = cellData['at']
        self.takeTime   = cellData['t']
        self.finishTime = cellData['f']

class Game:
    def __init__(self):
        self.data = None
        self.token = ''
        self.name  = ''
        self.uid   = -1
        self.Refresh()

    def JoinGame(self, name, force = False):
        if force == False and os.path.isfile('token'):
            with open('token') as f:
                self.token = f.readline().strip()
                data = CheckToken(self.token)
                if data != None:
                    if name == data['name']:
                        self.name = data['name']
                        self.uid  = data['uid']
                        return True
                else:
                    return False
    
        headers = {'content-type': 'application/json'}
        r = requests.post(hostUrl + 'joingame', data=json.dumps({'name':name}), headers = headers)
        data = r.json()
        with open('token', 'w') as f:
            f.write(data['token'] + '\n')
        self.token = data['token']
        self.uid   = data['uid']
        self.Refresh()

        return True

    def AttackCell(self, x, y):
        if self.token != '':
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'attack', data=json.dumps({'cellx':x, 'celly':y, 'token':self.token}), headers = headers)
            if r.status_code == 200:
                data = r.json()
                if data['err_code'] == 0:
                    return True
            else:
                print r
        else:
            print "You need to join the game first!"
            return False, None
        return False, data['err_msg']

    def GetCell(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            c = Cell(self.data['cells'][x+y*self.width])
            return c
        return None
    def GetTakeTimeEq(self, timeDiff):
        if timeDiff <= 0:
            return 200
        return 20*(2**(-timeDiff/20))+2
    def Refresh(self):
        headers = {'content-type': 'application/json'}
        if self.data == None:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":1}), headers = headers)
            if r.status_code == 200:
                self.data = r.json()
                self.width = self.data['info']['width']
                self.height = self.data['info']['height']
                self.currTime = self.data['info']['time']
                self.lastUpdate = self.currTime
        else:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":1, "timeAfter":self.lastUpdate}), headers = headers)
            d = r.json()
            self.width = d['info']['width']
            self.height = d['info']['height']
            self.currTime = d['info']['time']
            self.lastUpdate = self.currTime
            for c in d['cells']:
                cid = c['x'] + c['y']*self.width
                self.data['cells'][cid] = c
            for cell in self.data['cells']:
                if cell['c'] == 1:
                    cell['t'] = -1
                else:
                    if cell['o'] == 0:
                        cell['t'] = 1;
                    else:
                        cell['t'] = self.GetTakeTimeEq(self.currTime - cell['ot'])


