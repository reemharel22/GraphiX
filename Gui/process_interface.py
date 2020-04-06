import sys, math
import time
import subprocess
import os
import signal


class Gnuplot(object):

    def __init__(self, proc=False, winId=0, term=False):
        if proc:
            self.plot_proc = subprocess.Popen(['../gnuplot_exec/bin/gnuplot', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        self.write_mouse = "print MOUSE_X, MOUSE_Y\n"
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.height = 663
        self.width = 1250
        self.with_mirror_x = 0
        self.with_mirror_y = 0
        self.y_max = 0
        self.first_time = True
        # starting to set up the limits of the contours !
        self.should_plot = False
        self.with_mesh = True
        self.window_id = winId
        self.heatmap_name = ""
        self.set_terminal(term)
        self.set_bg_color("black")
        self.set_line_color()
        self.set_font_size()

    def set_x_limit(self, x_min, x_max, replot=False):
        self.x_min = x_min
        self.x_max = x_max
        self.plot_proc.stdin.write(b"\nset xrange[" + str(x_min) + ":" + str(x_max) + "]\n")
        if replot:
            self.plot_proc.stdin.write(b"replot\n")

    def set_y_limit(self, y_min, y_max, replot=False):
        self.y_min = y_min
        self.y_max = y_max
        self.plot_proc.stdin.write(b"\nset yrange[" + str(y_min) + ":" + str(y_max) + "]\n")
        if replot:
            self.plot_proc.stdin.write(b"replot\n")

    def get_current_limits(self):
        return self.x_min, self.x_max, self.y_min, self.y_max

    def set_bg_color(self, color, x_min=-1000, x_max=1000, y_min=-1000, y_max=1000):
        color = "\"" + color.lower() + "\""
        self.plot_proc.stdin.write(b"\nset object 1 rectangle from " + str(x_min) +
                                   "," + str(y_min) + " " +
                                   b"to " + str(x_max) + "," + str(y_max) +
                                   b" fillstyle solid fillcolor" + color + "\nreplot\n")
        self.plot_proc.stdin.flush()

    def set_line_color(self):
        self.plot_proc.stdin.write( b"\nset linetype 1 lc rgb \"blue\"\n"
                                    b"set linetype 2 lc rgb \"green\"\n"
                                    b"set linetype 3 lc rgb \"cyan\"\n"
                                    b"set linetype 4 lc rgb \"dark-magenta\"\n"
                                    b"set linetype 5 lc rgb \"dark-yellow\"\n"
                                    b"set linetype 6 lc rgb \"dark-red\"\n"
                                    b"set linetype 7 lc rgb \"mediumpurple3\"\n"
                                    b"set linetype 8 lc rgb \"red\"\n"
                                    b"set linetype 9 lc rgb \"gray\"\n"
                                    b"set linetype 10 lc rgb \"white\"\n"
                                    b"set linetype 11 lc rgb \"forest-green\"\n"
                                    b"set linetype 12 lc rgb \"gray\"\n"
                                    b"set linetype 13 lc rgb \"white\"\n"
                                    b"set linetype 14 lc rgb \"white\"\n"
                                    b"set linetype 15 lc rgb \"white\"\n"
                                    b"set linetype 16 lc rgb \"white\"\n"
                                    b"set linetype 17 lc rgb \"white\"\n"
                                    b"set linetype 18 lc rgb \"white\"\n"
                                    b"set linetype 19 lc rgb \"white\"\n"
                                    b"set linetype 25 lc rgb \"white\"\n\n\n")
        self.plot_proc.stdin.flush()
        # b"set linetype cycle 12\n")

    def clear_vof(self, replot=False):
        self.plot_proc.stdin.write(b"set lt 25 lc rgb \"black\"\n")

    def set_vof(self, replot=False):
        self.plot_proc.stdin.write(b"set lt 25 lc rgb \"white\"\n")

    def set_terminal(self, term=False, h=663, w=1250):
        self.height = h
        self.width = w
        if term:
            self.plot_proc.stdin.write(b"\nset terminal qt \n")
        else:
            self.plot_proc.stdin.write(b"\nset terminal x11 size {0},{1} window \"{2}\"\n".format(str(self.width),
                                                                                                      str(self.height), hex(self.window_id)))

    def plot_contour(self, f_name, cntr_name):
        # incase we haven't preprocessed the file already.
        # we ofc need the mesh to know the contours..

        f_name = self.correct_name(f_name)
        cntr_name = self.correct_name(cntr_name)
        self.set_palette_color()
        if self.with_mesh:
            if not self.with_mirror_x:
                self.plot_proc.stdin.write(b"set mouse;p" + f_name + " u 2:1:3 w l linecolor variable,"
                                       + cntr_name + "u 2:1:3 w l lw 1.5 palette z\n")
            else:
                self.plot_proc.stdin.write(b"\nplot" + f_name + " u 2:1:3 w l linecolor variable," + f_name + " u 2:($1 *-1):3 w l lc variable,"
                                           + cntr_name + "u 2:1:3 w l lw 1.5 palette z," + cntr_name + "u 2:($1*-1):3 w l lw 1.5 palette z \n")
        else:
            if not self.with_mirror_x and not self.with_mirror_y:
                self.plot_proc.stdin.write(b"p {0} u 2:1:3 w l lw 1.5 palette z\n".format(cntr_name))
            elif self.with_mirror_x and self.with_mirror_y:
                self.plot_proc.stdin.write(b"p {0} u 2:1:3 w l lw 1.5 palette z, {0} u 2:($1*-1):3 w l lw 1.5 palette z"
                                           b", {0} u ($2*-1):1:3 w l lw 1.5 palette z".format(cntr_name))
            elif self.with_mirror_x and not self.with_mirror_y:
                self.plot_proc.stdin.write(
                    b"p {0} u 2:1:3 w l lw 1.5 palette z, {0} u 2:($1*-1):3 w l lw 1.5 palette z".format(cntr_name))
            else:
                self.plot_proc.stdin.write(
                    b"p {0} u 2:1:3 w l lw 1.5 palette z, {0} u ($2*-2):1:3 w l lw 1.5 palette z".format(cntr_name))

        self.should_plot = True

    def plot_mesh(self, name):
        print("MESH")
        self.validate_connection()
        name = self.correct_name(name)
        if not self.with_mirror_x:
            self.plot_proc.stdin.write(b"\nplot " + name + " u 2:1:3 w l lc variable \n")
            if self.first_time:
                self.plot_proc.stdin.write(b"\nplot " + name + " u 2:1:3 w l lc variable \n")
                self.first_time = False
        else:
            if not self.with_mirror_x and not self.with_mirror_y:
                self.plot_proc.stdin.write(b"p {0} u 2:1:3 w l linecolor variable\n".format(cntr_name))
            elif self.with_mirror_x and self.with_mirror_y:
                self.plot_proc.stdin.write(b"p {0} u 2:1:3 w l linecolor variable, {0} u 2:($1*-1):3 w l linecolor variable"
                                           b", {0} u ($2*-1):1:3 w l linecolor variable".format(cntr_name))
            elif self.with_mirror_x and not self.with_mirror_y:
                self.plot_proc.stdin.write(
                    b"p {0} u 2:1:3 w l linecolor variable, {0} u 2:($1*-1):3 w l linecolor variable".format(cntr_name))
            else:
                self.plot_proc.stdin.write(
                    b"p {0} u 2:1:3 w l linecolor variable, {0} u ($2*-2):1:3 w l linecolor variable".format(cntr_name))
            #self.plot_proc.stdin.write(
#                b"\nplot" + name + " u 2:1:3 w l linecolor variable," + name + " u (2):($1 *-1):3 w l lc variable \n")
                    #b"\nplot" + name + " u 2:1:3 w l linecolor variable," + name + " u ($2 *-1):1:3 w l lc variable \n")
        self.plot_proc.stdin.write(b"\nplot " + name + " u 2:1:3 w l lc variable \n")

    def plot_mesh_2d(self, name):
        self.validate_connection()
        name = self.correct_name(name)
        self.plot_proc.stdin.write("p {0} u 2:1:3 w l linecolor variable\n;".format(name))
        self.plot_proc.stdin.write("p {0} u 2:1:3 w l linecolor variable\n;".format(name))

    def plot_mesh_mirror_x(self, name):
        name = self.correct_name(name)
        self.plot_proc.stdin.write("{0} u 2:($1*-1):3 w l linecolor variable".format(name))

    def plot_mesh_mirror_y(self, name):
        name = self.correct_name(name)
        self.plot_proc.stdin.write(b"{0} u ($2*-1):1:3 w l linecolor variable".format(name))

    def plot_mesh_mirror_xy(self, name):
        name = self.correct_name(name)
        self.plot_proc.stdin.write(b"{0} u ($2*-1):($1*-1):3 w l linecolor variable".format(name))

    def plot_addition(self, name):
        name = self.correct_name(name)
        self.plot_proc.stdin.write(b"{0} u 2:1:3 w l linecolor variable".format(name))

    def plot_heatmap(self, name, num_proc=1):
        self.validate_connection()
        self.heatmap_name = self.correct_name(name)
        self.set_palette_color()
        if self.heatmap_name.__contains__("mirror"):
            self.plot_proc.stdin.write(b"load " + self.heatmap_name + "\n")
        else:
            self.plot_proc.stdin.write(b"load " + self.heatmap_name + ";\np 10000 palette\n")
        self.should_plot = True

    def plot_vof(self, name):
        name = self.correct_name(name)
        self.plot_proc.stdin.write(b"load {0}\n".format(name))

    def unplot_objects(self, low=0, high=0, replot=False):
        self.plot_proc.stdin.write(b"unset for[i={0}:{1}] object i\n".format(low, high))

    def plot_velocities(self, scale=1):
        self.plot_proc.stdin.write(b"\n replot " + self.f_name + "i 1 u 2:1:4:3 w vectors filled heads")

    def correct_name(self, f):
        return "\"" + f + "\""

    def set_window_ID(self, id):
        self.window_id = id

    def clear(self):
        self.first_time = True
        self.plot_proc.stdin.write(b"clear\n")

    def set_font_size(self, size=22):
        self.plot_proc.stdin.write(b"set xtics font \'Times New Roman," + str(size) + "\' \n")
        self.plot_proc.stdin.write(b"set ytics font \'Times New Roman," + str(size) + "\' \n")
        self.plot_proc.stdin.write(b"set ytics format \'%g\'  \n")
        self.plot_proc.stdin.write(b"set xtics format \'%g\'  \n")

    def set_cbrange(self, c_min, c_max, type_c=False, tics=10):
        stride = (float(c_max) - float(c_min)) / tics

        if type_c:
            self.plot_proc.stdin.write(b"set logscale cb\n")
            self.plot_proc.stdin.write(b"set cbtics {0}, {1}, {2}\nshow cbtics\n".format(str(c_min), str(math.log(float(c_max))), str(c_max)))
        self.plot_proc.stdin.write(b"set cbtics font \'Times New Roman,22\' format \'%3.1e\'\n")
        self.plot_proc.stdin.write(b"set cbrange[{0}:{1}]\n".format(c_min, c_max))

        if not type_c:
            self.plot_proc.stdin.write(b"unset logscale cb\n")
            self.plot_proc.stdin.write(b"set cbtics {0}, {1}, {2}\nshow cbtics\n".format(str(c_min), str(stride), str(c_max)))

    def mouse_click(self, port):
        self.plot_proc.stdin.write(b"while(1) { \n"
                                   b"pause mouse button1\n"
                                   b"if(MOUSE_KEY == 1) {\n"
                                   b"system sprintf(\"echo \'%f,%f\' | nc --send-only localhost " + str(port) + "\", "
                                                                    "MOUSE_Y, MOUSE_X)\n} }\n")

    def change_color(self, mat_id, color):
        color = self.correct_name(color)
        self.plot_proc.stdin.write(b"\nset linetype {0} lc rgb {1}\nreplot\n".format(mat_id, color))

    def kill_mouse_click(self):
        self.plot_proc.send_signal(signal.SIGINT)
        self.plot_proc.stdin.write("\n")

    def kill_process(self):
        self.plot_proc.terminate()

    def set_palette_color(self):
        self.plot_proc.stdin.write(b"set palette defined (0 0 0 0.5, 1 0 0 1, 2 0 0.5 1, 3 0 1 1, 4 0.5 1 0.5, 5 1 1 0, "
                                   b"6 1 0.5 0, 7 1 0 0, 8 0.5 0 0)\n")

    def draw_line(self, x1, y1, x2, y2, id):
        self.plot_proc.stdin.write(b"set object {0} polygon front from {2},{1} to {4},{3} to {2},{1} fs solid border lc" \
                         " \"{5}\" lw 1.8\nreplot\n".format(id, x1, y1, x2, y2, "forest-green"))

    def flush(self):
        self.plot_proc.stdin.write(b";\n")

    def seperate(self):
        self.plot_proc.stdin.write(b",")

    def set_with_mesh(self, flag):
        self.with_mesh = flag

    def set_with_mirror_x(self, flag):
        self.with_mirror_x = flag

    def set_with_mirror_y(self, flag):
        self.with_mirror_y = flag

    def validate_connection(self):
        try:
            self.plot_proc.stdin.write(b"\n")
        except Exception as exc:
            print "Gnuplot dead, reviving"
            self.plot_proc = subprocess.Popen(['gnuplot', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
            self.first_time = True
            # starting to set up the limits of the contours !
            self.should_plot = False
            self.with_mesh = True
            self.heatmap_name = ""
            # self.set_terminal("x11")
            self.set_bg_color("black")
            self.set_line_color()
            self.set_font_size()

    def replot(self):
        self.plot_proc.stdin.write(b"\nreplot\n")
