#!/usr/bin/env python
import sys, math
import time
import os
import numpy as np
import GraphiX
import utils as ut
num_contours = 5

possible_paths = ["RCOMP/GraphiX/", "GraphiX/"]


def remove_files(file_names):
    print "Done clean."
    for f in file_names:
         if ut.file_exists(f):
             os.remove(f)


def get_time(infilename):
    f = open(infilename, 'r')
    t = f.readline().split()[1]
    close_file(f)
    return t


def get_xy_max_min(infilename):
    f = open(infilename, 'r')
    contents = f.readlines()
    contour_edge = get_min_max(contents)
    x_min, x_max, y_min, y_max = get_xMax_yMax(contents)
    close_file(f)
    return ut.calculate_limits_aspect_ratio(x_min, x_max, y_min, y_max)


def get_x_y_coordinates(infilename):
    f = open(infilename, 'r')
    contents = f.readlines()
    nx, ny = get_Nx_Ny(contents)
    start_mesh_data, end_mesh_data = get_mesh_data_indices(nx, ny, contents)

    x_coord, y_coord = seperate_data(contents[start_mesh_data:end_mesh_data], nx, ny)
    return x_coord, y_coord


def get_data_table(infilename):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()
    nx, ny = get_Nx_Ny(contents)
    start_mesh_data, end_mesh_data = get_mesh_data_indices(nx, ny, contents)

    x_coord, y_coord = seperate_data(contents[start_mesh_data:end_mesh_data], nx, ny)

    start_velocity_data, end_velocity_data = get_velocity_start_end_indices(contents)
    u_vel, v_vel = seperate_data(contents[start_velocity_data + 1:end_velocity_data], nx, ny)

    close_file(f)
    contours = GraphiX.getdata(nx, ny,  int(contents[1].split()[0]), infilename, end_velocity_data + 1)

    contour_lim = get_contour_limits(contents[:100], int(contents[1].split()[0]))
    return nx, ny, x_coord, y_coord, u_vel, v_vel, contours, contour_lim


def get_specific_contour_data(infilename, cnt_name):
    f = open(infilename, 'r')
    contents = f.readlines()
    cnt_index = get_contour_index(cnt_name, contents[0:100])
    nx, ny = get_Nx_Ny(contents)
    start_mesh_data, end_mesh_data = get_mesh_data_indices(nx, ny, contents)
    start_contour_data = find_start_contour(contents, nx, ny, end_mesh_data)
    end_contour_data = nx * ny + start_contour_data
    return get_contour_array(cnt_index, contents[start_contour_data + 1:end_contour_data], nx, ny)


def get_contour_array(index, contents, nx, ny):
    x = np.ndarray([nx * ny])
    k = 0
    for i in contents:
        x[k] = float(i.split()[index])
        k = k + 1
    return x


def get_contour_index(name, contents):
    n_cont = int(contents[1].split()[0])
    for k in range(n_cont):
        if name == contents[k + 2].split()[0]:
            return k


def get_contour_limits(first_lines, n_cont):
    contours = {}
    cont_offset = 2
    for k in range(0, n_cont):
        fl = first_lines[k + cont_offset].split()
        contours[str(fl[0])] = {}
        contours[str(fl[0])]["min"] = fl[1]
        contours[str(fl[0])]["max"] = fl[2]
        contours[str(fl[0])]["id"] = k

    return contours


def seperate_data(data, nx, ny):
    x = np.ndarray([nx*ny])
    y = np.ndarray([nx*ny])
    for i in range(nx * ny):
        tmp = data[i].split()
        x[i] = tmp[0]
        y[i] = tmp[1]
    return x, y


def seperate_contours(data, nx, ny, num_contours):
    x = np.ndarray([num_contours, nx * ny])
    for i in range(nx * ny):
        tmp = data[i].split()
        for j in range(num_contours):
            x[j][i] = tmp[j]
    return x


def make_mesh_file(infilename, override=True):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()
    nx, ny = get_Nx_Ny(contents)
    if not check_file_exists(infilename):
        print "No file with the name {0}".format(infilename)
        return ""
    else:
        x_min, x_max, y_min, y_max = get_xMax_yMax(contents)
        f_name = get_mesh_name(infilename)
        if not check_file_exists(f_name) or override:
            start_mesh_data, end_mesh_data = get_mesh_data_indices(nx, ny, contents)
            x, y, ind = pre_mesh_2d(nx, ny, contents[start_mesh_data:end_mesh_data])
            GraphiX.create_mesh(nx, ny, f_name, x, y, ind)
           
            


       #  print "Time took for mesh: " + str(time.time() - t1)
        return f_name#, x_min, x_max, y_min, y_max + 0.1


