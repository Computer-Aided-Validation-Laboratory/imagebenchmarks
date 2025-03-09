"""
================================================================================
image benchmarks for
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
import warnings
import time
from pathlib import Path
from importlib.resources import files
import json

import numpy as np
import dill
import mooseherder as mh
import pyvale

import imagebenchmarks.caseconstants as const


def get_sim_path() -> Path:
    return Path(files("imagebenchmarks.simulations").joinpath(""))

def get_benchmark_path() -> Path:
    return Path(files("imagebenchmarks.benchmarks").joinpath(""))

def check_sim_index(sim_index: int) -> int:
    if sim_index >= const.SIM_COUNT or sim_index < 0:
        sim_index = 0
        warnings.warn(f"Simulation index {sim_index} is out of bounds for"
                        + f" the number of simulations {const.SIM_COUNT}."
                        + "Defaulting sim index to zero",
                        category=UserWarning,)

    return sim_index

def check_case_index(case_index: int, case_list: list[str]) -> int:
    if case_index >= len(case_list) or case_index < 0:
        case_index = 0
        warnings.warn(f"Case index {case_index} is out of bounds for"
                        + f" the number of benchmarks {len(case_list)}."
                        + "Defaulting case index to zero",
                        category=UserWarning,)

    return case_index

def check_case_tag(case_tag: str, case_list: list[str]) -> int:
    if case_tag not in case_list:
        case_tag = case_list[0]
        warnings.warn(f"Case tag '{case_tag}' is not in the benchmarks."
                        + f" Defaulting to case tag '{case_list[0]}'.",
                        category=UserWarning,)

    return case_tag

def get_sim_file_path(sim_index: int) -> tuple[Path,Path]:
    sim_index = check_sim_index(sim_index)
    return (Path(files("imagebenchmarks.simulations")
                 .joinpath(const.SIM_FILES[sim_index]+".geo")),
            Path(files("imagebenchmarks.simulations")
                 .joinpath(const.SIM_FILES[sim_index]+".i")))


def run_one_simulation(sim_index: int,
                       n_threads: int = 8,
                       force_gmsh: bool = True,
                       gmsh_path: Path | None = None,
                       moose_path: Path | None = None,
                       ) -> Path:

    sim_index = check_sim_index(sim_index)
    sim_str = const.SIM_FILES[sim_index]

    if moose_path is None:
        moose_path = Path.home()

    if gmsh_path is None:
        gmsh_path = Path.home()

    sim_path = get_sim_path()

    print(80*'=')
    print(f'Running: {sim_str}')
    print(80*'=')

    sim_files = (sim_str+'.geo',sim_str+'.i')

    # NOTE: if the msh file exists then gmsh will not run
    if (((sim_path / sim_files[0]).is_file() ) or force_gmsh):
        gmsh_runner = mh.GmshRunner(gmsh_path / 'gmsh/bin/gmsh')

        gmsh_start = time.perf_counter()
        gmsh_runner.run(sim_path / sim_files[0])
        gmsh_run_time = time.perf_counter()-gmsh_start
    else:
        print('Bypassing gmsh.')
        gmsh_run_time = 0.0

    config = {'main_path': Path.home() / 'moose',
            'app_path': Path.home() / 'proteus',
            'app_name': 'proteus-opt'}

    moose_config = mh.MooseConfig(config)
    moose_runner = mh.MooseRunner(moose_config)

    moose_runner.set_run_opts(n_tasks = 1,
                              n_threads = n_threads,
                              redirect_out = False)

    moose_start_time = time.perf_counter()
    moose_runner.run(sim_path / sim_files[1])
    moose_run_time = time.perf_counter() - moose_start_time

    print()
    print("="*80)
    print(f'SIMULATION: {sim_str}')
    print(f'Gmsh run time = {gmsh_run_time:.2f} seconds')
    print(f'MOOSE run time = {moose_run_time:.3f} seconds')
    print("="*80)
    print()

    return sim_path


def run_simulations(sim_indices: tuple[int,...] | None = None) -> list[Path]:

    if sim_indices is None:
        sim_indices = range(const.SIM_COUNT)

    sim_paths = []
    for ss in sim_indices:
        sim_paths.append(run_one_simulation(ss))

    return sim_paths


def save_surface_meshes(sim_indices: tuple[int,...] | None = None,
                        save_path: Path | None = None) -> list[Path]:

    if sim_indices is None:
        sim_indices = range(const.SIM_COUNT)

    if save_path is None:
        save_path = get_benchmark_path()

    sim_path = get_sim_path()

    mesh_save_paths = []
    for ii in sim_indices:
        sim_index = check_sim_index(ii)
        curr_path = sim_path/(const.SIM_FILES[sim_index]+"_out.e")
        mesh_world = pyvale.create_camera_mesh(curr_path,
                                                const.FIELD_KEY,
                                                const.COMPONENTS,
                                                const.SPAT_DIMS)

        sim_tag = f"mesh{sim_index}_{mesh_world.elem_count}elems"
        mesh_save_file = save_path/(sim_tag+".dill")
        with open(mesh_save_file, 'wb') as dill_file:
            dill.dump(mesh_world,dill_file)

        mesh_save_paths.append(mesh_save_file)

    return mesh_save_paths


def build_and_save_benchmarks(sim_indices: tuple[int,...] | None = None,
                              save_path: Path | None = None
                              ) -> tuple[list[Path],list[Path],list[str]]:

    if sim_indices is None:
        sim_indices = range(const.SIM_COUNT)

    if save_path is None:
        save_path = get_benchmark_path()

    sim_path = get_sim_path()

    case_list = []
    mesh_save_paths = []
    benchmark_save_paths = []
    case_count = 0
    for ii in sim_indices:
        sim_index = check_sim_index(ii)
        curr_path = sim_path/(const.SIM_FILES[sim_index]+"_out.e")
        mesh_world = pyvale.create_camera_mesh(curr_path,
                                                const.FIELD_KEY,
                                                const.COMPONENTS,
                                                const.SPAT_DIMS)

        sim_tag = f"mesh{sim_index}_{mesh_world.elem_count}elems"
        mesh_path = save_path/(sim_tag+".dill")
        with open(mesh_path, 'wb') as dill_file:
            dill.dump(mesh_world,dill_file)

        mesh_save_paths.append(mesh_path)
        for jj,cc in enumerate(const.CAMERA_PIXELS):
            for bb in const.BORDER_FACTORS:
                for ss in const.SUBSAMPLING:

                    if bb >= 1.0:
                        crop_str = "nocrop"
                    else:
                        crop_str = "crop"

                    case_tag = (f"case{case_count}_{const.SIM_TAGS[ii]}_{const.CAMERA_TAGS[jj]}_"+
                            f"{ss}subsamp_{crop_str}_"+
                            f"{mesh_world.elem_count}elems")

                    cam_z_world = const.CAMERA_ROTS[ii].as_matrix()[:,-1]
                    fov_leng = (pyvale.CameraTools.fov_from_cam_rot_3d(const.CAMERA_ROTS[ii],
                                                        mesh_world.coords)*bb)
                    image_dist = pyvale.CameraTools.image_dist_from_fov_3d(cc[0],
                                                            cc[1],
                                                            const.FOCAL_LENGTH,
                                                            fov_leng)

                    roi_pos_world = mesh_world.coord_cent[:-1]
                    cam_pos_world = (roi_pos_world + np.max(image_dist)
                                        *cam_z_world)

                    cam_data = pyvale.CameraData(pixels_num=cc[0],
                                                pixels_size=cc[1],
                                                pos_world=cam_pos_world,
                                                rot_world=const.CAMERA_ROTS[ii],
                                                roi_cent_world=roi_pos_world,
                                                focal_length=const.FOCAL_LENGTH,
                                                sub_samp=ss)

                    benchmark_path = save_path/(case_tag+".dill")
                    with open(benchmark_path, 'wb') as dill_file:
                        dill.dump((case_tag,sim_tag,cam_data,mesh_path),dill_file)

                    benchmark_save_paths.append(benchmark_path)

                    case_list.append(case_tag)
                    print(f"Saving benchmark camera data for case: {case_tag}")
                    case_count = case_count + 1

    case_list_path = save_path/const.CASE_FILE
    with open(case_list_path , 'w', encoding="utf-8") as json_file:
        json.dump(case_list,json_file, indent=4)

    return (benchmark_save_paths,mesh_save_paths,case_list)


def load_case_list(benchmark_path: Path | None = None) -> list[str]:
    if benchmark_path is None:
        benchmark_path = get_benchmark_path()

    case_list_path = benchmark_path / const.CASE_FILE
    with open(case_list_path, "r", encoding="utf-8") as case_file:
        case_list = json.load(case_file)

    return case_list


def load_benchmark_by_index(case_index: int,
                             benchmark_path: Path | None = None
                            ) -> tuple[str,
                                       pyvale.CameraMeshData,
                                       pyvale.CameraData]:

    if benchmark_path is None:
        benchmark_path = get_benchmark_path()

    case_list = load_case_list(benchmark_path)
    case_index = check_case_index(case_index,case_list)

    case_path = benchmark_path/(case_list[case_index]+".dill")
    with open(case_path,"rb") as case_file:
        case_data = dill.load(case_file)

    mesh_path = benchmark_path/(case_data[1]+".dill")
    with open(mesh_path,"rb") as mesh_file:
        mesh_data = dill.load(mesh_file)

    return (case_data[0],mesh_data,case_data[2])

def load_benchmark_by_tag(case_tag: str,
                          benchmark_path: Path | None = None
                          ) -> tuple[str,
                                     pyvale.CameraMeshData,
                                     pyvale.CameraData]:

    if benchmark_path is None:
        benchmark_path = get_benchmark_path()

    case_list = load_case_list(benchmark_path)
    case_tag = check_case_tag(case_tag,case_list)

    case_path = benchmark_path/(case_tag+".dill")
    with open(case_path,"rb") as case_file:
        case_data = dill.load(case_file)

    mesh_path = benchmark_path/(case_data[1]+".dill")
    with open(mesh_path,"rb") as mesh_file:
        mesh_data = dill.load(mesh_file)

    return (case_data[0],mesh_data,case_data[2])


