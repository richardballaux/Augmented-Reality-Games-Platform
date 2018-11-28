# Reflection And Synthesis
Richard Ballaux<br/>
Viktor Deturck <br/>
Leon Santen <br/>

## Feedback And Decisions
_“ Based upon your notes from the technical review, synthesize the feedback you received addressing your key questions. How do you plan to incorporate it going forward? What new questions did you generate?”_<br/> 

We received feedback via some smaller group discussions in class and through an online survey with more technical questions. As we are in a relatively far developed state with our project, it wouldn’t make sense to ask very technical questions. Instead we decided to focus on some user design aspects in our platform for this design review. 

### How would you want to shoot with a controller in a space invaders game?

Ideas included:<br/>
- When the controller crosses a horizontal line, the player shoots.
- One controller for moving, a second controller (potentially different color) for shooting
- A “signal color” in one hand. The camera recognizes the color in your hand. When you open your hand it triggers shooting

Most people liked the crossing over a horizontal line to shoot, as this would be the easiest. There were, however, some concerns that people just would shoot the whole time by permanently holding the controller above the line, so we would have to address this. One possible way of doing this is by setting a time limit, so it would stop shooting after a defined time. Another way is limited ammo (which could be slowly refilling) so people are able to decide themselves how long they want to keep on shooting. 

The other ideas were less popular and also a bit more cumbersome as it would require extra effort. Either setting up a second controller and looking at two controllers at the same time on the screen, or having to paint something on your hand (or cover you controller with your hand, which would also maybe mess with our color recognition) seems a bit counterintuitive.


### How to check if the cursor is working after you set your color? 
Ideas included:<br/>
- Player has to hover over two boxes within 20 seconds. If the player cannot activate the two boxes, the color recognition will reset automatically.
- Maze that the player has to go through to proof that their controller is working
- Include tips on what color to choose and where to play the game (background)

By talking about this issue in depth with our classmates, we realized that it is very crucial to implement a color check. The game would not be playable otherwise. Furthermore, we learned that we should probably include instructions on how to choose a controller and what to consider for playing the game in general. 
## Review Process Reflection
_“How did the review go? Did you get answers to your key questions? Did you provide too much/too little context for your audience? Did you stick closely to your planned agenda, or did you discover new things during the discussion that made you change your plans? What could you do next time to have an even more effective technical review?”_<br/>

In our opinion, the second design review was very effective. We knew that it would be difficult to ask technically complex questions in class. Therefore, we decided to ask technical questions on the online feedback form and use the group phase for creativity based questions. We received valuable feedback in class and in our survey. Since this architectural review was useful to us, we think that we used our time effectively.<br/>

The presentation itself could have been a little bit more structured. Considering that the audience knew our project and had listened to two presentations about the same game project already, the amount of provided information about our games was appropriate.<br/>

 
