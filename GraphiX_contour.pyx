# algorithm taken from isoline marching squares !
# i_j is the lower left cell 1 or a
# i1_j is the upper left 2 or b
# i_j1 is lower right 3 or c
# i1_j1 is upper right 4 or d


from libc.stdlib cimport malloc,free, atof
from libc.stdio cimport fopen, fclose, fwrite, fscanf, FILE, fseek, SEEK_CUR, printf, fgets
cimport numpy as np
import numpy as np
cimport openmp
import math
from cython.parallel cimport prange

cpdef calc_contour(char[] f_name, int nx, int ny, int n_cont, double c_max, double c_min
, double [:]cont, double [:]x, double [:]y):
    cdef int num_contours = n_cont
    cdef int i, j, k, i_j, i1_j, i_j1, i1_j1, ii, jj, i_ja, i_jb, i1_jb, i1_ja, nnn
    cdef double dq = (c_max - c_min)/(num_contours)
    cdef int ncn = num_contours + 1
    cdef double xx
    cdef double xco[4]
    cdef double yco[4]
    cdef int pnts = 0
    cdef int* num_elem = <int*> malloc(sizeof(int) * num_contours + 2)
    cdef double* con = <double*> malloc(sizeof(double) * (num_contours + 2))
    cdef double** x1_cont = <double**> malloc(sizeof(double*) * (num_contours + 1))
    cdef double** x2_cont = <double**> malloc(sizeof(double*) * (num_contours + 1))
    cdef double** y1_cont = <double**> malloc(sizeof(double*) * (num_contours + 1))
    cdef double** y2_cont = <double**> malloc(sizeof(double*) * (num_contours + 1))

    for i in range(num_contours + 1):
        x1_cont[i] = <double*> malloc(sizeof(double) * nx*ny)
        x2_cont[i] = <double*> malloc(sizeof(double) * nx*ny)
        y1_cont[i] = <double*> malloc(sizeof(double) * nx*ny)
        y2_cont[i] = <double*> malloc(sizeof(double) * nx*ny)
    for k in range(0, ncn):
        con[k] = c_min + k * dq
        num_elem[k] = 0

    for j in range (1, ny - 1):
        i_j = (j - 1) * nx + 1
        i_j1 = i_j + nx
        for i in range (1, nx - 2):
            i1_j = i_j + 1
            i1_j1 = i_j1 + 1
            nnn = 0
            for k in range (1, ncn):
                k1 = 0
                k2 = 0
                k3 = 0
                k4 = 0
                if cont[i_j] <= con[k]:
                    k1 = 1
                if cont[i1_j] <= con[k]:
                    k2 = 1
                if cont[i_j1] <= con[k]:
                    k3 = 1
                if cont[i1_j1] <= con[k]:
                    k4 = 1
                # case 0 and 15, no need to draw line
                if (((k1*k2*k3*k4) != 0) or ((k1+k2+k3+k4) == 0)):
                    continue
                i_jb = i_j
                i_ja = i_j1
                if nnn == 0:
                    # calculate center of the known points because dror did it
                    for ii in range(1,3):
                        for jj in range (1,3):
                            i1_jb = i_jb + 1
                            i1_ja = i_ja + 1
                            xco[nnn] = 0.25 * (x[i1_jb] + x[i1_ja] + x[i_ja] + x[i_jb])
                            yco[nnn] = 0.25 * (y[i1_jb] + y[i1_ja] + y[i_ja] + y[i_jb])
                            i_ja = i1_ja
                            i_jb = i1_jb
                            nnn = nnn + 1
                        i_jb = i_j1
                        i_ja = i_j1 + nx
                # there might be a better way but for clearess of the code it will be like this.
                # the case's number is as the case presented in wikipedia "isoline" square march

                # case 1 and XX X,0,0,0 or 0,1,1,1
                if (k1 == 1 and k2 == 0 and k3 == 0 and k4 == 0) or \
                     (k1 == 0 and k2 == 1 and k3 == 1 and k4 == 1):
                    pnts = num_elem[k]

                    # point between 1 and 3 (see above)
                    xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    # point between 1 and 2 (see above)
                    xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    x2_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    y2_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    num_elem[k] = num_elem[k] + 1

                # case 2 and 13 0,0,1,0 or 1,1,0,1
                elif (k1 == 0 and k2 == 0 and k3 == 1 and k4 == 0) or \
                        (k1 == 1 and k2 == 1 and k3 == 0 and k4 == 1):
                    # maybe need to flip the indices, if it ain't working
                    pnts = num_elem[k]
                    # point between 1 and 3
                    xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    # point between 3 and 4
                    xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    num_elem[k] = num_elem[k] + 1

                # case 3 and 12 1,0,1,0 or 0,1,0,1
                elif (k1 == 1 and k2 == 0 and k3 == 1 and k4 == 0) or \
                        (k1 == 0 and k2 == 1 and k3 == 0 and k4 == 1):
                    pnts = num_elem[k]
                    # point between 1 and 2
                    xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    # point between 3 and 4
                    xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    num_elem[k] = num_elem[k] + 1

                # case 4 and 11 0,0,0,1 or 1,1,1,0
                elif (k1 == 0 and k2 == 0 and k3 == 0 and k4 == 1) or \
                        (k1 == 1 and k2 == 1 and k3 == 1 and k4 == 0):
                    pnts = num_elem[k]

                    # point between 2 and 4
                    xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    x1_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    y1_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    # point between 3 and 4
                    xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    num_elem[k] = num_elem[k] + 1

                # case 10 double points  0,1,1,0
                elif k1 == 0 and k2 == 1 and k3 == 1 and k4 == 0:
                    pnts = num_elem[k]
                    # point between 1 and 2
                    xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    x2_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    y2_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    # point between 1 and 3
                    xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    num_elem[k] = num_elem[k] + 1

                    pnts = num_elem[k]

                    # point between 2 and 4
                    xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    x1_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    y1_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    # point between 3 and 4
                    xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    num_elem[k] = num_elem[k] + 1
                    # now for the second line
                    #pnts = num_elem[k]
                    # point between 1 and 3
                    #xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    #x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    #y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    # point between 3 and 4
                    #xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    #x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    #y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    #num_elem[k] = num_elem[k] + 1

                    #pnts = num_elem[k]
                    # point between 1 and 2
                    #xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    #x1_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    #y1_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    # point between 2 and 4
                    #xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    #x2_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    #y2_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    #num_elem[k] = num_elem[k] + 1

                # case 6 and 9 0,0,1,1 or 1,1,0,0
                elif (k1 == 0 and k2 == 0 and k3 == 1 and k4 == 1) or \
                        (k1 == 1 and k2 == 1 and k3 == 0 and k4 == 0):
                    pnts = num_elem[k]
                    # point between 1 and 3
                    xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    # point between 2 and 4
                    xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    x2_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    y2_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    num_elem[k] = num_elem[k] + 1

                # case 7 and 8 1,0,1,1 or 0,1,0,0
                elif (k1 == 1 and k2 == 0 and k3 == 1 and k4 == 1) or \
                        (k1 == 0 and k2 == 1 and k3 == 0 and k4 == 0):
                    pnts = num_elem[k]
                    # point between 1 and 2
                    xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    # point between 2 and 4
                    xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    x2_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    y2_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    num_elem[k] = num_elem[k] + 1

                # case 5 1,0,0,1
                elif k1 == 1 and k2 == 0 and k3 == 0 and k4 == 1:
                    pnts = num_elem[k]
                    # point between 1 and 2
                    xx = (con[k] - cont[i_j]) / (cont[i1_j] - cont[i_j])
                    x2_cont[k][pnts] = xco[0] + xx * (xco[1] - xco[0])
                    y2_cont[k][pnts] = yco[0] + xx * (yco[1] - yco[0])

                    # point between 1 and 3
                    xx = (con[k] - cont[i_j]) / (cont[i_j1] - cont[i_j])
                    x1_cont[k][pnts] = xco[0] + xx * (xco[2] - xco[0])
                    y1_cont[k][pnts] = yco[0] + xx * (yco[2] - yco[0])

                    num_elem[k] = num_elem[k] + 1

                    pnts = num_elem[k]

                    # point between 2 and 4
                    xx = (con[k] - cont[i1_j]) / (cont[i1_j1] - cont[i1_j])
                    x1_cont[k][pnts] = xco[1] + xx * (xco[3] - xco[1])
                    y1_cont[k][pnts] = yco[1] + xx * (yco[3] - yco[1])

                    # point between 3 and 4
                    xx = (con[k] - cont[i_j1]) / (cont[i1_j1] - cont[i_j1])
                    x2_cont[k][pnts] = xco[2] + xx * (xco[3] - xco[2])
                    y2_cont[k][pnts] = yco[2] + xx * (yco[3] - yco[2])

                    num_elem[k] = num_elem[k] + 1

            i_j = i1_j
            i_j1 = i1_j1

    # 2 options to do this, let's sort by values of k.
    # i.e for gnuplot, each value k will be written together and be connected
    # f_name = "../data/test.gx"
    f1 = open(f_name, "w")
   # f1.write("set palette rgbformulae 33,13,10\n")
    for k in range (0, num_contours):
        f1.write("\n\n")
        for i in range (0, num_elem[k]):
            f1.write(str(x1_cont[k][i]) + " " + str(y1_cont[k][i]) + " " + str(con[k + 1]) + "\n"
            + str(x2_cont[k][i]) + " " + str(y2_cont[k][i]) + " " + str(con[k+1]) + "\n\n")
    f1.close()
    i = 0
    for i in range(num_contours + 1):
        free(x1_cont[i])
        free(x2_cont[i])
        free(y1_cont[i])
        free(y2_cont[i])

    free(x1_cont)
    free(x2_cont)
    free(y1_cont)
    free(y2_cont)

