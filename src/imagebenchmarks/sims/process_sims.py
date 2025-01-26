"""
================================================================================
pyvale: the python validation engine
image benchmarks
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
from pathlib import Path
import dill
import numpy as np
from scipy.spatial.transform import Rotation
import pyvale


def main() -> None:
    save_path = Path.home()/"imagebenchmarks"/"src"/"imagebenchmarks"/"benchmarks"

    field_key = "disp_y"
    components = ("disp_x","disp_y","disp_z")
    spat_dim = 3

    sim_path = Path.home()/"imagebenchmarks"/"src"/"imagebenchmarks"/"sims"
    sim_files = (sim_path/"cylinder_m1_out.e",
                 sim_path/"cylinder_m2_out.e",
                 sim_path/"cylinder_m3_out.e",
                 sim_path/"cylinder_m4_out.e",
                 sim_path/"cylinder_m5_out.e",
                 sim_path/"plate_m1_out.e",
                 sim_path/"plate_m5_out.e",
                 sim_path/"plate_m10_out.e",
                 sim_path/"plate_m25_out.e",
                 sim_path/"plate_m50_out.e",)
    sim_tags = ("cylinder",)*5 + ("plate",)*5

    cameras = {"0.3Mpx":(np.array([640,480]),np.array([5.0e-3,5.0e-3])),
               "1Mpx":(np.array([1280,960]),np.array([5.3e-3,5.3e-3])),
               "5Mpx":(np.array([2464,2056]),np.array([3.45e-3,3.45e-3])),
               "24Mpx":(np.array([5328,4608]),np.array([2.74e-3,2.74e-3])),}
    border_factors = (1.05,0.75)
    subsampling = (1,2)

    cylinder_rot =  Rotation.from_euler("zyx",
                                  [0.0, 0.0, -45.0],
                                  degrees=True)
    plate_rot =  Rotation.from_euler("zyx",
                                  [0.0, -20.0, 0.0],
                                  degrees=True)
    camera_rots = (cylinder_rot,)*5 + (plate_rot,)*5
    focal_length = 50.0

    sim_path = sim_path/sim_files[0]

    field_key = "disp_y"
    components = ("disp_x","disp_y","disp_z")

    case_count = 0
    for ii,ff in enumerate(sim_files):

        mesh_world = pyvale.create_camera_mesh(ff,
                                               field_key,
                                               components,
                                               spat_dim)

        sim_tag = f"mesh{ii}_{mesh_world.elem_count}elems"
        save_file = save_path/(sim_tag+".dill")
        with open(save_file, 'wb') as dill_file:
            dill.dump(mesh_world,dill_file)

        for cc in cameras:
            for bb in border_factors:
                for ss in subsampling:

                        cam_z_world = camera_rots[ii].as_matrix()[:,-1]
                        fov_leng = (pyvale.fov_from_cam_rot(camera_rots[ii],
                                                            mesh_world.coords)*bb)
                        image_dist = pyvale.image_dist_from_fov(cameras[cc][0],
                                                                cameras[cc][1],
                                                                focal_length,
                                                                fov_leng)
                        roi_pos_world = mesh_world.coord_cent[:-1]
                        cam_pos_world = (roi_pos_world + np.max(image_dist)
                                         *cam_z_world)

                        cam_data = pyvale.CameraData(pixels_num=cameras[cc][0],
                                                    pixels_size=cameras[cc][1],
                                                    pos_world=cam_pos_world,
                                                    rot_world=camera_rots[ii],
                                                    roi_cent_world=roi_pos_world,
                                                    focal_length=focal_length,
                                                    sub_samp=ss)

                        if bb >= 1.0:
                            crop_str = "nocrop"
                        else:
                            crop_str = "crop"

                        tag = (f"case{case_count}_{sim_tags[ii]}_{cc}_"+
                               f"{ss}subsamp_{crop_str}_"+
                               f"{mesh_world.elem_count}elems")

                        save_file = save_path/(tag+".dill")
                        with open(save_file, 'wb') as dill_file:
                            dill.dump((tag,sim_tag,cam_data),dill_file)

                        print(tag)
                        case_count = case_count + 1



if __name__ == "__main__":
    main()