def make_mesh_file_3d(infilename, override=True):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()
    nx, ny, nz = get_ny_nz(contents)
    f_name = get_mesh_name(infilename)

    if not check_file_exists(f_name) or override:
        x, y, z, ind = pre_mesh_3d(nx, ny, nz, contents[3:])
        create_mesh_3d(nx, ny, nz, x, y, z, ind, f_name)

        #new_mesh = create_new_segment(new_mesh)
        #f1 = open_write(f_name, new_mesh)
        #close_file(f1)

        # print "Writing to file: " + f_name
        #  print "Time took for mesh: " + str(time.time() - t1)
    return f_name  # , x_min, x_max, y_min, y_max + 0.1


def get_limits_file(name):
    if check_file_exists(name):
        f = open(name, "r")
        s = f.readlines()
        if s == []:
            return 0, 0
        start = s[0].split()[2]
        end = s[len(s) - 1].split()[2]
        f.close()
        return int(start), int(end)
    else:
        return 0, 0


def get_ny_nz(contents):
    a = contents[2].split(',')
    nx = int(a[1].split()[1])
    ny = int(a[2].split()[1])
    nz = int(a[3].split()[1])
    return nx, ny, nz


def create_mesh_2d_leeor(nx, ny, x, y, ind):
    title_data = [None] * 1
    title_data[0] = "#MESH\n"
    ttt = [None] * 1
    ttt[0] = "\n"
    angle_arr = angle_array1(nx, ny, x, y, ind)
    radial_arr = radial_array1(nx, ny, x, y, ind)

    return title_data + ttt + radial_arr + ttt + angle_arr


def make_velocity_file(infilename, override=True):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()

    Nx, Ny = get_Nx_Ny(contents)
    x_min, x_max, y_min, y_max = get_xMax_yMax(contents)
    contour_edge = get_min_max(contents)
    f_name = get_velocity_name(infilename)

    if not check_file_exists(f_name) or override:
        cell = (math.sqrt(pow(x_max - x_min, 2) + pow(y_max - y_min, 2)) / (math.sqrt(Nx * Ny)))
        max_velocity = get_max_velocity(contents)
        if max_velocity == 0:
            max_velocity = 1
        start_mesh_data, end_mesh_data = get_mesh_data_indices(Nx, Ny, contents)
        start_velocity_data, end_velocity_data, new_velocity = \
            velocity_segment(Nx, Ny, start_mesh_data, end_mesh_data, contents, max_velocity, cell)
        new_velocity = insert_nx_ny(contents) + new_velocity
        new_velocity = create_new_segment(new_velocity)
        f1 = open_write(f_name, new_velocity)

        close_file(f1)

   # print "Writing to file: " + f_name
   # print "Time took: " + str(time.time() - t1)
    return f_name, x_min, x_max, y_min, y_max, contour_edge


def make_contour_file(infilename, override=True):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()

    Nx, Ny = get_Nx_Ny(contents)
    contour_edge = get_min_max(contents)
    f_name = get_contour_name(infilename)
    if not check_file_exists(f_name) or override:
        start_mesh_data, end_mesh_data = get_mesh_data_indices(Nx, Ny, contents)
        end_velocity_data = find_start_contour(contents, Nx, Ny, end_mesh_data)
        end_contour, new_contour = contour_segment(Nx, Ny, contents, start_mesh_data, end_mesh_data, end_velocity_data)
        new_contour = insert_nx_ny(contents) + max_min_contours(contents) + new_contour
        new_contour = create_new_segment(new_contour)
        f1 = open_write(f_name, new_contour)
        close_file(f1)

    #print "Writing to file: " + f_name
   # print "Time took: " + str(time.time() - t1)
    return f_name, contour_edge


def make_vof_file(infilename, multiplier_x=1, multiplier_y=1, addition_name="", offset=2):
    t1 = time.time()
    f = open(infilename, 'r')
    contents = f.readlines()
    Nx, Ny = get_Nx_Ny(contents)
    f_name = get_vof_name(infilename + addition_name)
    len_vof = 0
    if not check_file_exists(f_name):
        start_mesh_data, end_mesh_data = get_mesh_data_indices(Nx, Ny, contents)
        new_vof, len_vof = vof_data_segment(contents[start_mesh_data + Nx*Ny: end_mesh_data], Nx, Ny, offset, multiplier_x, multiplier_y)
        new_vof = create_new_segment(new_vof)
        f1 = open_write(f_name, new_vof)
        close_file(f1)

    return f_name, len_vof


