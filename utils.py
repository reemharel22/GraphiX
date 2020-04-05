import socket
from asyncore import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import math
import GraphiX



# For connections:
class Handler(dispatcher):
    def __init__(self, socket, asyncon):
        dispatcher.__init__(self, socket)
        self.asyncon = asyncon

    def handle_read(self):
        self.asyncon.msg = self.recv(4096)


class AsyncConn(dispatcher):
    def __init__(self, port=12346):
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        dispatcher.__init__(self)
        connected = False
        while not connected:
            try:
                self.set_socket(s)
                self.msg = ""
                self.accepted = False
                self.bind(('127.0.0.1', self.port))
                connected = True
            except socket.error, e:
                connected = False
                print "Connecting to port {0} failed. Trying port {1}".format(self.port, self.port - 1)
                self.port = self.port - 1
        self.listen(5)
        self.set_reuse_addr()

    def handle_read(self):
        print "reading"
        data = self.recv(1024)
        if data:
            print data

    def handle_write(self):
        pass

    def readable(self):
        return True

    def handle_accept(self):
        self.accepted = True
        socket, addr = self.accept()
        Handler(socket, self)

    def kys(self):
        self.close()


# Static functions:

def area_ptc(x1, y1, x2, y2, x3, y3):
    return (x2 - x1) * (y3 - y1) - (y2 - y1)*(x3 - x1)


def change_color_name(clr):
    return clr.lower()


def guiname_to_dataname(s_name):
    name = str(s_name.lower())
    if name.__eq__("pressure"):
        return name.upper()
    elif name.__eq__("artificial viscosity"):
        return "arti_vis".upper()
    elif name.__eq__("density"):
        return name.upper()
    elif name.__eq__("internal energy"):
        return "internal_e".upper()
    elif name.__eq__("temperature"):
        return name.upper()
    elif name.__eq__("t_radiation"):
        return name.upper()
    elif name.__eq__("kria"):
        return name.upper()
    elif name.__eq__("pixt"):
        return name.upper()
    elif name.__eq__("epsp"):
        return name.upper()




    elif name.__eq__("shet_ng"):
        return name.upper()
    elif name.__eq__("thermal"):
        return name.upper()
    elif name.__eq__("fusion_rate"):
        return name.upper()
    elif name.__eq__("ra_in"):
        return name.upper()
    elif name.__eq__("tshock"):
        return name.upper()
    elif name.__eq__("roshock"):
        return name.upper()
    elif name.__eq__("epspc"):
        return name.upper()
    elif name.__eq__("epspd"):
        return name.upper()
    elif name.__eq__("phase"):
        return name.upper()


def calculate_limits_aspect_ratio(x_min, x_max, y_min, y_max, h=650, w=1250):
    delta_x = abs(x_max - x_min)
    delta_y = abs(y_max - y_min)
    height = h
    width = w
    if delta_x > (w/h) * delta_y:
        y_max1 = height * delta_x / width + y_min
        if y_max1 > y_max:
            y_max = y_max1
    else:
        x_max1 = width * delta_y / height + x_min
        if x_max1 > x_max:
            x_max = x_max1
    return x_min, x_max, y_min, y_max


def get_numbers_in_file(f_name):
    tmp = f_name.split('.')
    return str(int(tmp[len(tmp) - 1]))


def get_last_number_in_file(f_name):
    tmp = f_name.split('.')
    while file_exists(f_name):
        tmp = f_name.split('.')
        num = str(int(tmp[len(tmp) - 1]) + 1)
        tmp[len(tmp) - 1] = num
        f_name = ".".join(tmp)
    return num


def file_exists(f_name):
    if not os.path.isfile(f_name):
        return False
    return True


