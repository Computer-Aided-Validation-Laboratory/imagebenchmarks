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
    print(80*"-")
    print("Building Imaging Benchmarks")
    print(80*"-")
    ib.build_and_save_benchmarks()

    case_list = ib.load_case_list()
    print(80*"-")
    print(case_list[-1])
    print(80*"-")
    print("Complete.")


if __name__ == "__main__":
    main()

    # print()
    # print(80*"=")
    # print(80*"=")
    # print()