def heatmap_cython_file(x_data, y_data, cont_data, f_name, cont_name, c_min, c_max, addition_name="", offset=0):
    if not f_name.__contains__("_contour.gx"):
        f_name = get_contour_name(f_name)
        if not os.path.exists(f_name):
            print "No file found. Exiting"
            return ""
    f = open(f_name, 'r')
    contents = f.readlines()
    Nx = contents[0].split()[1]
    Ny = contents[1].split()[1]
    multiplier = offset
    f.close()
    f_hm = f_name.split("_contour.gx")[0] + "_" + str(cont_name) + "_" + addition_name + "heatmap.gx"
    GraphiX.heatmap(f_hm, int(Nx), int(Ny), cont_data, x_data, y_data, float(c_min), float(c_max), multiplier)
    return f_hm


def contour_cython_file(x_data, y_data, cont_data, f_name, cont_name, times, c_min, c_max):
    if not f_name.__contains__("_contour.gx"):
        f_name = get_contour_name(f_name)
        if not os.path.exists(f_name):
            print "No file found. Exiting"
            return ""
    f = open(f_name, 'r')
    contents = f.readlines()
    Nx = contents[0].split()[1]
    Ny = contents[1].split()[1]
    f.close()
    f_name = f_name.split(".gx")[0]
    f_cntr = get_contourcython_name(f_name, cont_name, times)
    GraphiX.calc_contour(f_cntr, int(Nx), int(Ny), int(times), float(c_max), float(c_min),
                         cont_data, x_data, y_data)
    return f_cntr


def get_heatmapcython_name(f_name, cont_name):
    f_name = create_graphix_tmp(f_name.split("_contour.gx")[0] +
                                "_" + str(cont_name) + "_" +"heatmap.gx")
    return f_name


def get_contourcython_name(f_name, cont_name, times):
    f_name = create_graphix_tmp(f_name + "_" + str(cont_name) + "_" + str(times) + ".gx")
    return f_name


def get_mesh_name(f_name):
    f_name = create_graphix_tmp(f_name + "_mesh.gx")
    return f_name


def get_vof_name(f_name):
    f_name = create_graphix_tmp(f_name + "_vof.gx")
    return f_name


def get_contour_name(f_name):
    f_name = create_graphix_tmp(f_name + "_contour.gx")
    return f_name


def get_velocity_name(f_name):
    f_name = create_graphix_tmp(f_name + "_velocity.gx")
    return f_name


def check_file_exists(name):
    if os.path.isfile(name):
        return True
    else:
        return False


def check_folder_exists(name):
    name = os.path.abspath(name)
    os.path.expanduser('~/')
    if os.path.exists(name):
        return True
    else:
        return False


def create_graphix_tmp(name):
    f_name = name.split('/')[len(name.split('/')) - 1]
    path1 = ""
    # for path in possible_paths:
    #     path = os.path.join(os.path.expanduser('~/'), path)
    #     if check_folder_exists(path):
    #         path1 = path
    #         break

    # path1 = os.path.join(path1, "tmp")
    # path1 = os.path.join(path1, f_name)
    path1 = os.path.join('/tmp', f_name)
    return path1


def insert_nx_ny(dataf):
    Nx, Ny = get_Nx_Ny(dataf)
    arr = [None] * 2
    arr[0] = "#Nx " + str(Nx) + "\n"
    arr[1] = "#Ny " + str(Ny) + "\n"
    return arr


def max_min_contours(dataf):
    num_contours = int(dataf[1].split()[0])
    arr = [None] * num_contours

    for i in range(num_contours):
        arr[i] = "#" + dataf[i + 2].split()[0] + " " + dataf[2 + i].split()[1] + " " + dataf[i + 2].split()[2] + "\n"
    return arr


