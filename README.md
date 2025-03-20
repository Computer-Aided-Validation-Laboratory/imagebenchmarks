# Image Benchmarks
A set of physics-based imaging benchmarks for testing the speed of simulating digital image correlation and infrared thermography using `pyvale`.

## Usage
The benchmark cases are describes below and z case can be retrieved using its index in the case list or by using its string tag as follows:

```python
import imagebenchmarks as ib

(case_ident,case_mesh,case_camera) = ib.load_benchmark_by_index(case_index)
(case_ident,case_mesh,case_camera) = ib.load_benchmark_by_tag(case_tag)
```

The case list can also be retrieved using the following: `case_list = ib.load_case_list()`. The mesh data (nodal coordinates, connectivity table and field to render) for the case is stored as a `pyvale.CameraMesh` data class and the camera data for the case is stored as a `pyvale.CameraData` data class. Each `pyvale.CameraData.field_to_render` contains 8 time steps to render along with a zero frame at the start.

The benchmarks should be run as follows:
- Average render time for a single frame rendering the last field in `pyvale.CameraData.field_to_render` 30 times sequentially. This case only allows parallelisation within a single frame.
- Average total time to render all 8 frames in `pyvale.CameraData.field_to_render` 30 times. This case allows for rendering the 8 frames in parallel.

## Case Descriptions

**Simulations**<br>
A 3D thin plate with a hole in the center loaded in tension. Uses tetrahedral 4-node linear elements with the surface mesh extracted to 3 node linear triangles. Higher order and quadrilateral meshes are included in the later benchmarks denoted: 'quadtri' for quadratic triangles, 'linquad' for linear quadrilaterals and 'quadquad' for quadratic quadrilaterals. The vertical displacement field `disp_y` is to be rendered as the image. Plate mesh bounding box: X [0,100], Y [0,130], Z [0,2] mm.

**Cameras**<br>
The following cameras form the benchmark list:
- "1Mpx" = 1280x960 pixels, pixel size = 5.3x5.3 micron
- "5Mpx" = 2464x2056 pixels, pixel size = 3.45x3.45 micron
- "24Mpx" = 5328x4608 pixels, pixel size = 2.74x2.74 micron

All cameras use a 50mm focal length lens. Two pixel subsampling (anti-aliasing) cases are analysed per camera: 1) 1 sample per pixel, 2) 2x2 subsamples per pixel.

**Camera Position**<br>
The camera is automatically positioned such that the center of the pixel array points at the center of the mesh. For the plate simulation the camera is rotated -30 degrees about the Y axis to view the plate at an angle.

The imaging distance is also automatically set based on the 'crop' / 'no crop' condition. For the 'crop' condition the camera is positioned to include 75% of the bounding box enclosing the mesh projected onto the camera viewing plane. For the no crop condition the camera is placed to include 105% of the bounding box enclosing the mesh projected onto the camera viewing plane (i.e. a 5% buffer is placed around the projected bounding box to ensure all elements are within the field of view).

