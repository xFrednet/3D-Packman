# Notes

## Dev
1. Rewrite engine
2. Create VS & FS get it running
3. Create GS 
4. Constant normal vector (cross product)
5. Calculate center
6. Move lighting from PS to GS for performance
7. Move lighting from FS to GS for performance


## 1. Geometry shader
* The value of `gl_in[index].gl_Position` have already been modified by the view and projection matrix.

## Terrain
* Swap between two triangle orientations to make it more interesting