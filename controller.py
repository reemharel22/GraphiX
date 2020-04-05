import process_interface as p_interface
import file_handler as fh
import os
import sys, math
import numpy as np
from threading import Thread
import utils as ut
import time
import contours
import file_handler_leeor as fhl


class Controller(object):

    def __init__(self, name="", winId=0, qt=False):
        self.last_command = ""
        self.x_coord = np.array([])
        self.y_coord = np.array([])
        self.u_vel = np.array([])
        self.v_vel = np.array([])
        self.plot_time = 0
        self.contour_limit = {}
        self.vof_offset = [2, 0]
        self.file_vof_x_name = ""
        self.file_vof_y_name = ""
        self.file_vof_xy_name = ""
        self.with_additional_plot = False
        self.file_vof_additional_name = ""
        self.vof_mirror_x_offset = [3, 0]
        self.vof_mirror_xy_offset = [4, 0]
        self.vof_mirror_y_offset = [5, 0]
        self.vof_additional_plot = [XX, 0]
        self.hm_offset = [7, 0]
        self.hm_mirror_x_offset = [9, 0]
        self.hm_mirror_y_offset = [11, 0]
        self.hm_mirror_xy_offset = [13, 0]
        self.hm_additional_offset = [XX, 0]
        self.additional_file_name = ""
        self.nx = 0
        self.lines_id = [None]
        self.x_min = 0
        self.x_max = 0
        self.num_vofs = 0
        self.y_max = 0
        self.y_min = 0
        self.ny = 0
        self.with_vof = True
        self.vof_num = 0
        self.file_names = []
        self.with_mirror_x = False
        self.with_mirror_y = False
        self.file_mesh_name = ""
        self.file_contour_name = "none"
        self.file_velocity_name = ""
        self.override = True
        self.file_vof_name = ""
        self.width = 1250
        self.contours = contours.Contours()
        self.height = 663
        self.proc_interface = p_interface.Gnuplot(True, winId, qt)
        self.file_name = name
        self.first_time = True
        self.plot_names = []
        self.fh = fhl.file_handler_leeor()

    def set_limits(self, x_min, x_max, y_min, y_max):
        self.proc_interface.set_x_limit(x_min, x_max, True)
        self.proc_interface.set_y_limit(y_min, y_max, True)

    def reset_limits(self, replot=True):
        self.default_x_min, self.default_x_max, self.default_y_min, self.default_y_max \
            = ut.calculate_limits_aspect_ratio(self.default_x_min, self.default_x_max, self.default_y_min, self.default_y_max, w=self.width, h=self.height)
        self.proc_interface.set_x_limit(self.default_x_min, self.default_x_max, replot=replot)
        self.proc_interface.set_y_limit(self.default_y_min, self.default_y_max, replot=replot)

    def get_limits(self):
        return self.proc_interface.get_current_limits()

    def pre_plot(self, f_name):
        self.unplot_vof(force=True)
        if not f_name.__eq__(self.file_name) or self.first_time:
            self.file_name = f_name
            self.plot_names.append(f_name)
            self.extract_data(f_name)
            self.file_names.append(self.file_vof_name)
        else:
            f_name = self.file_name
        if self.with_vof:
            self.plot_vof()
            self.file_names.append(self.file_vof_name)
        if self.last_command == "heatmap":
            # the limits of the heatmap object names
            self.unplot_heatmap()

    def unplot_heatmap(self):
        self.proc_interface.unplot_objects(self.nx * self.ny * (self.hm_offset[0] - 1),
                                           self.nx * self.ny * self.hm_offset[0])
        if self.with_mirror_x:
            self.proc_interface.unplot_objects(self.nx * self.ny * (self.hm_mirror_x_offset[0] - 1),
                                               self.nx * self.ny * self.hm_mirror_x_offset[0])
        if self.with_mirror_y:
            self.proc_interface.unplot_objects(self.nx * self.ny * (self.hm_mirror_y_offset[0] - 1),
                                               self.nx * self.ny * self.hm_mirror_y_offset[0])
        if self.with_additional_plot:
            self.proc_interface.unplot_objects(self.nx * self.ny * (self.hm_additional_offset[0] - 1),
                                               self.nx * self.ny * self.hm_additional_offset)

    def post_plot(self, f_name, command):
        self.last_command = command
        self.file_names.append(f_name)
        self.first_time = False
        self.proc_interface.flush()

    def plot_mesh(self, f_name=""):
        t = time.time()
        self.pre_plot(f_name)

        # pre process phase
        self.file_mesh_name = fh.make_mesh_file(self.file_name, self.override)
        if self.last_command == "":
            self.proc_interface.set_x_limit(self.default_x_min, self.default_x_max)
            self.proc_interface.set_y_limit(self.default_y_min, self.default_y_max)

        if self.first_time:
            self.proc_interface.plot_mesh_2d(self.file_mesh_name)

        self.proc_interface.plot_mesh_2d(self.file_mesh_name)

        if self.with_mirror_x:
            self.proc_interface.seperate()
            self.proc_interface.plot_mesh_mirror_x(self.file_mesh_name)

        if self.with_mirror_y:
            self.proc_interface.seperate()
            self.proc_interface.plot_mesh_mirror_y(self.file_mesh_name)

        if self.with_mirror_x and self.with_mirror_y:
            self.proc_interface.seperate()
            self.proc_interface.plot_mesh_mirror_xy(self.file_mesh_name)

        if self.with_additional_plot:
            self.proc_interface.seperate()
            file_mesh_name2 = fh.make_mesh_file(self.additional_file_name, self.override)
            self.file_names.append(file_mesh_name2)
            self.proc_interface.plot_mesh_mirror_x(file_mesh_name2)
            self.proc_interface.flush()

        self.post_plot(self.file_mesh_name, "mesh")

    def plot_contour(self, cntr_type, cntr_num, c_min=0, c_max=0, f_name="", logscale=False):
        #for when we go to the next plot
        d_cmin, d_cmax = self.get_contour_limits(cntr_type)
        #if not self.plot_names.__contains__(f_name):
        self.pre_plot(f_name)
        self.file_mesh_name = fh.make_mesh_file(self.file_name, self.override)
        if c_min == d_cmin and d_cmax == c_max:
            c_min, c_max = self.contours.get_contour_limits(cntr_type)
        # if we get a command for contour or heatmap without dealing with the mesh first...
        # process file, just incase we haven't already.

        self.file_contour_name, contour_edge = fh.make_contour_file(self.file_name, self.override)

        #if no user input or bad one of contour min, max we take the ones from the file parsing phase.
        f = fh.contour_cython_file(self.x_coord, self.y_coord, self.contours.get_contour_data(cntr_type),
                                   str(f_name), str(cntr_type), int(cntr_num), c_min, c_max)

        self.proc_interface.set_cbrange(c_min, c_max, type_c=logscale, tics=10)
        self.proc_interface.plot_contour(self.file_mesh_name, f)
        if self.first_time:
            self.proc_interface.plot_contour(self.file_mesh_name, f)
            self.first_time = False
        self.post_plot(self.file_contour_name, "contour")
        self.post_plot(f, "contour")

    def plot_heatmap(self, cntr_type, c_min=0, c_max=0, f_name="", logscale=False):
        d_cmin, d_cmax = self.contours.get_contour_limits(cntr_type)
        self.pre_plot(f_name)
        if c_min == d_cmin and d_cmax == c_max:
            c_min, c_max = self.contours.get_contour_limits(cntr_type)
        self.file_contour_name, contour_edge = fh.make_contour_file(self.file_name, self.override)

        if self.with_mirror_x:
            f = fh.heatmap_cython_file(-1 * self.x_coord, self.y_coord, self.contours.get_contour_data(cntr_type=cntr_type),
                                       str(f_name), cntr_type, c_min, c_max, addition_name="x_", offset=self.hm_mirror_x_offset[0])
            # self.post_plot(f, "heatmap")
            self.proc_interface.plot_heatmap(f)
            self.file_names.append(f)

        if self.with_mirror_y:
            f = fh.heatmap_cython_file(self.x_coord, self.y_coord * - 1,
                                       self.contours.get_contour_data(cntr_type=cntr_type),
                                       str(f_name), cntr_type, c_min, c_max, addition_name="y_", offset=self.hm_mirror_y_offset[0])
            self.proc_interface.plot_heatmap(f)
            self.file_names.append(f)

        if self.with_mirror_x and self.with_mirror_y:
            f = fh.heatmap_cython_file(-1 * self.x_coord, self.y_coord * - 1,
                                       self.contours.get_contour_data(cntr_type=cntr_type),
                                       str(f_name), cntr_type, c_min, c_max, addition_name="xy_", offset=self.hm_mirror_xy_offset[0])
            self.proc_interface.plot_heatmap(f)
            self.file_names.append(f)

        f = fh.heatmap_cython_file(self.x_coord, self.y_coord, self.contours.get_contour_data(cntr_type=cntr_type)
                                   , str(f_name), cntr_type, c_min, c_max, offset=self.hm_offset[0])
        self.proc_interface.set_cbrange(c_min, c_max, type_c=logscale)
        self.proc_interface.plot_heatmap(f)
        if self.with_additional_plot:
            file_contour_name, contour_edge = fh.make_contour_file(f_name, self.override)
            cnt_data = fh.get_specific_contour_data(f_name, cntr_type)
            x_coord, y_coord = fh.get_x_y_coordinates(f_name)
            f = fh.heatmap_cython_file(-1 * x_coord, y_coord, cnt_data
                                       , str(f_name), cntr_type, c_min, c_max, offset=self.hm_additional_offset[0])
            self.proc_interface.plot_heatmap(f)
            self.file_names.append(f)
            self.file_names.append(file_contour_name)

        self.post_plot(self.file_contour_name, "heatmap")
        self.post_plot(f, "heatmap")


    def plot_additional_heatmap(self, cntr_type, c_min=0, c_max=0, f_name="", logscale=False, additional_plot=False):
        d_cmin, d_cmax = self.contours.get_contour_limits(cntr_type)
        if c_min == d_cmin and d_cmax == c_max:
            c_min, c_max = self.contours.get_contour_limits(cntr_type)
        file_contour_name, contour_edge = fh.make_contour_file(f_name, self.override)
        cnt_data = fh.get_specific_contour_data(f_name, cntr_type)
        x_coord, y_coord = fh.get_x_y_coordinates(f_name)
        f = fh.heatmap_cython_file(-1 * x_coord, y_coord, cnt_data
                                   , str(f_name), cntr_type, c_min, c_max, offset=self.hm_additional_offset[0])
        self.proc_interface.plot_heatmap(f)
        self.file_names.append(f)
        self.file_names.append(file_contour_name)
        self.proc_interface.flush()
        self.plot_mirror_vof(f_name)

    def plot_vof(self, vof=False, f_name=""):
        if vof:
            self.with_vof = True
        if f_name == "":
            f_name = self.file_name

        if self.with_vof or self.first_time:
            self.file_vof_name, self.vof_offset[1] = fh.make_vof_file(f_name, 1, 1, offset=self.vof_offset[0])
            self.proc_interface.plot_vof(self.file_vof_name)
            self.file_names.append(self.file_vof_name)

            if self.with_mirror_x:
                self.file_vof_x_name, self.vof_mirror_x_offset[1] = fh.make_vof_file(f_name, -1, 1, addition_name="mirror_x",
                                                                                   offset=self.vof_mirror_x_offset[0])
                self.file_names.append(self.file_vof_x_name)
                self.proc_interface.plot_vof(self.file_vof_x_name)
            else:
                self.proc_interface.unplot_objects(self.nx * self.ny * self.vof_mirror_x_offset[0] - self.vof_mirror_x_offset[1]
                                                   , self.nx * self.ny * self.vof_mirror_x_offset[0])
            if self.with_mirror_y:
                self.file_vof_y_name, self.vof_mirror_y_offset[1] = fh.make_vof_file(f_name, 1, -1, addition_name="mirror_y", offset=self.vof_mirror_y_offset[0])
                self.file_names.append(self.file_vof_y_name)
                self.proc_interface.plot_vof(self.file_vof_y_name)
            else:
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_mirror_y_offset[0] - self.vof_mirror_y_offset[1]
                    , self.nx * self.ny * self.vof_mirror_y_offset[0])
            if self.with_mirror_y and self.with_mirror_x:
                self.file_vof_xy_name, self.vof_mirror_xy_offset[1] = fh.make_vof_file(f_name, -1, -1,
                                                                                   addition_name="mirror_xy",
                                                                                   offset=self.vof_mirror_xy_offset[0])
                self.file_names.append(self.file_vof_xy_name)
                self.proc_interface.plot_vof(self.file_vof_xy_name)
            if self.with_additional_plot:
                print self.additional_file_name
                self.file_vof_additional_name, self.vof_additional_plot[1] = fh.make_vof_file(self.additional_file_name, -1, 1,
                                                                                       addition_name="additional_plot",
                                                                                       offset=self.vof_additional_plot[
                                                                                           0])
                self.file_names.append(self.file_vof_additional_name)
                self.proc_interface.plot_vof(self.file_vof_additional_name)
            else:
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_additional_plot[0] - self.vof_additional_plot[1]
                    , self.nx * self.ny * self.vof_additional_plot[0])

        self.proc_interface.flush()

    def unplot_vof(self, vof=True, force=False):
        if not vof:
            self.with_vof = vof

        if not self.with_vof or force and not self.first_time:
            _, self.vof_offset[1] = fh.get_limits_file(self.file_vof_name)
            self.proc_interface.unplot_objects(self.nx * self.ny * self.vof_offset[0] - self.vof_offset[1],
                                               self.nx * self.ny * self.vof_offset[0])
            if self.with_mirror_x:
                _, self.vof_mirror_x_offset[1] = fh.get_limits_file(self.file_vof_x_name)
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_mirror_x_offset[0] - self.vof_mirror_x_offset[1]
                    , self.nx * self.ny * self.vof_mirror_x_offset[0])
            if self.with_mirror_y:
                _, self.vof_mirror_y_offset[1] = fh.get_limits_file(self.file_vof_y_name)
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_mirror_y_offset[0] - self.vof_mirror_y_offset[1]
                    , self.nx * self.ny * self.vof_mirror_y_offset[0])
            if self.with_mirror_y and self.with_mirror_x:
                _, self.vof_mirror_xy_offset[1] = fh.get_limits_file(self.file_vof_xy_name)
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_mirror_xy_offset[0] - self.vof_mirror_xy_offset[1]
                    , self.nx * self.ny * self.vof_mirror_xy_offset[0])
            if self.with_additional_plot:
                _, self.vof_additional_plot[1] = fh.get_limits_file(self.file_vof_additional_name)
                self.proc_interface.unplot_objects(
                    self.nx * self.ny * self.vof_additional_plot[0] - self.vof_additional_plot[1]
                    , self.nx * self.ny * self.vof_additional_plot[0])

    def plot_mirror_vof(self, f_name):
        self.file_vof_x_name, self.vof_mirror_x_offset[1] = fh.make_vof_file(f_name, -1, 1, addition_name="mirror_x",
                                                                             offset=self.vof_mirror_x_offset[0])
        self.file_names.append(self.file_vof_x_name)
        self.proc_interface.plot_vof(self.file_vof_x_name)

    def get_min_max_contour(self, cntr_type, cntr_min, cntr_max):
        def_cntr_min, def_cntr_max = self.contours.get_contour_limits(cntr_type)
        if def_cntr_min > cntr_min:
            cntr_min = def_cntr_min
        if def_cntr_max < cntr_max:
            cntr_max = def_cntr_max
        return cntr_min, cntr_max

    def set_terminal(self, term="x11"):
        self.proc_interface.set_terminal(term)

    def get_contour_limits(self, cont_name):
        return self.contours.get_contour_limits(cont_name)

    def clear_plot(self):
        self.first_time = True
        self.proc_interface.clear()

    def override_file(self, value):
        self.override = value

    def start_click_gnuplot(self, port):
        self.proc_interface.mouse_click(port)
        # algorithm to search for the cell data.. we need x1,x2,x3,x4,y1,y2,y3,y4.. u..v.. and pressure etc..

    def extract_data(self, new_file):
        self.nx, self.ny, self.x_coord, self.y_coord, self.u_vel, self.v_vel, contour, contour_limit =\
               fh.get_data_table(self.file_name)
        self.contours.update_data(contour, contour_limit)
        self.default_x_min, self.default_x_max, self.default_y_min, self.default_y_max \
           = fh.get_xy_max_min(self.file_name)
        self.plot_time = fh.get_time(self.file_name)

    def get_mouse_click_parameters(self, x, y):
        k = ut.position_to_cell(x, y, self.x_coord, self.y_coord, self.nx, self.ny)
        k = int(k)
        i, j = ut.convert_1d_to_2d_i(k, self.nx)
        i = i + 1
        j = j + 1
        table_param = {}
        table_param["i_j"] = {}
        table_param["i1_j"] = {}
        table_param["i_j1"] = {}
        table_param["i1_j1"] = {}
        cell_param = {}

        for st in self.contours.get_contour_names():
            cell_param[st] = {}
            cell_param[st]["value"] = self.contours.get_contour_value(st, k)

        table_param["i_j"]["i"] = i
        table_param["i_j"]["j"] = j
        table_param["i_j"]["x"] = self.x_coord[k]
        table_param["i_j"]["y"] = self.y_coord[k]
        table_param["i_j"]["u"] = self.u_vel[k]
        table_param["i_j"]["v"] = self.v_vel[k]

        table_param["i1_j"]["x"] = self.x_coord[k + 1]
        table_param["i1_j"]["y"] = self.y_coord[k + 1]
        table_param["i1_j"]["u"] = self.u_vel[k + 1]
        table_param["i1_j"]["v"] = self.v_vel[k + 1]

        table_param["i_j1"]["x"] = self.x_coord[k + self.nx]
        table_param["i_j1"]["y"] = self.y_coord[k + self.nx]
        table_param["i_j1"]["u"] = self.u_vel[k + self.nx]
        table_param["i_j1"]["v"] = self.v_vel[k + self.nx]

        table_param["i1_j1"]["x"] = self.x_coord[k + self.nx + 1]
        table_param["i1_j1"]["y"] = self.y_coord[k + self.nx + 1]
        table_param["i1_j1"]["u"] = self.u_vel[k + self.nx + 1]
        table_param["i1_j1"]["v"] = self.v_vel[k + self.nx + 1]
        return table_param, cell_param, k

    def change_color(self, mat_id, clr):
        clr = str(clr)
        self.proc_interface.change_color(mat_id, ut.change_color_name(clr))

    def stop_mouse_loop(self):
        self.proc_interface.kill_mouse_click()

    def kill_process(self):
        self.proc_interface.kill_process()

    def change_background_color(self, clr):
        self.proc_interface.set_bg_color(clr)

    def unload_heatmap(self):
        self.proc_interface.unplot_objects()
        if self.with_mirror_x:
            self.proc_interface.unplot_objects(self.nx * self.ny * 11, self.nx * self.ny * 12)

    def remove_files(self):
        ut.remove_files(self.file_names)

    def set_with_mesh(self, flag):
        self.proc_interface.set_with_mesh(flag)

    def mirror_plot(self, flag_x, flag_y):
        self.with_mirror_x = flag_x
        self.with_mirror_y = flag_y
        self.proc_interface.set_with_mirror_x(flag_x)
        self.proc_interface.set_with_mirror_y(flag_y)
        if flag_y:
            self.default_x_min = -self.default_x_max
        if flag_x: # we plot with mirror
            # self.proc_interface.plot_mesh(self.file_mesh_name, flag)
            self.default_y_min = -self.default_y_max
        if not flag_x and not flag_y:
            self.default_x_min, self.default_x_max, self.default_y_min, self.default_y_max \
                = fh.get_xy_max_min(self.file_name)
        self.reset_limits()

    def get_time_of_plot(self):
        return self.plot_time

    def sum_cell_mass_in_polygon(self, list_vertices, mat_id):
        list_points = ut.find_points_in_polygon(list_vertices, self.x_coord, self.y_coord)
        print "Cell mass is: ", fh.read_mass_diag(self.nx, self.ny, mat_id, list_points, self.file_name)

    def resize(self, width, height):
        # self.proc_interface.set_terminal(w=width, h=height)

        # Reset the limits..
        # if width < self.width:
        #     #because they flip their axes..
        #     self.default_x_min, self.default_x_max = self.y_coord[0], self.y_coord[len(self.x_coord) - 1]
        #     self.default_y_min, self.default_y_max = self.x_coord[0], self.x_coord[len(self.y_coord) - 1]
        #     self.width = width
        #     self.height = height
        # else:
        #     self.width = width
        #     self.height = height
        self.reset_limits(False)

    def operator_contour(self, operator, cntr_name):
        self.contours.operator_data(operator, cntr_name)

    def get_contour_names(self):
        return self.contours.get_contour_names()

    def plot_line(self, px1, py1, px2, py2):
        id = self.nx * self.ny * 20 + len(self.lines_id)
        self.lines_id.append(id)
        self.proc_interface.draw_line(px1, py1, px2, py2, id)

    def clear_lines(self):
        if len(self.lines_id) > 2:
            self.proc_interface.unplot_objects(self.lines_id[0], self.lines_id[len(self.lines_id) - 1])
            self.lines_id = []

    def set_with_mirror_x(self, flag):
        self.with_mirror_x = flag
        self.proc_interface.set_with_mirror_x(flag)

    def set_with_mirror_y(self, flag):
        self.with_mirror_y = flag
        self.proc_interface.set_with_mirror_y(flag)

    def set_additional_plot(self, flag, f_name=""):
        self.with_additional_plot = flag
        self.additional_file_name = f_name
