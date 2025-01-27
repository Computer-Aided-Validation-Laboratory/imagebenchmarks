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
    ib.run_simulations((0,1,2))
    #ib.run_simulations()

if __name__ == "__main__":
    main()