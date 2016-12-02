# pygame-testground
SI 206 Project 4 Repository

I was assigned to create a game using the pygame module, with the requirements:
  - Include movement, collision detection, scoring or time, animation, and sound.
  - Have a unique implementation of class inheritance.
  - Present the game to the class.
  
Things to know before playing:
  - You will need to have the pygame library installed.
  - You will need to have a gamepad / controller. Was tested with an xbox 360 controller, compatiblity not guranteed.

Some notes:
  - Understanding the joystick functioanlity and implementing it was the biggest hurdle of this project.
  - I intially tried nested looping through standard lists and using the colliderect function, but this proved 
    too expensive.
      - Creating groups to section out the kinds of collisions, and letting the groupcollide function handle removing destroyed enemies
        seems to be much more efficient.
        
Rights Statement:
  - All are free to use this game, the code within, and the assests within at their own risk, so long as I am referenced.
