# Intro 
Some notes about the different program components and ongoing discussion.

Kaleidoscope should be implemented as a simulation library that enables to generate
very simple game of life or fractal visualizations.

So a user should be able to define the agent and the environment (or select some
pre defined one's) and run the simulation.

# Initialization
Key program arguments are

+ Seed value
+ World size (x, y, z?)
+ Initial state of the world
+ Agent (**region of influence (ROI)** , e.g 3x3 area, and function to be called)
+ Environment (update function that runs before agents are executed)
+ Border conditions (border are dead area, they reflect, they wrap around)

# Agent
The agent is a simple function that receives a sub region of the world (ROI)
and returns a new region of the same size.

For each pixel of the world a agent function is executed once per tick.

# Environment 
The environment function is called at the beginning of each tick and can alter
the complete world.

It can create seed new fields or alter existing onces.

# Update function
The update function is executed each tick and performs the following steps
1. Creates a new world (W1) based on the previous world (W0)
2. Execute the environment on the new world
3. Executes in multiple threads the Agent for each pixel reading W1 writing to W0
4. The visualization function is used to show the state of W0
5. User input that effects execution is processed

# Visualization
The visualization is plotting W0 where each pixel is represented as RGB 32Bit color pixel

In addition to the world the meta information is plotted like
+ Tick count
+ Ticks per second
+ Level indicator (z coordinate)
+ avg(df/F) ... indicator on how much did the world change in the last 10? ticks
+ Documentation for key bindings

# User interaction
The interface is implemented by a few key bindings that will take effect at the
end of the current tick cycle.

+ Quit (q)
+ Store image of current world (s)
+ Change Level (j ... up, k ... down)
+ Increase ticks/second (+)
+ Decrease ticks/second (-)