def read_file(infilename):
    f = open(infilename, 'r')
    contents = f.readlines()

    Nx, Ny = get_Nx_Ny(contents)
    x_min, x_max, y_min, y_max = get_xMax_yMax(contents)
    cell = (math.sqrt(pow(x_max - x_min, 2) + pow(y_max - y_min, 2)) / (math.sqrt(Nx*Ny)))
    max_velocity = get_max_velocity(contents)
    if max_velocity == 0:
        max_velocity = 1
    # max_velocity =  ( max_velocity)
    # start_data is where the mesh data begins.
    # end_data is where the mesh data ends.
    start_mesh_data, end_mesh_data = get_mesh_data_indices(Nx, Ny, contents)

    # insert hashtags to the start of file for gnu to read.
    insert_hashtags_to_start(start_mesh_data, contents)


    #mesh_fixed(start_mesh_data, Nx, Ny, contents)
    # velocity segment
    t1 = time.time()
    start_velocity_data, end_velocity_data, new_velocity = \
        velocity_segment(Nx, Ny, start_mesh_data, end_mesh_data, contents, max_velocity, cell)
    t2 = time.time()
    print "time took for velocity segment: " + str(t2 - t1)
    # contours segment
    end_contour, new_contour = contour_segment(Nx, Ny, contents, start_mesh_data, end_mesh_data, end_velocity_data)
    t3 = time.time()
    print "time took for contour segment: " + str(t3 - t2)
    # mesh data segment
    new_mesh = mesh_data_segment(Nx, Ny, contents[start_mesh_data: end_mesh_data])
    t4 = time.time()
    print "time took for mesh segment: " + str(t4 - t3)
    end_mesh_data = (end_mesh_data - start_mesh_data) - Nx*Ny

    # insert the indices where the mesh, contour etc start and end
    new_start = start_segment(Nx, Ny, contents[0:start_mesh_data], start_mesh_data, end_mesh_data)

    contents = create_new_content(new_start,
                      new_mesh, new_velocity, new_contour, end_contour, contents)
    t5 = time.time()
    print "time took for create new content +start segment: " + str(t5 - t4)
    f1 = open_write(infilename + ".gnu", contents)
    t6 = time.time()
    print "time took for open write: " + str(t6 - t5)

    close_files(f1, f)
    t7 = time.time()
    print "time took for close: " + str(t7 - t6)
    return x_min, x_max, y_min, y_max, Nx, Ny


def find_start_contour(dataf, Nx, Ny, end_mesh):
    end_cont = end_mesh + Nx*Ny
    while not(dataf[end_cont].__contains__("CONTOURS")):
        end_cont = end_cont + 1
    return end_cont


def start_segment(Nx, Ny, contents, start_mesh_data, end_mesh_data):
    start_mesh_data = int(start_mesh_data) + 5
    end_mesh_data = int(start_mesh_data) + int(end_mesh_data) * 3 + 2 * Nx * Ny + 1
    start_velocity_data = int(end_mesh_data) + 4
    end_velocity_data = int(start_velocity_data + Nx * Ny)
    start_contour_data = int(end_velocity_data + 3)
    end_contour = int(start_contour_data) + Nx * Ny
    m_data = [None] * 1
    vel_data = [None] * 1
    con_data = [None] * 1
    tri_data = [None] * 1
    m_data[0] = "Mesh " + str(start_mesh_data) + " " + str(end_mesh_data) + " \n"
    vel_data[0] = "Velocity " + str(start_velocity_data) + " " + str(end_velocity_data) + " \n"
    con_data[0] = "Contour " + str(start_contour_data) + " " + str(end_contour) + " \n"
    tri_data[0] = "Triangle " + " \n"
    return contents + m_data + vel_data + con_data + tri_data


def contour_segment(Nx, Ny, contents, start_mesh, end_mesh, end_velocity_data):
    contents[end_velocity_data] = "#" + contents[end_velocity_data]
    end_contour_data = end_velocity_data + 1 + Nx * Ny

    contour_part = contents[end_velocity_data + 1: end_contour_data]
    mesh_part = contents[start_mesh: end_mesh]
    title_part = contents[end_velocity_data:end_velocity_data + 1]

    new_contour = insert_mesh_data_contour(contour_part, mesh_part, title_part)

    return end_contour_data, new_contour


def insert_mesh_data_contour(data_contour, data_mesh, title):
    for i in range(len(data_contour)):
        str_m = data_mesh[i]    .split()
        data_contour[i] = " " + str_m[0] + " " + str_m[1] + data_contour[i]
    ttt = [None] * 1
    ttt[0] = "\n"
    return ttt + ttt + title + data_contour


def get_xMax_yMax(content):
    st = content[1].split()
    return float(st[8]), float(st[9]), float(st[6]), float(st[7])


def get_max_velocity(contents):
    st = contents[1].split()
    return float(st[10])


# get the mesh'es indices (start & end)
def get_mesh_data_indices(Nx, Ny, contents):
    start_mesh_data = get_start_index_mesh_data(contents)
    end_mesh_data = get_end_index_mesh_data(Nx, Ny, start_mesh_data, contents)
    return start_mesh_data, end_mesh_data


