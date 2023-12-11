# Project: Degrees

## Concept & Background

Write a program that determines how may `degrees of separation` apart two actors are.
Implement [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon).

### Frame as a search problem

- state: people.
- action: movies; take us from one actor to another
- initial state and goal state: defined by the two people we’re trying to connect

By using breadth-first search, we can find the shortest path from one actor to another.

### Terms

`CSV file`: way of organizing data in a text-based format
- each row corresponds to one data entry
- with commas in the row separating the values for that entry

## Required

Complete the implementation of the `shortest_path` function such that it returns the shortest path from the person with id `source` to the person with the id `target`.

- Return a list that each item is the next `(movie_id, person_id)` pair; should be a tuple of two strings.
- If there are multiple paths of minimum length from the source to the target, your function can return any of them.
- If there is no possible path between two actors, your function should return `None`.
- Should not modify anything else in the file other than the `shortest_path function`, though you may write additional functions and/or import other Python standard library modules.
