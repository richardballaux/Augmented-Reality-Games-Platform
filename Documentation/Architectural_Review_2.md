# Augmented Reality Games Platform

Richard Ballaux<br/>
Viktor Deturck<br/>
Leon Santen<br/>
## Background And Context
The goal of this software is to provide several small games that are controlled by computer vision. The controllers can be colored objects that are being recognized by the computer’s camera. With the controller, the players can navigate through the menu and play all available games. For the object recognition, we are using OpenCV. <br/>

We are trying to have at least two games in total. We also want the object recognition for the controller to work better. Furthermore, keeping track of a local high score or even a high score saved in a databank online is one of our main goals. In the current state, our GUI consists of basic geometrical shapes with one color. Substituting these shapes and buttons with more interesting pictures and giving the game a specific style is another action item. <br/>

Besides all these tangible goals, the performance of our code is very low at the moment. We are worried about the structure of our while loops, and our update functions seem to work very uneffectively. <br/>

## Key Questions
Are nested loops the way to go, with one general arbiter that defines the game/menu and one arbiter to define the states in the game. While in one state, using a while loop to stay in that state until something happens. <br/><br/>

How to shoot in space invaders. We need to find a way to shoot in the space invaders game. We don’t know if the player should use their second controller to shoot or move their one controller in a certain way that the game recognizes it as shooting.<br/><br/>

Preventing windows from popping up. Since we have several files and loops, for a new game a new window pops up at the moment. Ideally, we want the game to stay in one window. In addition, we ran into the problem of not being able to close the window. Is there a way to force to close a window?<br/><br/>

Should database be online or local? We do not know if it is feasible to create a well working online database connection. We would appreciate tips if anyone has experience with online databases.<br/><br/>

How to check if the cursor is working after you set the color. <br/><br/>

We would need to know how to rescale pictures in the window so they all fit on the screen. <br/><br/>
## Agenda For Technical Review Session
- Go over architectural changes and bring audience up to date <br/>
- Show difficulties regarding:<br/>
          a - running the code<br/>
          b - architecture: nested loops are becoming complicated<br/>
          c - calling code from different files<br/>
- Go over crucial to-do’s:<br/>
          a - high score still needs to be implemented<br/>
          b - polishing graphics and GUI<br/>
- Interactive ideation <br/>




## Links for Presentation
[Link](https://docs.google.com/presentation/d/11C4przxhQGoBpjT3DJMFUIvVmDSv7QRJcwKs1btrSR4/edit?usp=sharing) to GoogleSlides. <br/>

[Link](https://docs.google.com/forms/d/e/1FAIpQLScHnsqMLcOjPnrN3jl7qrlDSOzroM-_KjyQL16N_ipS9nfDew/viewform?usp=sf_link) to the feedback form. <br/>
