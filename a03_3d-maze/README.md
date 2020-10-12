# Packman 3D - just a bit worse

## Controls
| Type              | Controls                   |
| ----------------- | -------------------------- |
| Movement controls | `[W]`, `[A]`, `[S]`, `[D]` |
| Vertical control  | `[SPACE]`, `[SHIFT]`       |
| Rotation controls | `[<]`, `[^]`, `[v]`, `[>]` |
| Camera switch     | `[M]`                      |
| Return to Home    | `[H]`                      |
| Debug information | `[P]`                      | 

## Installing and running the game
This game uses: 
* PyOpenGL and pygame for rendering
* PyGLM for beautiful math.
* Esper for the ECS architecture

You can use `pip install PyOpenGL pygame PyGLM esper` to install these requirements.

Use `python main.py` to run the game.

## Documentation
We choose an entity component system as out game architecture. The documentation is found in [`.docs/ecs.md`](.docs/ecs.md) and is definitely worth a read. The lighting system with out addition of a attenuation is documented in [`.docs/lighting.md`](.docs/lighting.md). Have fun reading them :D.

## A small note:
I'm not quite sure when it happened and why but we swapped the y and z value of the world. This means that x and y are basically the floor while z controls the height above the floor. This is a bit unusual for 3D games but it seems to work so yay.