## Case List
The list of all benchmark cases is stored in a json file which can be retrieved using the `imagebenchmark.get_case_list()` function. The current benchmark list is given below. Each benchmark uses
```json
[
    "case0_plate_lintri_1Mpx_1subsamp_nocrop_11776elems",
    "case1_plate_lintri_1Mpx_2subsamp_nocrop_11776elems",
    "case2_plate_lintri_1Mpx_1subsamp_crop_11776elems",
    "case3_plate_lintri_1Mpx_2subsamp_crop_11776elems",
    "case4_plate_lintri_5Mpx_1subsamp_nocrop_11776elems",
    "case5_plate_lintri_5Mpx_2subsamp_nocrop_11776elems",
    "case6_plate_lintri_5Mpx_1subsamp_crop_11776elems",
    "case7_plate_lintri_5Mpx_2subsamp_crop_11776elems",
    "case8_plate_lintri_24Mpx_1subsamp_nocrop_11776elems",
    "case9_plate_lintri_24Mpx_2subsamp_nocrop_11776elems",
    "case10_plate_lintri_24Mpx_1subsamp_crop_11776elems",
    "case11_plate_lintri_24Mpx_2subsamp_crop_11776elems",
    "case12_plate_lintri_1Mpx_1subsamp_nocrop_65296elems",
    "case13_plate_lintri_1Mpx_2subsamp_nocrop_65296elems",
    "case14_plate_lintri_1Mpx_1subsamp_crop_65296elems",
    "case15_plate_lintri_1Mpx_2subsamp_crop_65296elems",
    "case16_plate_lintri_5Mpx_1subsamp_nocrop_65296elems",
    "case17_plate_lintri_5Mpx_2subsamp_nocrop_65296elems",
    "case18_plate_lintri_5Mpx_1subsamp_crop_65296elems",
    "case19_plate_lintri_5Mpx_2subsamp_crop_65296elems",
    "case20_plate_lintri_24Mpx_1subsamp_nocrop_65296elems",
    "case21_plate_lintri_24Mpx_2subsamp_nocrop_65296elems",
    "case22_plate_lintri_24Mpx_1subsamp_crop_65296elems",
    "case23_plate_lintri_24Mpx_2subsamp_crop_65296elems",
    "case24_plate_lintri_1Mpx_1subsamp_nocrop_250496elems",
    "case25_plate_lintri_1Mpx_2subsamp_nocrop_250496elems",
    "case26_plate_lintri_1Mpx_1subsamp_crop_250496elems",
    "case27_plate_lintri_1Mpx_2subsamp_crop_250496elems",
    "case28_plate_lintri_5Mpx_1subsamp_nocrop_250496elems",
    "case29_plate_lintri_5Mpx_2subsamp_nocrop_250496elems",
    "case30_plate_lintri_5Mpx_1subsamp_crop_250496elems",
    "case31_plate_lintri_5Mpx_2subsamp_crop_250496elems",
    "case32_plate_lintri_24Mpx_1subsamp_nocrop_250496elems",
    "case33_plate_lintri_24Mpx_2subsamp_nocrop_250496elems",
    "case34_plate_lintri_24Mpx_1subsamp_crop_250496elems",
    "case35_plate_lintri_24Mpx_2subsamp_crop_250496elems",
    "case36_plate_linquad_1Mpx_1subsamp_nocrop_5888elems",
    "case37_plate_linquad_1Mpx_2subsamp_nocrop_5888elems",
    "case38_plate_linquad_1Mpx_1subsamp_crop_5888elems",
    "case39_plate_linquad_1Mpx_2subsamp_crop_5888elems",
    "case40_plate_linquad_5Mpx_1subsamp_nocrop_5888elems",
    "case41_plate_linquad_5Mpx_2subsamp_nocrop_5888elems",
    "case42_plate_linquad_5Mpx_1subsamp_crop_5888elems",
    "case43_plate_linquad_5Mpx_2subsamp_crop_5888elems",
    "case44_plate_linquad_24Mpx_1subsamp_nocrop_5888elems",
    "case45_plate_linquad_24Mpx_2subsamp_nocrop_5888elems",
    "case46_plate_linquad_24Mpx_1subsamp_crop_5888elems",
    "case47_plate_linquad_24Mpx_2subsamp_crop_5888elems",
    "case48_plate_quadtri_1Mpx_1subsamp_nocrop_47104elems",
    "case49_plate_quadtri_1Mpx_2subsamp_nocrop_47104elems",
    "case50_plate_quadtri_1Mpx_1subsamp_crop_47104elems",
    "case51_plate_quadtri_1Mpx_2subsamp_crop_47104elems",
    "case52_plate_quadtri_5Mpx_1subsamp_nocrop_47104elems",
    "case53_plate_quadtri_5Mpx_2subsamp_nocrop_47104elems",
    "case54_plate_quadtri_5Mpx_1subsamp_crop_47104elems",
    "case55_plate_quadtri_5Mpx_2subsamp_crop_47104elems",
    "case56_plate_quadtri_24Mpx_1subsamp_nocrop_47104elems",
    "case57_plate_quadtri_24Mpx_2subsamp_nocrop_47104elems",
    "case58_plate_quadtri_24Mpx_1subsamp_crop_47104elems",
    "case59_plate_quadtri_24Mpx_2subsamp_crop_47104elems",
    "case60_plate_quadquad_1Mpx_1subsamp_nocrop_135168elems",
    "case61_plate_quadquad_1Mpx_2subsamp_nocrop_135168elems",
    "case62_plate_quadquad_1Mpx_1subsamp_crop_135168elems",
    "case63_plate_quadquad_1Mpx_2subsamp_crop_135168elems",
    "case64_plate_quadquad_5Mpx_1subsamp_nocrop_135168elems",
    "case65_plate_quadquad_5Mpx_2subsamp_nocrop_135168elems",
    "case66_plate_quadquad_5Mpx_1subsamp_crop_135168elems",
    "case67_plate_quadquad_5Mpx_2subsamp_crop_135168elems",
    "case68_plate_quadquad_24Mpx_1subsamp_nocrop_135168elems",
    "case69_plate_quadquad_24Mpx_2subsamp_nocrop_135168elems",
    "case70_plate_quadquad_24Mpx_1subsamp_crop_135168elems",
    "case71_plate_quadquad_24Mpx_2subsamp_crop_135168elems"
]
```