# deals with the velocity part in the output file
def velocity_segment(Nx, Ny, start_mesh_data, end_mesh_data, contents, v_max, cell):
    start_velocity_data, end_velocity_data = get_velocity_start_end_indices(contents)
    # Let's pad VELOCITIES with #
    contents[start_velocity_data] = "#" + contents[start_velocity_data]
    # as far as I know, velocities number of data is Nx*Ny
    end_velocity_data = start_velocity_data + 1 + Nx * Ny

    velocity_part = contents[start_velocity_data + 1: end_velocity_data]
    mesh_part = contents[start_mesh_data:start_mesh_data + Nx * Ny]
    title_part = contents[start_velocity_data:start_velocity_data + 1]

    new_velocity = multiply_velocity(velocity_part, mesh_part, title_part, v_max, cell)
    return start_velocity_data, end_velocity_data, new_velocity


# insert more points for velocity data.
def multiply_velocity(data_velocity, data_mesh, title, v_max, cell):
    for i in range(len(data_velocity)):
        if i != len(data_velocity) - 1:
            nxt_pnt = data_mesh[i + 1]
            nxt_pnt = nxt_pnt.split()
        curr_pnt = data_mesh[i]
        curr_pnt = curr_pnt.split()
        cell_size = math.sqrt(math.pow(float(nxt_pnt[0]) - float(curr_pnt[0]), 2)
                              + math.pow(float(nxt_pnt[1]) - float(curr_pnt[1]), 2))
        if cell_size == 0:
            cell_size = 1
        if cell_size > 1:
            cell_size = 1
        str_vel = data_velocity[i].split()

        str_vel = normalize_velocity(str_vel,  v_max, cell)
        data_velocity[i] = "  " + curr_pnt[0] + " " + curr_pnt[1] + " " + str_vel[0] + " " + str_vel[1] + "\n"
    ttt = [None] * 1
    ttt[0] = "\n"
    return ttt + ttt + title + data_velocity


def normalize_velocity(str_vel, v_max, cell):
    str_vel[0] = float(str_vel[0])
    str_vel[1] = float(str_vel[1])
    v1 = math.sqrt(math.pow(str_vel[0], 2) + math.pow(str_vel[1], 2))
    #if v1 / v_max > cell_size:
    #  v_max = v_max**2
    v2 = math.log(v1 / v_max + cell)
    str_vel[0] = str_vel[0] / v_max
    str_vel[1] = str_vel[1] / v_max
    str_vel[0] = str(str_vel[0])
    str_vel[1] = str(str_vel[1])
    return str_vel


# multiply the number of points so that gnu will be able to plot the mesh.
# inserts as well a # Mesh for gnu processing.
def mesh_data_segment(Nx, Ny, dataf):
    title_data = [None] * 1
    title_data[0] = "#MESH\n"
    ttt = [None] * 1
    ttt[0] = "\n"
    angle_arr = angle_array(Nx, Ny, dataf)
    radial_arr = radial_array(Nx, Ny, dataf)

    if len(dataf[Nx*Ny:]) > 1:
        return title_data + ttt + angle_arr + ttt + radial_arr# + ttt + second_segment
    else:
        return title_data + angle_arr + ttt + radial_arr


def pre_mesh_3d(nx, ny, nz, contents):
    x = [None] * nx * ny * nz
    y = [None] * nx * ny * nz
    z = [None] * nx * ny * nz
    ind = [None] * nx * ny * nz
    i = 0
    for j in range(nx * ny * nz):
        tmp = contents[i].split()
        x[i] = tmp[0]
        y[i] = tmp[1]
        z[i] = tmp[2]
        ind[i] = tmp[3]
        i = i + 2
    return x, y, z, ind


def pre_mesh_2d(nx, ny, contents):
    x = np.ndarray([nx*ny], dtype=np.double)
    y = np.ndarray([nx*ny], dtype=np.double)
    ind = np.ndarray([nx*ny], dtype=np.int)

    for i in range(nx * ny):
        tmp = contents[i].split()
        x[i] = float(tmp[0])
        y[i] = float(tmp[1])
        ind[i] = int(tmp[2])
    return x, y, ind


def create_mesh_3d(nx, ny, nz, x, y, z, index, f1):
    f = open(f1, "w")
    ind = 0
    #first segment
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                ind = i + j * nx + k * nx * ny
                f.write(x[ind] + " " + y[ind] + " " + z[ind] + " " + index[ind] + "\n")
            f.write("\n")
    f.write("\n")
    for k in range(nz):
        for j in range(nx):
            for i in range(ny):
                ind = i * nx + j + k * nx * ny
                f.write(x[ind] + " " + y[ind] + " " + z[ind] + " " + index[ind] + "\n")
            f.write("\n")
    f.write("\n")
    for k in range(nx):
        for j in range(ny):
            for i in range(nz):
                ind = i * nx * ny + j * nx + k
                f.write(x[ind] + " " + y[ind] + " " + z[ind] + " " + index[ind] + "\n")
            f.write("\n")


