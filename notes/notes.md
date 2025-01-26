# Notes
- Toml to install the benchmarks and make the accesible to python
- Perform full conversion to extracted mesh and only surface mesh data that is
  required


- Need an overarching controller that can run as many benchmarks as you like
- Need functions that setup the benchmarks

- Saved output from each benchmark as a numpy array: image and depth buffers

## Field of View:
```
sensor_dimension = num_pixels * pixel_size

FOV_angle = 2 * arctan(sensor_dimension / (2 * focal_length))
FOV_leng = 2 * imaging_distance * tan(FOV_angle / 2)

imaging_distance = FOV_leng / (2*tan(FOV_ang/2))
```

## Cameras
All with a 50mm focal length lens.

- 0.3 Mpx, 640x480 pixels, pixel size = 5x5 micron
- 1.2 Mpx, 1280x960 pixels, pixel size = 5.3x5.3 micron
- 5.1 Mpx, 2464x2056 pixels, pixel size = 3.45x3.45 micron
- 24.6 Mpx, 5328x4608 pixels, pixel size = 2.74x2.74 micron

## Print Mesh Data
```python
print()
print(80*"-")
print("EXTRACTED SURFACE MESH DATA")
print(f"{mesh_world.name=}")
print()
print(f"node_count =     {mesh_world.node_count}")
print(f"elem_count =     {mesh_world.elem_count}")
print(f"nodes_per_elem = {mesh_world.nodes_per_elem}")
print()
print(f"{mesh_world.coords.shape=}")
print(f"{mesh_world.connectivity.shape=}")
print()
print(f"{mesh_world.elem_coords.shape=}")
print()
print(f"{mesh_world.field_by_node.shape=}")
print(f"{mesh_world.field_by_elem.shape=}")
print()
print(f"{mesh_world.coord_bound_min=}")
print(f"{mesh_world.coord_bound_max=}")
print(f"{mesh_world.coord_cent=}")
    print(80*"-")
```