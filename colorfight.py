import requests
import json
import os
import random

hostUrl   = 'https://colorfight.herokuapp.com/'

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
        self.Refresh()
        self.token = ''
        self.name  = ''
        self.uid   = -1

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
    
        headers = {'content-type': 'application/json'}
        r = requests.post(hostUrl + 'joingame', data=json.dumps({'name':name}), headers = headers)
        data = r.json()
        with open('token', 'w') as f:
            f.write(data['token'] + '\n')
        self.token = data['token']
        self.uid   = data['uid']

        return True

    def AttackCell(self, x, y):
        if self.token != '':
            headers = {'content-type': 'application/json'}
            r = requests.post(hostUrl + 'attack', data=json.dumps({'cellx':x, 'celly':y, 'token':self.token}), headers = headers)
            if r.status_code == 200:
                data = r.json()
                if data['err_code'] == 0:
                    print "attack success on ({}, {})".format(x,y)
                    return True
                else:
                    print data['err_msg']
        else:
            print "You need to join the game first!"
        return False, data['err_code']

    def GetCell(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            c = Cell(self.data['cells'][x+y*self.width])
            return c
        return None
    def Refresh(self):
        r = requests.get(hostUrl + 'getgameinfo')
        self.data = r.json()
        self.width = self.data['info']['width']
        self.height = self.data['info']['height']
        self.currTime = self.data['info']['time']

if __name__ == '__main__':
    g = Game()
    g.JoinGame('gaotiantian')
    while True:
        for x in range(g.width):
            for y in range(g.height):
                c = g.GetCell(x,y)
                if c.owner == g.uid:
                    d = random.choice([(0,1), (0,-1), (1, 0), (-1,0)])
                    cc = g.GetCell(x+d[0], y+d[1])
                    if cc != None:
                        if cc.owner != g.uid:
                            g.AttackCell(x+d[0], y+d[1])
                            g.Refresh()
    print dir(c)

