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

class User:
    def __init__(self, userData):
        self.id         = userData['id']
        self.name       = userData['name']
        self.cdTime     = userData['cd_time']
        self.cellNum    = userData['cell_num']

class Game:
    def __init__(self):
        self.data = None
        self.token = ''
        self.name  = ''
        self.uid   = -1
        self.endTime = 0
        self.users = []
        self.Refresh()

    def JoinGame(self, name, password = None, force = False):
        if type(name) != str:
            print("Your name has to be a string!")
            return False
        if force == False and os.path.isfile('token'):
            with open('token') as f:
                self.token = f.readline().strip()
                data = CheckToken(self.token)
                if data != None:
                    if name == data['name']:
                        self.name = data['name']
                        self.uid  = data['uid']
                        return True
    
        headers = {'content-type': 'application/json'}
        data = {'name':name}
        if password != None:
            data['password'] = password
        r = requests.post(hostUrl + 'joingame', data=json.dumps(data), headers = headers)
        if r.status_code == 200:
            data = r.json()
            with open('token', 'w') as f:
                f.write(data['token'] + '\n')
            self.token = data['token']
            self.uid   = data['uid']
            self.Refresh()
        else:
            return False

        return True

    def AttackCell(self, x, y):
        if self.token != '':
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'attack', data=json.dumps({'cellx':x, 'celly':y, 'token':self.token}), headers = headers)
            if r.status_code == 200:
                data = r.json()
                if data['err_code'] == 0:
                    return True, None, None
                else:
                    return False, data['err_code'], data['err_msg']
            else:
                return False, None, "Server did not return correctly"
        else:
            return False, None, "You need to join the game first!"


    def GetCell(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            c = Cell(self.data['cells'][x+y*self.width])
            return c
        return None
    def GetTakeTimeEq(self, timeDiff):
        if timeDiff <= 0:
            return 200
        return 20*(2**(-timeDiff/20))+2
    def RefreshUsers(self, usersData):
        self.users = []
        for userData in usersData:
            self.users.append(User(userData))
    def Refresh(self):
        headers = {'content-type': 'application/json'}
        if self.data == None:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":1}), headers = headers)
            if r.status_code == 200:
                self.data = r.json()
                self.width = self.data['info']['width']
                self.height = self.data['info']['height']
                self.currTime = self.data['info']['time']
                self.endTime = self.data['info']['end_time']
                self.lastUpdate = self.currTime
                self.RefreshUsers(self.data['users'])
        else:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":1, "timeAfter":self.lastUpdate}), headers = headers)
            d = r.json()
            self.data['info'] = d['info']
            self.data['users'] = d['users']
            self.width = d['info']['width']
            self.height = d['info']['height']
            self.currTime = d['info']['time']
            self.endTime = self.data['info']['end_time']
            self.lastUpdate = self.currTime
            self.RefreshUsers(self.data['users'])
            for c in d['cells']:
                cid = c['x'] + c['y']*self.width
                self.data['cells'][cid] = c
            for cell in self.data['cells']:
                if cell['c'] == 1:
                    cell['t'] = -1
                else:
                    if cell['o'] == 0:
                        cell['t'] = 2;
                    else:
                        cell['t'] = self.GetTakeTimeEq(self.currTime - cell['ot'])


