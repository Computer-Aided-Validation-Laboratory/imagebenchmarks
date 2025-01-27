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
import pyvale
import imagebenchmarks as ib


def main() -> None:
    save_path = Path.home()/"imagebenchmarks"/"src"/"imagebenchmarks"/"benchmarks"
    sim_path = Path.home()/"imagebenchmarks"/"src"/"imagebenchmarks"/"simulations"

    case_count = 0
    for ii,ff in enumerate(ib.SIM_FILES):

        mesh_world = pyvale.create_camera_mesh(sim_path/(ff+"_out.e"),
                                               ib.FIELD_KEY,
                                               ib.COMPONENTS,
                                               ib.SPAT_DIMS)

        sim_tag = f"mesh{ii}_{mesh_world.elem_count}elems"
        save_file = save_path/(sim_tag+".dill")
        with open(save_file, 'wb') as dill_file:
            dill.dump(mesh_world,dill_file)

        for cc in ib.CAMERAS:
            for bb in ib.BORDER_FACTORS:
                for ss in ib.SUBSAMPLING:

                        cam_z_world = ib.CAMERA_ROTS[ii].as_matrix()[:,-1]
                        fov_leng = (pyvale.fov_from_cam_rot(ib.CAMERA_ROTS[ii],
                                                            mesh_world.coords)*bb)
                        image_dist = pyvale.image_dist_from_fov(ib.CAMERAS[cc][0],
                                                                ib.CAMERAS[cc][1],
                                                                ib.FOCAL_LENGTH,
                                                                fov_leng)
                        roi_pos_world = mesh_world.coord_cent[:-1]
                        cam_pos_world = (roi_pos_world + np.max(image_dist)
                                         *cam_z_world)

                        cam_data = pyvale.CameraData(pixels_num=ib.CAMERAS[cc][0],
                                                    pixels_size=ib.CAMERAS[cc][1],
                                                    pos_world=cam_pos_world,
                                                    rot_world=ib.CAMERA_ROTS[ii],
                                                    roi_cent_world=roi_pos_world,
                                                    focal_length=ib.FOCAL_LENGTH,
                                                    sub_samp=ss)

                        if bb >= 1.0:
                            crop_str = "nocrop"
                        else:
                            crop_str = "crop"

                        tag = (f"case{case_count}_{ib.SIM_TAGS[ii]}_{cc}_"+
                               f"{ss}subsamp_{crop_str}_"+
                               f"{mesh_world.elem_count}elems")

                        save_file = save_path/(tag+".dill")
                        with open(save_file, 'wb') as dill_file:
                            dill.dump((tag,sim_tag,cam_data),dill_file)

                        print(tag)
                        case_count = case_count + 1


if __name__ == "__main__":
    main()