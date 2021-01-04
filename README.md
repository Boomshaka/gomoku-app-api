# gomoku-app-api
Gomoku app api source code

This is a backend Django REST API for playing the traditional Japanese game Gomoku (Connect Five) against an AI that implements [Minixmax Algorithm](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/) and [Alpha Beta Pruning](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/).

METHODS
========

### POST base_url/game/
#### Create a new game
Request Example:
http://localhost:8000/game/
	
| Method | URL Parameter | Request Payload | Response Body   |
|--------|---------------|-----------------|-----------------|
|  POST  | None          | Empty           | game json object|
	
Response Example:
  ```json
  {"id":"74371eb5-2529-43ba-97a8-0ea6e1046e58",
  "grid":[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  "winner":0,
  "status":"Started",
  "date":"2021-01-04T03:03:27.233112Z"}
  ```

### GET base_url/game/{uuid:id}
#### Get a game
Request Example:
http://localhost:8000/game/74371eb5-2529-43ba-97a8-0ea6e1046e58/

| Method | URL Parameter | Request Payload | Response Body   |
|--------|---------------|-----------------|-----------------|
|  GET   |      id       | Empty           | game json object|

Response Example:
  ```json
  {"id":"74371eb5-2529-43ba-97a8-0ea6e1046e58",
  "grid":[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  "winner":0,
  "status":"Started",
  "date":"2021-01-04T03:03:27.233112Z"}  
  ```
  
  ### POST base_url/game/{uuid:id}
  #### Make a move
  Request Example:
  http://localhost:8000/game/74371eb5-2529-43ba-97a8-0ea6e1046e58/

| Method | URL Parameter | Request Payload | Response Body   |
|--------|---------------|-----------------|-----------------|
|  POST  |      id       | row, col        | game json object|

