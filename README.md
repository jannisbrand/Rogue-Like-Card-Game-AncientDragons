# MANUAL
- Step 1: Clone
- Step 2: Go to the directory
- Step 3: Hit "launch_game.bat"

Controls are in ./Documents

To close the game.. Task Manager

# TODOs
- Scene state refactor:
    - Implement State-Pattern.
    - Think about a better callback structure. (Maybe seperate from the scene)
    - Implement the ability for the player to play multiple cards and apply effects.
    - Implement the ability for the player to end thier turn manually.

- Input subscribtion refactor:
    - Instead of (source, keys, mouse_buttons), create and pass an subscribtion object with all information.
    - Implement Buttons seperate Button press and release detection.
    - Implement subcribtion click once feature.

- Implement animation system:
    - IDEA: Classes that wrap around sprite classes and handle transoformations.
    - IDEA: Handle sprite transforms seperately.

- Implement more Interactibles
    - To visualize active effects.
    - Indicators. (I.e. showing where the card is allowed to be placed..)