def radial_array(Nx, Ny, dataf):
    radial_arr = ["0"] * (Nx * Ny)
    #zogi.
    for i in range(0, Ny, 2):
        for j in range(0, Nx):
            kn = i * Nx + j
            km = (i - 1) * Nx + j - 1
            if i == 0:
                km = j - 1

            if j == 0:
                radial_arr[kn] = dataf[kn]
            else:
                if int(dataf[kn - 1].split()[2]) < int(dataf[km].split()[2]):
                    radial_arr[kn] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1]\
                                    + " " + dataf[kn - 1].split()[2] + "\n"
                else:
                    radial_arr[kn] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                                    + " " + dataf[km].split()[2] + "\n"

    #odd
    t = 0
    for i in range(1, Ny, 2):
        t = i * Nx
        for j in range(Nx - 1, -1, -1):
            kn = i * Nx + j
            km = (i - 1) * Nx + j
            if j == Nx - 1:
                radial_arr[t] = dataf[kn]
            else:
                if dataf[kn].split()[2] < dataf[km].split()[2]:
                    radial_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                                     + " " + dataf[kn].split()[2] + "\n"
                else:
                    radial_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                                     + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    for i in range(Ny):
        radial_arr[i*Nx - 1] += "\n"

    return radial_arr


def angle_array(Nx, Ny, dataf):
    angle_arr = ["0"] * (Nx * Ny)
    # even
    for i in range(0, Nx, 2):
        t = i * Ny
        for j in range(0, Ny):
            kn = j * Nx + i
            km = kn - Nx - 1
            if i == 0:
                km = kn
            if j == 0:
                angle_arr[t] = dataf[kn]
            else:
                a = min(dataf[kn - Nx].split()[2], dataf[km].split()[2])
                angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                               + " " + a + "\n"
                # if int(dataf[kn - Nx].split()[2]) < int(dataf[km].split()[2]):
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                #                      + " " + dataf[kn - Nx].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    # odd
    t = 0
    for i in range(1, Nx, 2):
        t = i * Ny
        for j in range(Ny - 1, -1, -1):
            kn = j * Nx + i
            km = kn - 1
            if j == Ny - 1:
                angle_arr[t] = dataf[kn]
            else:
                a = min(dataf[kn].split()[2], dataf[km].split()[2])
                angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                               + " " + a + "\n"
                # if dataf[kn].split()[2] < dataf[km].split()[2]:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[kn].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    for i in range(Nx):
        angle_arr[i*Ny - 1] += "\n"

    return angle_arr


def angle_array1(nx, ny, x, y, ind):
    angle_arr = ["0"] * (nx * ny)
    # even
    for i in range(0, nx, 2):
        t = i * ny
        for j in range(0, ny):
            kn = j * nx + i
            km = kn - nx - 1
            if i == 0:
                km = kn
            if j == 0:
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                a = min(ind[kn - nx], ind[km])
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(a) + "\n"
                # if int(dataf[kn - Nx].split()[2]) < int(dataf[km].split()[2]):
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                #                      + " " + dataf[kn - Nx].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    # odd
    t = 0
    for i in range(1, nx, 2):
        t = i * ny
        for j in range(ny - 1, -1, -1):
            kn = j * nx + i
            km = kn - 1
            if j == ny - 1:
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                a = min(ind[kn], ind[km])
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(a) + "\n"

                # if dataf[kn].split()[2] < dataf[km].split()[2]:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[kn].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    for i in range(nx):
        angle_arr[i*ny - 1] += "\n"
    return angle_arr


def radial_array1(nx, ny, x, y, ind):
    radial_arr = ["0"] * (nx * ny)
    #zogi.
    for i in range(0, ny, 2):
        for j in range(0, nx):
            kn = i * nx + j
            km = (i - 1) * nx + j - 1
            if i == 0:
                km = j - 1
            if j == 0:
                radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                if int(ind[kn - 1]) < int(ind[km]):
                    radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn - 1]) + " " + "\n"
                else:
                    radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[km]) + " " + "\n"


    #odd
    t = 0
    for i in range(1, ny, 2):
        t = i * nx
        for j in range(nx - 1, -1, -1):
            kn = i * nx + j
            km = (i - 1) * nx + j
            if j == nx - 1:
                radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                if int(ind[kn]) < ind[km]:
                    radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
                else:
                    radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[km]) + " " + "\n"
            t = t + 1

    for i in range(ny):
        radial_arr[i*nx - 1] += "\n"

    return radial_arr


