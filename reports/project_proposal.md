# Evacuation

![Sample Output](media/sampleOutput.png)
Possible output graphs.

## Experiments
The original research paper ran multiple experiments that we would like to replicate.
First, a single exit with a large crowd. This will let us validate our model matches the original paper.

We want to extend our software to allow arbitrary map input, so that we can experiment with different environments, including a widened corridor, multiple doors, etc.

The original paper implemented herding behavior and low visibility, but these are probably out of scope.

Our biggest technical risk is 1. making a usable physics simulation, 2. making agents have goals. After discussing the problems with peers and reading on the internet, we concluded that making a physics simulation is feasible, and that the agents can have simple goals while still creating interesting phenomena.

The original paper has very effective data visualization that we want to replicate and learn from.
