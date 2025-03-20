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

    case_index = 10
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
    print(f"{case_mesh.coord_cent=}")
    print(f"{case_mesh.coord_bound_min=}")
    print(f"{case_mesh.coord_bound_max=}")
    print(80*"-")
    print(f"{case_mesh.node_count=}")
    print(f"{case_mesh.elem_count=}")
    print(f"{case_mesh.coords.shape=}")
    print(f"{case_mesh.connectivity.shape=}")
    print(f"{case_mesh.fields_by_node.shape=}")


if __name__ == "__main__":
    main()