cpdef heatmap(char[]f_name, int nx, int ny, double [:]cont, double [:]x, double [:]y, double min_contour,double max_contour, int multiplier):
    cdef int i,j,k
    cdef int index_1,index_2,index_3,index_4
    cdef double cont1

    f1 = open(f_name , "w");
    f1.write("set cbrange[" + str(min_contour)+":"+str(max_contour)+"]\n")

    for i in range(0, ny - 1):
        for j in range(0, nx - 1):
            index_1 = j + i * nx
            index_2 = index_1 + 1
            index_4 = index_1 + nx
            index_3 = index_4 + 1
            cont1 = cont[index_1]

            f1.write("set object {0} polygon from {1},{2} to {3},{4} to {5},{6} to {7},{8} to {1},{2} fs solid 1 fc palette cb {9}\n".
                     format(multiplier*nx*ny - (j + i*nx), y[index_1], x[index_1], y[index_2], x[index_2], y[index_3], x[index_3], y[index_4], x[index_4], cont1 ))
    #f1.write("\n plot 0 palette\n")

    f1.close()


cpdef getdata(int nx, int ny, int n_cont, char[] f_name, int offset):
    cdef double[:, :] cont_data = np.zeros((n_cont, nx * ny))
    cdef double *a
    cdef char* fname = f_name
    cdef char stam[1024]
    cdef FILE* cfile
    cdef int i,j
    with nogil:
        cfile = fopen(fname, "r")
        i = 0
        while i != offset:
            fgets(&stam[0], 1024, cfile)
            i = i + 1
        i = 0
        for j in range(nx * ny):
            for i in range(n_cont):
                fscanf(cfile,'%s',&stam);
                cont_data[i][j] = atof(stam)



    return cont_data

