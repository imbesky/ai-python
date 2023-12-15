# Project: Tic-Tac-Toe

## Newly-Made-Functions

### blank_of(board)

- returns the number of cells which value is `EMPTY`
- used at `player()`, `terminal()`, `minimax()`

### winnable_actions_of(board)

- return the actions that lead the current player to winning in this turn

### not_losable_actions_of(board)

- return the actions that does not lead the opponent of current player to winning next turn

## Judgement

The goal of playing game is to win, at least draw = avoid losing.

### actions of player and opponent

Player should suppose that the actions of opponent will due to the goal;
- win
- at least draw = avoid losing

So in `minimax()`, the actions that can lead opponent to winning in the next turn will not be accepted to the frontier, using `not_losable_actions_of(board)`

### optimal action

Returned action of `minimax()` should lead the player to winning, at least draw.
For this goal, it follows sequence like this;

#### 1. search to find the most reasonable action to win

```
    # to win
    for action in root_actions:
        if ((winnable_actions[action][0] < losable_actions[action][0]
             or losable_actions[action][0] == 0)
                and winnable_actions[action][1] > max_count != 0):
            max_count = winnable_actions[action][1]
            optimal_action = action
```

- using `while` loop in `minimax()`, find the root actions that can lead player to win
- save their `minimum value of required moves to win` and `counts` at dictionary structure
- choose the actions
  - it should have fewer moves than the `minimum value of required moves to lose` originated from the same root action
  - or there are no case of losing originated from the same root action
  - it should have the maximum value of counts among the actions that satisfy the conditions above

#### 2. if there are no way to win, search to find the most reasonable action to draw
```
    # to draw
    if optimal_action is None:
        max_count = 0
        for action in root_actions:
            if ((drawable_actions[action][0] < losable_actions[action][0]
                 or losable_actions[action][0] == 0)
                    and drawable_actions[action][1] > max_count != 0):
                max_count = drawable_actions[action][1]
                optimal_action = action
```

- using `while` loop in `minimax()`, find the root actions that can lead player to draw(tie)
- save their `minimum value of required moves to draw` and `counts` at dictionary structure
- choose the actions
  - it should have fewer moves than the `minimum value of required moves to lose` originated from the same root action
  - or there are no case of losing originated from the same root action
  - it should have the maximum value of counts among the actions that satisfy the conditions above

#### 3. if there are no way to win or draw, return random action

```
    # there is no way to win
    if optimal_action is None:
        try:
            optimal_action = root_actions.pop()
        except KeyError:
            optimal_action = actions(board).pop()
```