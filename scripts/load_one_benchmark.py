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

    case_index = 41
    case_list = ib.load_case_list()
    print()
    print(80*"-")
    print(case_list[case_index])
    print(80*"-")

if __name__ == "__main__":
    main()