def angle_array3d(nx, ny, x, y, z, ind):
    angle_arr = ["0"] * (nx * ny)
    # even
    for i in range(0, nx, 2):
        t = i * ny
        for j in range(0, ny):
            kn = j * nx + i
            km = kn - nx - 1
            if i == 0:
                km = kn
            if j == 0:
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                a = min(ind[kn - nx], ind[km])
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(a) + "\n"
                # if int(dataf[kn - Nx].split()[2]) < int(dataf[km].split()[2]):
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] \
                #                      + " " + dataf[kn - Nx].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    # odd
    t = 0
    for i in range(1, nx, 2):
        t = i * ny
        for j in range(ny - 1, -1, -1):
            kn = j * nx + i
            km = kn - 1
            if j == ny - 1:
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn]) + " " + "\n"
            else:
                a = min(ind[kn], ind[km])
                angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(a) + "\n"

                # if dataf[kn].split()[2] < dataf[km].split()[2]:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[kn].split()[2] + "\n"
                # else:
                #     angle_arr[t] = " " + dataf[kn].split()[0] + " " + dataf[kn].split()[1] + " " + dataf[km].split()[2] + "\n"
            t = t + 1

    for i in range(nx):
        angle_arr[i*ny - 1] += "\n"
    return angle_arr


def radial_array3d(nx, ny, x, y,z, ind):
    radial_arr = ["0"] * (nx * ny)

    for i in range(0, nx, 1):
        for j in range(0, ny, 1):
            kn = i * nx + j
            radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn]) + " " + "\n"


    # #zogi.
    # for i in range(0, ny, 2):
    #     for j in range(0, nx):
    #         kn = i * nx + j
    #         km = (i - 1) * nx + j - 1
    #         if i == 0:
    #             km = j - 1
    #         if j == 0:
    #             radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn]) + " " + "\n"
    #         else:
    #             if int(ind[kn - 1]) < int(ind[km]):
    #                 radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn - 1]) + " " + "\n"
    #             else:
    #                 radial_arr[kn] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[km]) + " " + "\n"
    #
    #
    # #odd
    # t = 0
    # for i in range(1, ny, 2):
    #     t = i * nx
    #     for j in range(nx - 1, -1, -1):
    #         kn = i * nx + j
    #         km = (i - 1) * nx + j
    #         if j == nx - 1:
    #             radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) +  " " + str(ind[kn]) + " " + "\n"
    #         else:
    #             if int(ind[kn]) < ind[km]:
    #                 radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[kn]) + " " + "\n"
    #             else:
    #                 radial_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(z[kn]) + " " + str(ind[km]) + " " + "\n"
    #         t = t + 1

    for i in range(ny):
        radial_arr[i*nx - 1] += "\n"

    return radial_arr


def get_velocity_start_end_indices(content):
    i = 0
    while content[i] != "VELOCITIES\n":
        i = i + 1
    start_ind = i
    i = 0
    while content[i] != "CONTOURS\n":
        i = i + 1
    return start_ind, i


def vof_data_segment(dataf, nx, ny, offset, mirror_x, mirror_y):
    new_segment = [None] * len(dataf)
    for i in range(len(dataf)):

        st = dataf[i].split()
        st[0] = str(mirror_x * float(st[0]))
        st[2] = str(mirror_x * float(st[2]))
        st[1] = str(mirror_y * float(st[1]))
        st[3] = str(mirror_y * float(st[3]))

        new_segment[i] = "set object {0} polygon front from {2},{1} to {4},{3} to {2},{1} fs solid border lc" \
                         " \"{5}\" lw 1.8\n".format(offset*nx*ny - i, st[0], st[1], st[2], st[3], "white")
    return new_segment, len(dataf) - 1

# def multiply_points_second_segment(dataf):
#     new_segment = [None] * 2 * len(dataf)
#     for i in range(len(dataf)):
#         st = dataf[i].split()
#         new_segment[2 * i + 1] =
#         new_segment[2 * i] =
#     return new_segment

# insert hashtag to all lines that come before the datas
# assuming get_Nx_Ny was operated before.
def insert_hashtags_to_start(start_data, contents):
    for i in range(start_data):
        contents[i] = "#" + contents[i]
    return contents


