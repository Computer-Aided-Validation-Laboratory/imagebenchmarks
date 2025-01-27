"""
================================================================================
pyvale: the python validation engine
image benchmarks
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
from pathlib import Path
from importlib.resources import files
import imagebenchmarks.caseconstants as const


def get_sim_file_paths(sim_index: int) -> tuple[Path,Path]:
    return (Path(files("imagebenchmarks.simulations")
                 .joinpath(const.SIM_FILES[sim_index]+".geo")),
            Path(files("imagebenchmarks.simulations")
                 .joinpath(const.SIM_FILES[sim_index]+".i")))


