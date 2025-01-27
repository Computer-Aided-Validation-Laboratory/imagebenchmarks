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

    (case_ident,case_mesh,case_camera) = ib.load_benchmark_by_index(case_index)
    print()
    print(80*"-")
    print(f"{case_ident=}")
    print(case_mesh)
    print(case_camera)
    print(80*"-")

    case_tag = case_list[-1]
    (case_ident,case_mesh,case_camera) = ib.load_benchmark_by_tag(case_tag)
    print()
    print(80*"-")
    print(f"{case_ident=}")
    print(case_mesh)
    print(case_camera)
    print(80*"-")


if __name__ == "__main__":
    main()