def parse_operator(str, data, max, min):
    str = "a"
    str.lstrip(' ')
    # First we want the first argument before the operator itself, then we want the second argment after the operator
    # a OPERATOR b
    operator = find_operator(str)
    if not operator == "None":
        if str.count(operator) > 1:
            #we have the same operator twice
            a = operator.partition(operator)[0]
        else:
            a = str.split(operator)[0]

        b = str.split(operator)[1]

        if b == "None":
            #done parsing
            execute_operator(a, b, operator)


def find_operator(str):
    if str.__contains__("/"):
        opeartor = "/"
    elif str.__contains__("*"):
        operator = "*"
    elif str.__contains__("+"):
        operator = "+"
    elif str.__contains__("-"):
        operator = "-"
    elif str.__contains__("^"):
        operator = "^"
    else:
        operator = "None"
    return operator


def execute_operator(a, b, operator):
    if operator.__eq__("/"):
        return a / b
    elif operator.__eq__("*"):
        return a * b
    elif operator.__eq__("+"):
        return a + b
    elif operator.__eq__("-"):
        return a - b
    elif operator.__eq__("^"):
        return a ** b
    else:
        return a


def parse_execute_operator(char_arg, args_values=None):
    arg = None
    arg_type = None

    # print parse_fortran_type('1.72223046614d26')
    char_arg = str(char_arg)  # casting into char for all types

    if len(char_arg) > 0:

        if 'E' in char_arg and arg is None:

            try:

                a = float(char_arg[:char_arg.index('E')])
                b = float(char_arg[char_arg.index('E') + 1:])

                arg = a * pow(10, b)
                arg_type = "double"

            except ValueError:

                pass

        elif 'e' in char_arg and arg is None:

            try:

                a = float(char_arg[:char_arg.index('e')])
                b = float(char_arg[char_arg.index('e') + 1:])

                arg = a * pow(10, b)
                arg_type = "double"

            except ValueError:

                pass

        if 'D' in char_arg and arg is None:

            try:

                a = float(char_arg[:char_arg.index('D')])
                b = float(char_arg[char_arg.index('D') + 1:])

                arg = a * pow(10, b)
                arg_type = "double"

            except ValueError:

                pass

        elif 'd' in char_arg and arg is None:

            try:

                a = float(char_arg[:char_arg.index('d')])
                b = float(char_arg[char_arg.index('d') + 1:])

                arg = a * pow(10, b)
                arg_type = "double"

            except ValueError:

                pass

        if '.' in char_arg and arg is None:

            try:

                a = float(char_arg)

                arg = float(char_arg)
                arg_type = "double"

            except ValueError:

                pass

        calc = ['+', '-', '*', '/', '^', '(', ')']

        try:

            for c in calc:

                if c in char_arg:

                    try:

                        # nsp = NumericStringParser() # complex expressions
                        # arg = nsp.eval(char_arg)
                        try:

                            arg = eval(char_arg, args_values)
                            arg_type_by_python = type(arg)

                            if arg_type_by_python == int:
                                arg_type = "integer"

                            if arg_type_by_python == float:
                                arg_type = "double"

                        except NameError or ValueError or SyntaxError:

                            arg = char_arg
                            arg_type = "char"
                            return arg, arg_type

                    except SyntaxError:

                        pass

        except ValueError:

            pass

        if arg is None:

            breaks = False

            for c in char_arg:

                try:

                    int(c)

                except ValueError:

                    breaks = True

            if breaks is False:
                arg = int(char_arg)
                arg_type = "integer"

        if arg is None:  # meaning all of the aboves didnt match

            arg = char_arg
            arg_type = "char"

    return arg, arg_type


def remove_files(file_names):
    for f in file_names:
         if file_exists(f):
             os.remove(f)


def convert_1d_to_2d_i(k, nx):
    j = int(k / nx)
    i = int(k - j * nx)
    return int(i), int(j)


def position_to_cell(x, y, x_coord, y_coord, nx, ny):
    x = np.float64(x)
    y = np.float64(y)
    return GraphiX.position_to_cell(x, y, x_coord, y_coord, nx, ny)


