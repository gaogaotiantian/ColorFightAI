# ColorFight!

ColorFight is a game where you try to occupy as many cells as possible on the map.

## Rules

* When you join the game, you will be given a random cell as a start.

* You can only attack the cell that's adjacent to your occupied cells.

* You can only attack one cell at a time. During that time, you are not able to attack other cells.

* The time you need to occupy a cell is based on the last time when the cell is occupied. The longer the time is, the easier it would be to be attacked. The minimum time to occupy a cell is 2s. (The equation of the time to occupy is ```2 + 20 * (2 ^ (-x/20))```. So when it's just occupied, it takes 22s to attack it. After 20s, it becomes 12s. After around 55s, it becomes 5s). If the cell is surrounded by more than 1 attacker's occupied cell, the time to take it is decreased. One extra adjacent cell takes off 0.5s to take the cell.

* You can attack your own cell to refresh the occupy time, but it would take the same amount of time as other players attacking it.

* Golden cells worth 5 times as normal cells.

## How To Start

* First clone the git repository. `git clone https://github.com/gaogaotiantian/ColorFightAI.git`

* Then you can run the exampleAI by `python exampleAI.py`

* If your computer complains about `requests` module, try `pip install requests[security]` or `sudo pip install requests[security]` if it complains about privilege. 

* Or you can use python3 by `python3 exampleAI.py`. The library and the exampleAI support both python2 and python3. 

* You can watch the result here [https://colorfight.herokuapp.com/](https://colorfight.herokuapp.com)

## API

The module provided some API for the game. You are welcome to add your own API, even directly talk to the server with HTTP requests if you want.

`Game` is the main class for the API. You should instantiate an object for it like `g = Game()`.

### After that, you can do the following actions:

* `JoinGame(name)` will let you join the game with a name. ex. `g.JoinGame('MyAI')`. Notice the API is already optimized so when you try to join the game with the same name on the same computer(with the generated token file), it will not generate a user. You can continue to play the game as the user before. `name` has to be a `str`.

* `Refresh()` will get the current game data from the server. ex. `g.Refresh()`. This function will store the raw data into `self.data` which you can access if you want. Also this function will fill in `self.width` and `self.height` for the game, as well as `self.currTime` for the time of this information. For game that has a end time, `self.endTime` will be updated, otherwise it will be `0`.

* `GetCell(x,y)` is a easy way to access the data of one cell. ex. `g.GetCell(1,2)`. The function will return a `Cell` object which has all the data of a single cell at (x,y). If the pair (x,y) given is invalid, it will return `None`. x and y starts with `0`, and the maximum value is `g.width-1`, `g.height-1`, respectively.

* `AttackCell(x,y)`is the only action you need to play the game. ex. `g.AttackCell(2,2)`. It will try to attack the cell you specified. The return value will be a tuple with 3 items. Returning `(True, None, None)` means the action is successful. Otherwise it will return a tuple `(False, err_code, err_msg)` where `err_code` will contain the error code from the server and `err_msg` will contain the reason it failed.

### You also have the following data in `Game`:

* `uid` contains your user id. That's the unique identification for you.

* `endTime` is the time when the current game will end. If it's `0`, it's unlimited time game. This is a timestamp from the server.

* `width` and `height` contains the width and height of the current game.

* `currTime` is the current time of the current data from the server. This is a timestamp from the server.

* `users` is a list of `User` object which has all the user info.

* `cdTime` is your cd time

* `cellNum` is your cell number

## Cell Data

* `owner`: who owns this cell now. It's a user id.

* `attacker`: who is attacking this cell now. Invalid if `isTaking` is `False`.

* `isTaking`: is this cell being attacked. If it's `True` then you can't attack it.

* `x`: x coordinate.

* `y`: y coordinate.

* `occupyTime`: when is this cell occupied. Server side time in seconds. This is a timestamp from the server.

* `attackTime`: when is this cell attacked. Invalid if `isTaking` is `False`. This is a timestamp from the server.

* `takeTime`: how long it would take if you attack this cell. This is a number of seconds.

* `finishTime`: when will the attack finish. Invalid if `isTaking` is `False`. This is a timestamp from the server.

* `cellType`: `'gold'` if it's golden cell and `'normal'` if it's a normal cell.`

## User Data

* `id`: unique user identification.

* `name`: user name.

* `cdTime`: when can this user attack again. This is a timestamp from the server.

* `cellNum`: how many cells does this user occupy.

## Error Code from AttackCell()

* 0: Success.

* 1: The cell you attack is invalid. It could be that your input is out of the map, or the cell you attack is not adjacent to your occupied cells.

* 2: The cell you attack is being taken by another player.

* 3: You are in CD time. You can't attack any cell now.

* 4: The game already ends
