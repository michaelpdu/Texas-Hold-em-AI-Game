# Texas-Hold-em-AI-Game

## Texas Hold'em AI Platform

[http://poker-dev.wrs.club:3001/index.html](http://poker-dev.wrs.club:3001/index.html)

## Process

Create Game --> Table number is 9090 --> confirm

## Features

There are 4 models for this game: model_for_hands, model_for_board3, model_for_board4 and model_for_board5.

Feature list:

- 1-52: hand cards and board cards
- 53: same suit in hand cards
- 54: same rank in hand cards
- 55: rank_1/13
- 56: rank_2/13
- 57: (abs gap of rank)/12
- 58: call rate
- 59: rank of hand cards
- 100: rank percentage in board3
- 101: rank percentage in board4
- 101: rank percentage in board5
- 110: max gap (between hand and board) in board4 / 2000
- 111: gap (between hand and board) in board5 / 2000

In these model, we use XGBoost build machine learning model and make action in the game.


## Training Process

Please refer to training process in PySIE: 
[https://github.com/michaelpdu/pysie/tree/dev/machine_learning/training_process](https://github.com/michaelpdu/pysie/tree/dev/machine_learning/training_process)



