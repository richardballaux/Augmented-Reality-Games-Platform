# Augmented Reality Games Platform Using Computer Vision
## @Authors: Richard Ballaux, Viktor Deturck, Leon Santen


## What this game is about
This game is a two-player game. Each player needs a controller in form of a colorful object that is being recognized by your computer's camera.
To select the settings, one of the two players needs to hover with their 'controller' over the corresponding setting they are trying to change. After having selected all necessary settings for the game and the game itself, the game starts automatically.

### Pong Game
Each player controls the height of their paddle with their controller by changing the height of the green object they are holding.

### Space Invaders
Currently, this game is not fully implemented and cannot be chosen via the menu. In the final version, you will be able to control the movement of the spaceship with your controller. 

## How to run and install
This game is meant to be run on a linux system.

### Install OpenCV  on linux
```
$ conda update anaconda-navigator
$ conda update navigator-updater
$ pip install opencv-python
```
### Run Game
Run game via the terminal. Navigate to the folder the game file is located in.
Run the following command:
```
$ python argame.py
```
_or_
```
$ python3 argame.py
```

## Final Write-Up
You can find the final write-up PDF document in this folder. It is called "Final Write Up - Augmented Reality Pong Game" and includes a detailed description of implementation and the project idea.
