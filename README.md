# Sand Simulation 2

**WORK IN PROGRESS**
## Who am I
I am Johnathan Bill, a recent Graduate from West Virginia University Institute of Technology with a Bachelor's of Science in Information Systems and a minor in Computer Science. I am aspiring Software Engineer and Web Developer and love to challenge myself with new and interesting projects. 

## Why Sand Simulation
I always found physics in video games interesting especially in games like <a href="https://dan-ball.jp/en/javagame/dust/" target="_blank">Dust</a> where objects interact with each other in such a way that it become life like while being able to remain rather simple. I wanted to challenge myself and create a sand simulation with a variety of systems using new technology (pygame) with little to no guidance.


## Future Additions
- Fire
- Heat
- Mossisfication speed
## Current Issues
- Optimization Issues
    - The (without altering settings) simulation handles upto physics particles (non-void particles) 14400 (determined by screen size and pixel size in game.py) particles. This is a lot of particles, which can cause slow downs once the screen is full of them.
## Recent Changes
- Added Hud
- Added Particle Inspection
- Added Moss
- Updated entire physics engine so it is more optimal
    - Update fixed overlapping issue, pushing issues, and non existent particles issue
- added oil to simulate liquid densities (Water will follow the same rules in oil as sand does in water)
- Added gas density simulation (Steam will rise through smoke)
## How to Use
1. **Clone the repository to your local machine.**
    ```bash
    git clone https://github.com/username/SandSimulation2.git
    ```

2. **Navigate to the project directory.**
    ```bash
    cd SandSimulation2
    ```

3. **Run the simulation.**
    ```bash
    python main.py
    ```

## Dependencies
- Python 3.6 or higher
- [Pygame](https://www.pygame.org/)

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to the branch.
5. Create a pull request.

## Known Issues
- For a more detailed list of known issues, please refer to the [issues](https://github.com/username/SandSimulation2/issues) section.

## Future Plans
I am actively working on addressing the current issues and implementing new features. Feel free to contribute by submitting bug reports, feature requests, or code contributions.


**Note:** Please be aware that this project is a work in progress, and contributions are welcome. Keep an eye on updates for improvements and new features.
