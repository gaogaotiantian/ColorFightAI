import colorfight
import random

if __name__ == '__main__':
    g = colorfight.Game()
    g.JoinGame('MyAI')

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