# returns Nx points and Ny points of the mesh.
def get_Nx_Ny(content):
    for i in range(len(content)):
        # assuming that the 2nd lines contains Nx & Ny.
        if i == 1:
            st = content[i].split()
            break
    # assuming Nx is the 3rd char (after # padding) and Ny is the 4th char
    return int(st[1]), int(st[2])


def get_nx_ny_nz(content):
    for i in range(len(content)):
        if i == 1:
            st = content[i].split()
            break
            # assuming Nx is the 3rd char (after # padding) and Ny is the 4th char
        return int(st[1]), int(st[2]), int(st[3])


# contents -is the whole file data
# returns the line in which the mesh data begins
def get_start_index_mesh_data(content):
    for i in range(len(content)):
        # assuming the data starts when there is 2 spaces.
        if content[i][0] == ' ' and content[i][1] == ' ' and content[i][2] != ' ':

            return int(i)
        if content[i][0] == ' ' and content[i][1] == '-' and content[i][2] != ' ':
            return int(i)


def get_index_mesh_3d(content, nx, ny, nz):
    start = 0
    end = 0
    return 2, len(content)
    # for i in range(len(content)):
    #     # assuming the data starts when there is 2 spaces.
    #     if content[i][0] == ' ' and content[i][1] == ' ' and content[i][2] != ' ':
    #         start = int(i)
    #     if content[i][0] == ' ' and content[i][1] == '-' and content[i][2] != ' ':
    #         start = int(i)
    # i = nx * ny * nz
    # # no connecting line in the middle of mesh
    # while contents[start + i] != "VELOCITIES\n":
    #     i = i + 1
    # end = int(start_index + i)
    # return start, end


# returns the end index of points, we check for String
def get_end_index_mesh_data(Nx, Ny, start_index, contents):
    i = Nx * Ny - 1
    # no connecting line in the middle of mesh
    while contents[start_index + i] != "VELOCITIES\n":
        i = i + 1
    return int(start_index + i)


#  combines all the data to form a new output file that is suitable for gnu
def create_new_content(new_start, new_mesh, new_velocity, new_contour, new_end, contents):
    contents = new_start + new_mesh + new_velocity + new_contour + contents[new_end:]
    contents = "".join(contents)
    return contents


def create_new_segment(dataf):
    dataf = "".join(dataf)
    return dataf


# close the original and new output files
def close_files(f1, f2):
    f1.close()
    f2.close()


# close the original and new output files
def close_file(f1):
    f1.close()


# opens a new file .
def open_write(file_name, contents):
    f1 = open(file_name, "w")
    f1.write(contents)
    return f1


def get_min_max(contents):
    num_contours = int(contents[1].split()[0])
    arr = [None] * num_contours
    for i in range(num_contours):
        st = contents[i + 2].split()
        arr[i] = st[1:]
    return arr


def prepare_contour_array(data, cont_num):
    i = 0
    while data[i] != "#CONTOURS\n":
        i = i + 1
    i = i + 1
    s = len(data) - i
    x_data = np.ndarray(s, dtype=np.float)
    y_data = np.ndarray(s, dtype=np.float)
    cont_data = np.ndarray(s, dtype=np.float)
    for j in range(s):
        line = data[j + i].split()
        x_data[j] = float(line[0])
        y_data[j] = float(line[1])
        cont_data[j] = float(line[cont_num + 1])
    return cont_data, x_data, y_data


def get_cmax(dataf, cont_name):
    i = 0
    while not(dataf[i].split()[0].__contains__(cont_name)):
        i = i + 1
    return dataf[i].split()[1], dataf[i].split()[2]


def read_mass_diag(nx, ny, mat_id, list_points, path):
    mat_id = int(mat_id - 1)
    mass_file = os.path.join(os.path.split(path)[0], "mass_diag")
    sum_mass = 0.0
    f = open(mass_file)
    file_read = f.readlines()
    nmats = len(file_read[0].split())
    sum_mass = float(0)
    for k in list_points:
        sum_mass = sum_mass + np.float64(file_read[k].split()[mat_id])
    f.close
    return sum_mass
















      






if __name__ == '__main__':
    try:
        infilename = sys.argv[1]
    except:
        sys.exit(1)

    f = open(infilename, 'r')
    contents = f.readlines()

    contour_edge = get_min_max(contents)
    x_min, x_max, y_min, y_max = get_xMax_yMax(contents)
    f.close()
    ff = make_mesh_file(infilename)























