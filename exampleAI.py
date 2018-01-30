# You need to import colorfight for all the APIs
import colorfight
import random

if __name__ == '__main__':
    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit. 
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    if g.JoinGame('MyAI'):
        # Put you logic in a while True loop so it will run forever until you 
        # manually stop the game
        while True:
            # Use a nested for loop to iterate through the cells on the map
            for x in range(g.width):
                for y in range(g.height):
                    # Get a cell
                    c = g.GetCell(x,y)
                    # If the cell I got is mine
                    if c.owner == g.uid:
                        if g.gold > 60:
                            g.BuildBase(x,y)
                        # Pick a random direction based on current cell 
                        d = random.choice([(0,1), (0,-1), (1, 0), (-1,0)])
                        # Get that adjacent cell
                        cc = g.GetCell(x+d[0], y+d[1])
                        # If that cell is valid(current cell + direction could be
                        # out of range) and that cell is not mine
                        if cc != None:
                            if cc.owner != g.uid:
                                # Attack the cell and print the result
                                # if (True, None, None) is printed, it means attack
                                # is successful, otherwise it will print the error
                                # code and error message
                                print(g.AttackCell(x+d[0], y+d[1]))
                                # Refresh the game, get updated game data
                                g.Refresh()
    else:
        print "Failed to join the game!"
