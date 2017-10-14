#ColorFight!

ColorFight is a game where you try to occupy as many cells as possible on the map.

##Rules

* When you join the game, you will be given a random cell as a start.

* You can only attack the cell that's adjacent to your occupied cells.

* You can only attack one cell at a time. During that time, you are not able to attack other cells.

* The time you need to occupy a cell is based on the last time when the cell is occupied. The longer the time is, the easier it would be to be attacked. The minimum time to occupy a cell is 2s.

* You can attack your own cell to refresh the occupy time, but it would take the same amount of time as other players attacking it.

## API

The module provided some API for the game. You are welcome to add your own API, even directly talk to the server with HTTP requests if you want.

`Game` is the main class for the API. You should instantiate an object for it like `g = Game()`.

After that, you can do the following actions:

* `JoinGame(name)` will let you join the game with a name. ex. `g.JoinGame('MyAI')`. Notice the API is already optimized so when you try to join the game with the same name on the same computer(with the generated token file), it will not generate a user. You can continue to play the game as the user before.

* `Refresh()` will get the current game data from the server. ex. `g.Refresh()`. This function will store the raw data into `self.data` which you can access if you want. Also this function will fill in `self.width` and `self.height` for the game, as well as `self.currTime` for the time of this information.

* `GetCell(x,y)` is a easy way to access the data of one cell. ex. `g.GetCell(1,2)`. The function will return a `Cell` object which has all the data of a single cell at (x,y). If the pair (x,y) given is invalid, it will return `None`

* `AttackCell(x,y)`is the only action you need to play the game. ex. `g.AttackCell(2,2)`. It will try to attack the cell you specified. Returning `True` means the action is successful. Otherwise it will return a tuple `(False, err_msg)` where `err_msg` will contain the reason it failed.

##Cell Data

* `owner`: who owns this cell now. It's a user id.

* `attacker`: who is attacking this cell now. Invalid if `isTaking` is `False`

* `isTaking`: is this cell being attacked. If it's `True` then you can't attack it.

* `x`: x coordinate

* `y`: y coordinate

* `occupyTime`: when is this cell occupied. Server side time in seconds.

* `attackTime`: when is this cell attacked. Invalid if `isTaking` is `False`

* `takeTime`: how long it would take if you attack this cell

* `finishTime`: when will the attack finish. Invalid if `isTaking` is `False`
