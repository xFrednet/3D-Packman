# 3D Terrain - rendering smooth was yesterday
This project was created in the _Computer Graphics_ course at Reykjavik University in 2020. The project renders a 3D low poly terrain with some particle effects. It is written using Python and OpenGL.

The [report](.docs/report.md) and a [gallery](.docs/gallery.md) can be found inside the `.doc` folder.

## Controls
| Type                 | Controls                   |
| -------------------- | -------------------------- |
| Movement controls    | `[W]`, `[A]`, `[S]`, `[D]` |
| Vertical control     | `[SPACE]`, `[SHIFT]`       |
| Rotation controls    | `[<]`, `[^]`, `[v]`, `[>]` |
| Height map selection | `[0]`, `[1]`, ..., `[9]`   |

## Installation
This game uses: 
* PyOpenGL and pygame for rendering
* PyGLM for beautiful math.
* Esper for the ECS architecture
* PyGame as a engine (Note that minimum version `2.0.0.dev12` is required)
* NumPy for some number magic

You can use `pip install -r requirements.txt` to install these requirements.

## Running the Simulation
The simulation can be started by starting the `main.py` file in the source directory:
* `$ python main.py`