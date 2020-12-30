# Packman 3D - just a bit worse
This project was creates as a part of the _Computer Graphics_ course at _Reykjavík University_. It's a 3D maze game where you have to reach the goal in the middle while avoiding the ghosts on the map.

It was creates in cooperation with @ertolv.

## Here is a low quality example:
![](res/readme/example.gif)

The actual game looks much nicer and even contains music. It's definitely worth a try if you have 5 minutes to spare :)

## Controls
| Type              | Controls                   |
| ----------------- | -------------------------- |
| Movement controls | `[W]`, `[A]`, `[S]`, `[D]` |
| Vertical control  | `[SPACE]`, `[SHIFT]`       |
| Rotation controls | `[<]`, `[^]`, `[v]`, `[>]` |
| Camera switch     | `[M]`                      |
| Return to Home    | `[H]`                      |
| Debug information | `[P]`                      | 

You can also use the mouse to rotate the view :)

## Installing and running the game
This game uses: 
* PyOpenGL and pygame for rendering
* PyGLM for beautiful math.
* Esper for the ECS architecture

You can use to install these requirements:
* `pip install -r requirements.txt`

Use `python src/main.py` to run the game.

## Documentation
We choose an entity component system as our game architecture. The documentation is found in [`.docs/ecs.md`](.docs/ecs.md) and is definitely worth a read. The lighting system with our addition of light attenuation is documented in [`.docs/lighting.md`](.docs/lighting.md). Have fun reading them :D.

(I don't take responsibility for any spelling mistakes. Feel free to fix them, it's sadly not my strong suit)

## A small note:
I'm not quite sure when it happened and why, but we swapped the y and z value of the world. This means that x and y are basically the floor while z controls the height above the floor. This is a bit unusual for 3D games, but it seems to work so yay.

## Repository
This project was extracted from a previous [repository](https://github.com/xFrednet/ru_tgra_Computer-Graphics/tree/03ea2939ef882d420cef6fd575a9e1d5afa98b30) containing several projects. 