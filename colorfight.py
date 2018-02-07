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
        self.cellType   = cellData['ct']
        self.buildType  = cellData['b']
        self.isBase     = cellData['b'] == "base"
        self.isBuilding = cellData['bf'] == False
        self.buildTime  = cellData['bt']

    def __repr__(self):
        s = ""
        s += "({x}, {y}), owner is {owner}\n".format(x = self.x, y = self.y, owner = self.owner)
        if self.isTaking:
            s += "Cell is being attacked\n"
            s += "Attacker is {attacker}\n".format(attacker = self.attacker)
            s += "Attack time is {atkTime}\n".format(atkTime = self.attackTime)
            s += "Finish time is {finishTime}\n".format(finishTime = self.finishTime)
        else:
            s += "Cell is not being attacked\n"
            s += "Cell is occupied at {occupyTime}\n".format(occupyTime = self.occupyTime)
            s += "Take time is {takeTime}\n".format(takeTime = self.takeTime)
        return s

class User:
    def __init__(self, userData):
        self.id            = userData['id']
        self.name          = userData['name']
        self.cdTime        = userData['cd_time']
        self.cellNum       = userData['cell_num']
        self.baseNum       = userData['base_num']
        self.goldCellNum   = userData['gold_cell_num']
        self.energyCellNum = userData['energy_cell_num']
        if 'energy' in userData:
            self.energy = userData['energy']
        if 'gold' in userData:
            self.gold = userData['gold']
    
    def __repr__(self):
        return "uid: {}\nname: {}\ncd time: {}\ncell number: {}\n".format(self.id, self.name, self.cdTime, self.cellNum)

class Game:
    def __init__(self):
        self.data = None
        self.token = ''
        self.name  = ''
        self.uid   = -1
        self.endTime = 0
        self.users = []
        self.cellNum = 0
        self.baseNum = 0
        self.goldCellNum = 0
        self.energyCellNum = 0
        self.cdTime = 0
        self.energy = 0
        self.gold = 0
        self.gameVersion = ''
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

    def AttackCell(self, x, y, boost = False):
        if self.token != '':
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'attack', data=json.dumps({'cellx':x, 'celly':y, 'boost': boost, 'token':self.token}), headers = headers)
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

    def BuildBase(self, x, y):
        if self.token != '':
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'buildbase', data=json.dumps({'cellx':x, 'celly':y, 'token':self.token}), headers = headers)
            if r.status_code == 200:
                data = r.json()
                if data['err_code'] == 0:
                    return True, None, None
                else:
                    return False, data['err_code'], data['err_msg']
            else:
                return False, None, "Server did not return correctly, status_code ", r.status_code
        else:
            return False, None, "You need to join the game first!"
    
    def Blast(self, x, y, direction, blastType):
        if self.token != '':
            if direction not in ["square", "vertical", "horizontal"]:
                return False, None, "Wrong direction!"
            if blastType not in ["attack", "defense"]:
                return False, None, "Wrong blast type!"
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'blast', data=json.dumps({'cellx':x, 'celly':y, 'token':self.token, 'direction':direction, 'blastType':blastType}), headers = headers)
            if r.status_code == 200:
                data = r.json()
                if data['err_code'] == 0:
                    return True, None, None
                else:
                    return False, data['err_code'], data['err_msg']
            else:
                return False, None, "Server did not return correctly, status_code ", r.status_code
        else:
            return False, None, "You need to join the game first!"

    def GetCell(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            c = Cell(self.data['cells'][x+y*self.width])
            return c
        return None
    def GetTakeTimeEq(self, timeDiff):
        if timeDiff <= 0:
            return 33
        return 30*(2**(-timeDiff/30.0))+3
    def RefreshUsers(self, usersData):
        self.users = []
        for userData in usersData:
            u = User(userData)
            self.users.append(u)
            if u.id == self.uid:
                self.gold   = u.gold
                self.energy = u.energy
                self.cdTime = u.cdTime
                self.cellNum = u.cellNum
                self.baseNum = u.baseNum
                self.goldCellNum = u.goldCellNum
                self.energyCellNum = u.energyCellNum
        self.users.sort(key = lambda x: x.cellNum, reverse = True)
    def Refresh(self):
        headers = {'content-type': 'application/json'}
        if self.data == None:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":2}), headers = headers)
            if r.status_code == 200:
                self.data = r.json()
                self.width = self.data['info']['width']
                self.height = self.data['info']['height']
                self.currTime = self.data['info']['time']
                self.endTime = self.data['info']['end_time']
                self.lastUpdate = self.currTime
                self.RefreshUsers(self.data['users'])
            else:
                return False
        else:
            r = requests.post(hostUrl + 'getgameinfo', data=json.dumps({"protocol":1, "timeAfter":self.lastUpdate}), headers = headers)
            if r.status_code == 200:
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
            else:
                return False
        return True


