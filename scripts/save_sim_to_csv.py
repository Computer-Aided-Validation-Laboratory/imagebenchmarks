from pathlib import Path
import numpy as np
import pyvale
import imagebenchmarks as ib

def main() -> None:
    sim_path = ib.get_sim_path()
    sim_file = sim_path / "cylinder_m1_out.e"

    mesh_world = pyvale.create_camera_mesh(sim_file,
                                           ib.const.FIELD_KEY,
                                           ib.const.COMPONENTS,
                                           ib.const.SPAT_DIMS)

    save_path = Path.home() / "zig-learn" / "rasteriser" / "data"

    print(80*"-")
    print(f"{mesh_world.coords.shape=}")
    print(f"{mesh_world.connectivity.shape=}")
    print(f"{mesh_world.fields_by_node.shape=}")
    print(80*"-")

    np.savetxt(save_path/'coords.csv',mesh_world.coords, delimiter=',')
    np.savetxt(save_path/'connectivity.csv',mesh_world.connectivity, delimiter=',')
    np.savetxt(save_path/'field_disp_x.csv',mesh_world.fields_by_node[:,:,0], delimiter=',')
    np.savetxt(save_path/'field_disp_y.csv',mesh_world.fields_by_node[:,:,1], delimiter=',')
    np.savetxt(save_path/'field_disp_z.csv',mesh_world.fields_by_node[:,:,2], delimiter=',')


if __name__ == "__main__":
    main()