def get_max_min_coordinates(list_vertices):
    xmax = -100000000.0
    xmin = 100000000.0
    ymax = -100000000.0
    ymin = 100000000.0
    for i in range(len(list_vertices["i"])):
        x = float(list_vertices["x"][i])
        y = float(list_vertices["y"][i])
        xmin = min(x, xmin)
        xmax = max(x, xmax)
        ymin = min(y, ymin)
        ymax = max(y, ymax)

    return float(xmin), float(xmax), float(ymin), float(ymax)


def find_points_in_polygon(list_vertices, x_coord, y_coord):
    xmin, xmax, ymin, ymax = get_max_min_coordinates(list_vertices)
    list_points = []
    e = (xmax - xmin) / 100
    for j in range(len(x_coord)):
        x = x_coord[j]
        y = y_coord[j]
        # print xmin, x, xmax, ymin, y, ymax
        if x < xmin or x > xmax or y < ymin or y > ymax:
            continue
        else:
            y2 = ymin - e
            x2 = x
            intersection = 0
            k = len(list_vertices["i"]) - 1
            for i in range(k):
                if is_intersect(list_vertices["x"][i], list_vertices["y"][i],
                                list_vertices["x"][i + 1], list_vertices["y"][i + 1], x, y, x2, y2):
                    intersection = intersection + 1

            if is_intersect(list_vertices["x"][0], list_vertices["y"][0],
                            list_vertices["x"][k], list_vertices["y"][k], x, y, x2, y2):
                intersection = intersection + 1
            if not intersection % 2 == 0:
                list_points.append(j)
    return list_points


def is_intersect(v1x1, v1y1, v1x2, v1y2, v2x1, v2y1, v2x2, v2y2):
    v1x1, v1y1, v1x2, v1y2, v2x1, v2y1, v2x2, v2y2 = float(v1x1), float(v1y1), float(v1x2), float(v1y2), float(v2x1)\
        , float(v2y1), float(v2x2), float(v2y2)
    # See: http: // en.wikipedia.org / wiki / Linear_equation
    a1 = v1y2 - v1y1
    b1 = v1x1 - v1x2
    c1 = (v1x2 * v1y1) - (v1x1 * v1y2)
    d1 = (a1 * v2x1) + (b1 * v2y1) + c1
    d2 = (a1 * v2x2) + (b1 * v2y2) + c1

    if d1 > 0 and d2 > 0:
        return False
    if d1 < 0 and d2 < 0:
        return False

    a2 = v2y2 - v2y1
    b2 = v2x1 - v2x2
    c2 = (v2x2 * v2y1) - (v2x1 * v2y2)

    # Calculate d1 and d2 again, this time using points  of vector 1.
    d1 = (a2 * v1x1) + (b2 * v1y1) + c2
    d2 = (a2 * v1x2) + (b2 * v1y2) + c2

    # Again,if both have the same sign ( and neither one is 0),
    # no intersection is possible.
    if d1 > 0 and d2 > 0:
        return False
    if d1 < 0 and d2 < 0:
        return False

    # If we get here, only two possibilities are left.Either the two vectors intersect in exactly
    # one point or they are collinear, which means they intersect in any number of points from zero to infintie
    if (a1 * b2) - (a2 * b1) == 0.0:
        return True
    return True


def get_real_path(f_name, f_name2):
    path = f_name
    if f_name.__contains__('~'):
        path = os.path.expanduser('~') + f_name.split('~')[1]
    elif f_name.__contains__('..'):
        path = path
    else:
        splt = f_name2.split('/')[len(f_name2.split('/')) - 2]
        path = os.path.abspath(os.path.join(f_name2 + "/../" + splt, f_name))
        print path
    return path


# def same_folder_different_file(f1, f2):
#     st = f2
#     if not f2.__contains__('~'):
#         st = os.path.join(f1.split('/')[0:len(f1) - 2], f2)
#     return st
