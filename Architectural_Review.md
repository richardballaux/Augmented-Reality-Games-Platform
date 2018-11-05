# AR-Games Corp

Richard Ballaux<br/>
Viktor Deturck<br/>
Leon Santen<br/>

## Background And Context
The goal of this software is to provide several small games that are controlled by computer vision. The controllers can be colored objects that are being recognized by the computer’s camera. With the controller, the players can navigate through the menu and play all available games. For the object recognition, we are using OpenCV. <br/>

We are trying to have three games in total. At the moment, the only game that is fully working is a two-player pong game. The mirrored live video of the computer’s camera is the background of the game while the pong paddles and the ball are drawn on top of it. We want to keep the concept of having the live camera video in the background for all games. Currently, we are considering adding an augmented reality version of space invaders and fruit ninja. <br/>

Since the game provides a menu with several settings, the program needs to keep track of the changed settings and how the user is navigating through the menu. At the moment, we are using a class object as a state machine. Depending on the state of the state machine, the functions in the game execute different parts of the code.<br/>

## Key Questions

We are currently facing bigger design decisions regarding the over the architecture of our code.
**How should we organize the code for several games? Should we have a model class for every new game? Any other suggestions about how to divide up the code into different files and classes?**<br/>

For saving high scores, we are thinking about using already existing online databases. **Are there any databases that would serve our purpose well?**<br/>

We are running into problems with the performance of our code. The OpenCV image recognition is very calculation heavy and the camera live feed seems to lag too much considering the simple task of a camera live feed. **How can we reduce the complexity of object recognition? How can we reduce the complexity of streaming the camera feed?** <br/>

We were also thinking about if and how we can reuse some parts of the code and if it would make our code easier and better. For example, we will probably need to implement classes and functions like collision detection, wall objects,  the view model,... in more than one game/application. **How should we efficiently implement common functions over the different games and make the code less redundant?**<br/>

If we want to implement a high score system we need the user to be able to enter his name. **Is there an easy and fun way to use voice-recognition to input names or letters, or just as another fun input?**<br/>

For now, our project has a very simple GUI, because it doesn’t have a lot of functionality. In the future, we want to make an appealing menu. How would a good menu for an AR gaming platform look like?<br/>

## Agenda For Technical Review Session

- Background and context explanation
- What are we up to now
- Where do we want to go
- Open Discussion

## Feedback Form
We decided on asking lighter questions in the survey and saving technical questions for the in-class discussion.
This is the [feedback form](https://goo.gl/forms/HH9hExiRd4c8JpYF3) for after the presentation.
