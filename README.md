# Augmented Reality Games Platform Using Computer Vision
## @Authors: Richard Ballaux, Viktor Deturck, Leon Santen


## Our Games Platform
This program is a games platform that uses your camera so you can play our games with an object that you are holding in your hands. It uses computer vision, OpenCV, to track an object that you are using as the games controller. For your convenience, you can set the color of the controller-object yourself. 

At the moment, you can play two games on our platform: __Air Pong__ and __Space Invaders__

### Pong Game
Air Pong is a two-player game. Each player needs a controller in form of a colorful object that is being recognized by your computer's camera.
To select the settings, one of the two players needs to hover with their 'controller' over the corresponding setting they are trying to change. After having selected all necessary settings for the game and the game itself, the game starts automatically.

Each player controls the height of their paddle with their controller by changing the height of the green object they are holding.

### Space Invaders
This game is a one-player game and designed in the style of the well-known Space Invaders game. With your controller, you can change the horizontal postion of your spaceship in order to shoot your enemies, monsters. Hold your controller higher in order to move it above the right line and trigger your spaceship’s gun. There are also more instruction in the game. We hope you’ll survive the battle!

## How to run and install
This game is meant to be run on a linux system.

### Install OpenCV  on Linux
```
$ conda update anaconda-navigator
$ conda update navigator-updater
$ pip install opencv-python
```
### Run Game
Run game via the terminal. Navigate to the folder the game file is located in.
Run the following command:
```
$ python centralMain.py
```
_or_
```
$ python3 centralMain.py
```

## The Game Does Not Work Correctly?
Here are a few tips to ensure that your game is working correctly:
- Use a colorful controller. We highly recommend a __green controller__!
- Avoid lights or bright spots in the background.
- Choose a plain white wall as your background.
- __No shadows!__ Make sure that your controller's brightness doesn't change. Regardless of your controller's position, your controller should always look the same in the live video. 

## More Information on Our Website
Check out our website to find out about the coding process and our software design decisions. There are also more pictures if you are curious. 
Our website is right [here](https://sd18fall.github.io/Augmented-Reality-Games-Platform/#)!

## Our Platform! This Is What It Looks Like!
<a href="http://www.youtube.com/watch?feature=player_embedded&v=8q39Rc6IwFo
" target="_blank"><img src="http://img.youtube.com/vi/8q39Rc6IwFo/0.jpg" 
alt="COOL VIDEO" width="480" height="360" border="10" /></a>

