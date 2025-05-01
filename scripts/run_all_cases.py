"""
================================================================================
image benchmarks for
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
import imagebenchmarks as ib

def main() -> None:
    #ib.run_simulations((0,1,2))

    # Run default list of simulations with 16 threads
    ib.run_simulations(sim_indices=(0,1,3,4,5,6,7,8,9),num_threads=16)

if __name__ == "__main__":
    main()