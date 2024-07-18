# Sand Simulation 2

**WORK IN PROGRESS**
## Who am I
I am Johnathan Bill, a Software Engineer from West Virginia and aspiring web / full stack developer. I enjoy creating interesting projects that not only challenge myself but also showcase my skillset with the my field of work.

## Why Sand Simulation
I always found physics in video games interesting especially in games like <a href="https://dan-ball.jp/en/javagame/dust/" target="_blank">Dust</a> where objects interact with each other in such a way that it become life like while being able to remain rather simple. I wanted to challenge myself and create a sand simulation with a variety of systems using new technology (pygame) with little to no guidance.


## Future Additions
- Options screen for pixel size and world size
- ability to hide controls from the right hand corner
## Current Issues
- Code is getting difficult to manage need to refactor the code
- Optimization Issues
    - The (without altering settings) simulation handles upto  14400 (non-void particles) (determined by screen size and pixel size in game.py) particles. This is a lot of particles, which can cause slow downs once the screen is full of them.
## Recent Changes
- Added a laser (bounces around like the DVD logo)
- Added Ice
- Ice turns to water when touching lava and Fire
- Ice Freezes water after a delay
- Steam, Smoke, Gas dissipation
- Oil is instantly consumed by fire and doesnot generate ash
- Steam can dissipate into water
- Water extinguishes fire
- lava destroys wood and moss
- Added Fire
- Fire Dissipation
- Fire creates smoke
- Fire turns to ash
- Fire spreads to wood and moss
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
