# Project: Tic-Tac-Toe

## Newly-Made-Functions

### blank_of(board)

- returns the number of cells which value is `EMPTY`
- used at `player()`, `terminal()`, `minimax()`

### accept_action(target_player, board, action)

- returns the board according to the given argument of target player, board and action
- make a deep copy of `board` to avoid modifying `board`
- raise exception if the point of action is not `EMPTY`

### switch_player(current_player)

- returns the next player according to the current player
- ex: return X if current player is O