cpdef area_ptc(double x1, double y1, double x2, double y2, double x3,double y3):
    return (x2 - x1) * (y3 - y1) - (y2 - y1)*(x3 - x1)

def convert_1d_to_2d_i(int k, int nx):
    j = int(k / nx)
    i = int(k - j * nx)
    return int(i), int(j)

cpdef position_to_cell(double x, double y, double[:] x_coord, double[:] y_coord, int nx, int ny):
    cpdef int nyp = ny
    cpdef int nxp = nx
    cpdef int nxpy = (nyp - 1) * nxp - 2
    cpdef int i = nxpy

    found = False
    # We calculate the triangle area that is formed from the point clicked, to one of the
    # vertices of the 4 point mesh.
    # If the point is in the rectangle, all of the signs are + + + + (notice the order of the
    # x1,x2,x3... in the function call)
    # Same scheme is in the leeor.
    while i >= 0 and not found:
        s1 = math.copysign(1, area_ptc(x, y, x_coord[i], y_coord[i],
                                          x_coord[i + 1], y_coord[i + 1]))
        s2 = math.copysign(1, area_ptc(x, y, x_coord[i + 1], y_coord[i + 1],
                                          x_coord[i + 1 + nxp], y_coord[i + 1 + nxp]))
        s3 = math.copysign(1, area_ptc(x, y, x_coord[i + 1 + nxp], y_coord[i + 1 + nxp],
                                          x_coord[i + nxp], y_coord[i + nxp]))
        s4 = math.copysign(1, area_ptc(x, y, x_coord[i + nxp], y_coord[i + nxp],
                                          x_coord[i], y_coord[i]))
        n, m = convert_1d_to_2d_i(i, nx)
        if s1 == s2 and s1 == s3 and s1 == s4 and n != nxp - 1:
            found = True
        i = i - 1
    if not found:
        return -1
    return int(i) + 1


cpdef create_mesh(int nx, int ny, char [] f_name, double [:]x
, double [:]y, long [:] ind):
    radial_arr = ["0"] * (nx * ny)
    angle_arr = ["0"] * (nx * ny)
    f1 = open(f_name , "w");

    for i in range(0, ny, 1):
        if i % 2 == 0:
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

        else:
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
    #zogi.


    for i in range(ny):
        radial_arr[i*nx - 1] += "\n"

    # even
    for i in range(0, nx, 1):
        if i % 2 == 0:
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
        else:
            t = i * ny
            for j in range(ny - 1, -1, -1):
                kn = j * nx + i
                km = kn - 1
                if j == ny - 1:
                    angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(ind[kn]) + " " + "\n"
                else:
                    a = min(ind[kn], ind[km])
                    angle_arr[t] = " " + str(x[kn]) + " " + str(y[kn]) + " " + str(a) + "\n"
                t = t + 1

    for i in range(nx):
        angle_arr[i*ny - 1] += "\n"

    f1.write("#MESH\n")
    f1.writelines(radial_arr)
    f1.write("\n")
    f1.writelines(angle_arr)
    f1.close()