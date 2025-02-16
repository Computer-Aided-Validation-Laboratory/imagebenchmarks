"""
================================================================================
image benchmarks for
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
import time
from pathlib import Path
import mooseherder as mh

def main() -> None:
    sim_str = "cylinder_m2"
    sim_path = Path("src/imagebenchmarks/simulations/")

    gmsh_path = Path.home()
    sim_files = (sim_str+'.geo',sim_str+'.i')

    # NOTE: if the msh file exists then gmsh will not run
    if (sim_path / sim_files[0]).is_file():
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
                              n_threads = 16,
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


if __name__ == "__main__":
    main()