"""
================================================================================
image benchmarks for
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
import numpy as np
from scipy.spatial.transform import Rotation

CASE_FILE = "case_list.json"

FIELD_KEY = "disp_y"
COMPONENTS = ("disp_x","disp_y","disp_z")
SPAT_DIMS = 3

CAMERA_TAGS = ("1Mpx","5Mpx","24Mpx")
CAMERA_PIXELS = ((np.array([1280,960],dtype=np.int32),np.array([5.3e-3,5.3e-3])),
           (np.array([2464,2056],dtype=np.int32),np.array([3.45e-3,3.45e-3])),
           (np.array([5328,4608],dtype=np.int32),np.array([2.74e-3,2.74e-3])),)
BORDER_FACTORS = (1.05,0.75)
SUBSAMPLING = (1,2)
FOCAL_LENGTH = 50.0


SIM_FILES = ("plate_m10",
            "plate_m25",
            "plate_m50",
            "plate_m10_linquad",
            "plate_m10_quadtri",
            "plate_m10_quadquad",)

SIM_COUNT = len(SIM_FILES)
SIM_TAGS = ("plate_lintri",
            "plate_lintri",
            "plate_lintri",
            "plate_linquad",
            "plate_quadtri",
            "plate_quadquad")


PLATE_ROTS = Rotation.from_euler("zyx",
                                [0.0, -30.0, 0.0],
                                degrees=True)
CAMERA_ROTS = (PLATE_ROTS,)*SIM_COUNT


# SIM_FILES = ("plate_m1",
#             "plate_m5",
#             "plate_m10",
#             "plate_m25",
#             "plate_m50",)
# SIM_FILES = ("cylinder_m1",
#             "cylinder_m2",
#             "cylinder_m3",
#             "cylinder_m4",
#             "cylinder_m5",
#             "plate_m1",
#             "plate_m5",
#             "plate_m10",
#             "plate_m25",
#             "plate_m50",)
#SIM_TAGS = ("cylinder",)*5 + ("plate",)*5
# CYLINDER_ROT = Rotation.from_euler("zyx",
#                                 [0.0, 0.0, -45.0],
#                                 degrees=True)
# PLATE_ROTS = Rotation.from_euler("zyx",
#                                 [0.0, -20.0, 0.0],
#                                 degrees=True)
# CAMERA_ROTS = (CYLINDER_ROT,)*5 + (PLATE_ROTS,)*5
