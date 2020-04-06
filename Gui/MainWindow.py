import future_builtins
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtSql import *
from PyQt4.QtNetwork import *
import socket
from asyncore import *
import re
import os
import multiprocessing as mulp
import platform
import ui_designergui
import controller as controller
import ErrorDialog
from socket import *
import threading
import signal
import fpformat
import utils as ut
import FileDialog
import ColorDialog
import MovieDialog
import OperatorDialog
import BackgroundDialog
import CountCellMassDialog

tablecell_offset = 6


class MainWindow(QMainWindow, ui_designergui.Ui_MainWindow):

    def __init__(self, f_name="", qt=False, port=12345, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.should_stop = False
        self.s = None
        self.contours_name = []
        self.pink = 0
        self.last_command = ""
        self.first_window = 0
        self.set_up_gui()
        self.change_contour_limits = False
        self.tableVertex.enabledChange(False)
        self.f_name = f_name
        #self.last_command = "mesh"
        self.plotTitle.setText("Mesh " + self.f_name)
        self.control = controller.Controller(self.f_name, self.graphicsView.winId(), qt)
        self.thread = threading.Thread(target=self.gnuplot_click)
        self.port = port
        self.f_dialog = FileDialog.FileDialog()
        self.operator = OperatorDialog.OperatorDialog()
        self.color_dialog = ColorDialog.ColorDialog()
        self.movie_dialog = MovieDialog.MovieDialog()
        self.bg_dialog = BackgroundDialog.BackgroundDialog()
        self.count_cell_mass_dialog = CountCellMassDialog.CountCellMassDialog()
        self.list_vertices = {}
        self.list_vertices["i"] = []
        self.list_vertices["j"] = []
        self.list_vertices["x"] = []
        self.list_vertices["y"] = []
        self.list_vertices_flag = False
        self.display_callback()

    def resizeEvent(self, QResizeEvent):
        if self.first_window > 1:
            self.kill_thread()
            self.graphicsView.resize(self.width() - 20, self.graphicsView.height())
            self.control.resize(self.width() - 20, self.graphicsView.height())
        self.first_window = self.first_window + 1

    def post_plot(self):
        self.update_celltable_header()
        self.start_and_kill_thread()

    ############ CALL BACKS FROM EXPLICIT CLICKING ON THINGS IN GUI
    def file_load_callback(self):
        ok = self.f_dialog.exec_()
        if ok and self.f_dialog.filePath.text() != "": #we need to change the file
            f_name = str(self.f_dialog.filePath.text())
            f_name = str(ut.get_real_path(f_name, self.f_name))
            self.control.set_additional_plot(self.f_dialog.applyChkBox.isChecked(), f_name)

    def change_background_color_callback(self):
        ok = self.bg_dialog.exec_()
        if ok:
            # mat_id = self.color_dialog.
            if self.color_dialog.mat_color_txt.text() != "":
                mat_clr = self.color_dialog.mat_color_txt.text()
                self.color_dialog.mat_color_txt.clear()
            else:
                mat_clr = self.color_dialog.mat_color.currentText()
            self.kill_thread()
            self.control.change_background_color(str(self.bg_dialog.mat_color.currentText()))
            self.start_thread()


    #REGULAR DISPLAY, NO CONTOURS
    #we first set the limit text, update plot title, last command
    #then plot mesh and start the thread with start & kill
    def display_callback(self):
        if not self.last_command.__eq__(""):
            cntr_t = self.contour_type.currentText()
            dcmin, dcmax = self.control.get_contour_limits(cntr_t)
            c_min = self.cMin.text()
            c_max = self.cMax.text()
        self.control.plot_mesh(self.f_name)
        self.set_title_name("Mesh ")
        if not self.last_command.__eq__("") and c_min == dcmin and c_max == dcmax:
            self.reset_contour_callback()
        if self.last_command == "":
            self.set_limit_text()
        self.last_command = "mesh"
        self.post_plot()

    def display_two_plots(self, f):
        # If somone gives us a ~/XXXX path we need to extract the full path
        f = ut.same_folder_different_file(self.f_name, f)
        f = ut.get_real_path(f)
        if not self.last_command.__eq__(""):
            cntr_t = self.contour_type.currentText()
            dcmin, dcmax = self.control.get_contour_limits(cntr_t)
            c_min = self.cMin.text()
            c_max = self.cMax.text()
        if self.last_command.__eq__("mesh"):
            self.control.plot_additional_mesh(f)
            self.set_title_name("Mesh ")
            self.last_command = "mesh"
            self.post_plot()
        elif self.last_command.__eq__("heatmap"):
            cntr_t = self.contour_type.currentText()
            dcmin, dcmax = self.control.get_contour_limits(str(cntr_t))
            c_min = self.cMin.text()
            c_max = self.cMax.text()
            if c_min == c_max or (self.contourLogScale.isChecked() and float(c_min) < 0):
                self.error_message("Error in contour limits.\n")
            else:
                self.control.plot_additional_heatmap(cntr_t, c_min, c_max, f, self.contourLogScale.isChecked())
                self.set_title_name("Color map ")
                self.last_command = "heatmap"
                if c_min == dcmin and c_max == dcmax:
                    self.reset_contour_callback()
                self.post_plot()

        if not self.last_command.__eq__("") and c_min == dcmin and c_max == dcmax:
            self.reset_contour_callback()
        if self.last_command == "":
            self.set_limit_text()


    #Swaps the terminal
    # def terminal_callback(self):
    #     if self.terminal_qt.isChecked():
    #         self.control.set_terminal("qt")
    #         # self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    #         # self.setFixedSize(1930, 1500)
    #         # self.setGeometry(0, 0, 0, 0)
    #
    #     elif self.terminal_x11.isChecked():
    #         self.control.set_terminal("x11")
    #         self.showNormal()
    #         self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

    # Heatmap Display.
    # We first get the type of the contour and extract the min and max contour
    # then set titlename and plot via plot_heatmap. update last command and start & kill thread
    def display_heatmap_callback(self):
        cntr_t = self.contour_type.currentText()
        dcmin, dcmax = self.control.get_contour_limits(str(cntr_t))
        c_min = self.cMin.text()
        c_max = self.cMax.text()
        if c_min == c_max or (self.contourLogScale.isChecked() and float(c_min) < 0):
            self.error_message("Error in contour limits.\n")
        else:
            self.control.plot_heatmap(cntr_t, c_min, c_max, self.f_name, self.contourLogScale.isChecked())
            self.set_title_name("Color map ")
            self.last_command = "heatmap"
            if c_min == dcmin and c_max == dcmax:
                self.reset_contour_callback()
            self.post_plot()

    # Contours Display.
    # We first get the type ornumber of the contour and extract the min and max contour
    # then set titlename and plot via plot_heatmap. update last command and start & kill thread
    def display_contour_callback(self):
        cntr_t = self.contour_type.currentText()
        dcmin, dcmax = self.control.get_contour_limits(cntr_t)
        cntr_num = self.contour_number.text()
        c_min = self.cMin.text()
        c_max = self.cMax.text()
        if c_min == c_max:
            self.error_message("Contour limits are the same.\n")
        else:
            self.control.plot_contour(cntr_t, cntr_num, c_min, c_max, self.f_name, self.contourLogScale.isChecked())
        self.last_command = "contour"
        self.set_title_name("Contour ")
        if c_min == dcmin and c_max == dcmax:
            self.reset_contour_callback()
        self.post_plot()

    def update_celltable_header(self):
        j = 0
        k = 0
        num_cntr = len(self.control.get_contour_names())
        if num_cntr < tablecell_offset + 1:
            self.tableCell.setColumnCount(num_cntr)
            self.tableCell_2.setHidden(True)
        else:
            self.tableCell.setColumnCount(tablecell_offset)
            self.tableCell_2.setHidden(False)
            self.tableCell_2.setColumnCount(num_cntr - tablecell_offset)
        for i in self.control.get_contour_names():
            if j < tablecell_offset:
                self.tableCell.setHorizontalHeaderItem(j, QTableWidgetItem(i))
                k = j
            else:
                self.tableCell_2.setHorizontalHeaderItem(j - tablecell_offset, QTableWidgetItem(i))
            j = j + 1
        self.tableCell.setGeometry(590, 160, (k + 1) * 100 + 19, 60)
        self.tableCell_2.setGeometry(590, 230, (j - tablecell_offset) * 100 + 19, 60)
        self.set_contour_table()

    """
    Sets the contour options dynamically
    Called from update_celltable_header, because if we update the list we gotta update the contour options
    """
    def set_contour_table(self):
        j = 0
        cntr_names = self.control.get_contour_names()
        reset_list = False
        for i in cntr_names:
            seen = False
            for j in range(len(cntr_names)):
                if i == self.contour_type.itemText(j):
                    seen = True
            if not seen:
                reset_list = True
        if reset_list:
            self.contours_name = []
            for i in cntr_names:
                self.contour_type.removeItem(j)
                self.contour_type.addItem(i)
                self.contours_name.append(i)
                j = j + 1

    """
        Displays the plot.X+1 with the same option the users picked before
    """
    def next_plot_callback(self):
        tmp = []
        tmp = self.f_name.split('.')
        stride = self.skipPlot.text()
        tmp[len(tmp) - 1] = str(int(tmp[len(tmp) - 1]) + int(stride))
        tmp = ".".join(tmp)
        if not ut.file_exists(tmp):
            self.error_message("File {0} not found.".format(tmp))
            return

        self.f_name = tmp
        self.set_contour_limit_callback()
        self.display_by_last_command()

    """
        Displays the plot.X-1 with the same option the users picked before
    """
    def previous_plot_callback(self):
        x_min, x_max, y_min, y_max = self.control.get_limits()
        tmp = []
        tmp = self.f_name.split('.')
        stride = self.skipPlot.text()
        tmp[len(tmp) - 1] = str(int(tmp[len(tmp) - 1]) - int(stride))
        tmp = ".".join(tmp)

        if not ut.file_exists(tmp):
            self.error_message()
            return
        self.f_name = tmp
        self.display_by_last_command()
        #print x_min, x_max
        #self.control.set_limits(x_min, x_max, y_min, y_max)

    # In case the user wants us to override the file we act properly. ( we change the value at cojntroller)
    def override_callback(self):
        self.control.override_file(self.overrideChkBox.checkState())

    def vof_callback(self):
        self.control.with_vof = self.withVof.isChecked()

    def mesh_callback(self):
        if not self.withMesh.isChecked():
            self.control.set_with_mesh(False)
        else:
            self.control.set_with_mesh(True)

    def mirror_callback(self):
        self.control.mirror_plot(self.withMirror_x.isChecked(), self.withMirror_y.isChecked())

    # LIMIT PART:
    # Because we replot at the end we first kill the working thread.
    # we extract the limit typed by the user, set it via controller. and revive thread.
    def set_limits_callback(self):
        self.kill_thread()
        self.control.set_limits(float(self.xMin.text()), float(self.xMax.text()),
                                float(self.yMin.text()), float(self.yMax.text()))
        self.start_thread()

    # Same as above, we first kill thread, reset the limits to the default and revive thread.
    def reset_limits_callback(self):
        self.kill_thread()
        self.control.reset_limits()
        self.set_limit_text()
        self.start_thread()

    # END LIMIT
    # Reset the default values of the minimum and maximum value of the contours
    def reset_contour_callback(self):
        c_min, c_max = self.control.get_contour_limits(self.contour_type.currentText())
        self.cMin.setText(c_min)
        self.cMax.setText(c_max)

    # remove plot & notify controller to kill the loop & kill thread
    def clear_plot_callback(self):
        self.kill_thread()
        self.control.clear_plot()
        self.set_title_name("")

    def change_color_callback(self):
        ok = self.color_dialog.exec_()
        if ok:
            mat_id = self.color_dialog.mat_index.text()
            if self.color_dialog.mat_color_txt.text() != "":
                mat_clr = self.color_dialog.mat_color_txt.text()
                self.color_dialog.mat_color_txt.clear()
            else:
                mat_clr = self.color_dialog.mat_color.currentText()
            self.kill_thread()
            self.control.change_color(mat_id, mat_clr)
            self.start_thread()

    def movie_callback(self):
        end = str(int(ut.get_last_number_in_file(self.f_name)) - 1)
        self.movie_dialog.insert_defaults(self.contours_name, ut.get_numbers_in_file(self.f_name), end)
        ok = self.movie_dialog.exec_()
        plot_type = self.movie_dialog.plot_type.currentText()
        end = int(self.movie_dialog.endIndex.text())
        if ok:
            t_interval = float(self.movie_dialog.timeInterval.text())
            counter = int(self.movie_dialog.startIndex.text())
        if plot_type == "Color Map":
            self.display_heatmap_callback()
            counter = counter + 1
            title = "Color Map "
            self.set_title_name(title)
            time.sleep(t_interval)
            self.set_title_name(title)
        elif plot_type == "Contour":
            title = "Contour Map "
            self.display_contour_callback()
            counter = counter + 1
            self.set_title_name(title)
            time.sleep(t_interval)
            self.set_title_name(title)
        else:
            title = "Mesh "
            while counter != end:
                self.next_plot_callback()
                self.set_title_name(title)
                time.sleep(t_interval)
                counter = counter + 1

    def count_cell_mass_callback(self):
        self.kill_thread()
        ok = self.count_cell_mass_dialog.exec_()
        if ok:
            self.control.clear_lines()
            self.mat_id_for_mass = int(self.count_cell_mass_dialog.mat_index.value())
            self.list_vertices.clear()
            self.list_vertices["i"] = []
            self.list_vertices["j"] = []
            self.list_vertices["x"] = []
            self.list_vertices["y"] = []
            self.list_vertices_flag = True
        self.start_thread()

    """
    When we are done counting the cell mass we call the controller to calculate us what the result is
    """
    def stop_cell_mass_callback(self):
        self.kill_thread()
        self.list_vertices_flag = False
        leng = len(self.list_vertices["x"])
        self.control.plot_line(self.list_vertices["x"][0], self.list_vertices["y"][0], self.list_vertices["x"][leng - 1], self.list_vertices["y"][leng - 1])
        self.control.sum_cell_mass_in_polygon(self.list_vertices, int(self.count_cell_mass_dialog.mat_index.text()))
        self.start_thread()

    def operator_callback(self):
        self.operator.insert_contours(self.contours_name)
        ok = self.operator.exec_()
        if ok:
            cntr, o = self.operator.get_result()
            self.control.operator_contour(o, cntr)
            self.set_contour_limit_callback()

    """
        Picks what to display, either the heatmap or contour option
    """
    def display_contourheatmap_callback(self):
        if self.heatMap.checkState():
            self.display_heatmap_callback()
        else:
            self.display_contour_callback()

    """
    Sets the x,y limit text
    """
    def set_limit_text(self):
        xmin, xmax, ymin, ymax = self.control.get_limits()
        xmin = xmin
        xmax = xmax
        ymin = ymin
        ymax = ymax
        digit = '%1.2f'
        xmin = digit % xmin
        xmax = digit % xmax
        ymin = digit % ymin
        ymax = digit % ymax
        self.xMin.setText(str(xmin))
        self.xMax.setText(str(xmax))
        self.yMin.setText(str(ymin))
        self.yMax.setText(str(ymax))

    """
    Forcing the contour limit text with the default 
    """
    def set_contour_limit_callback(self):
        cmin, cmax = self.control.get_contour_limits(self.contour_type.currentText())
        self.cMin.setText(str(cmin))
        self.cMax.setText(str(cmax))

    """
        Sets the title of the plot
    """
    def set_title_name(self, type):
        self.plotTitle.setText("Time: " + self.control.get_time_of_plot() + "\n" + type + os.path.split(self.f_name)[1])

    """
        Displays the plot by the last pick of the user
    """
    def display_by_last_command(self):
        type_c = self.last_command
        if type_c.__eq__("mesh"):
            self.display_callback()
        elif type_c.__eq__("heatmap"):
            self.display_heatmap_callback()
        elif type_c.__eq__("contour"):
            self.display_contour_callback()

    """
        Abstract error message
    """
    def error_message(self, dialog=""):
        e = ErrorDialog.ErrorDialog(msg=dialog)
        e.exec_()

    """
        When GraphiX is initialized we create the menu bar, set the shortcut and connect actions to the commands
    """
    def set_up_gui(self):
        self.create_menubar()
        self.set_shortcuts()
        self.set_connections()

    """
        Top menu bar
    """
    def create_menubar(self):
        self.addPlot.setText("&Load File")
        self.addPlot.setToolTip("Load file from file browser.")
        self.colorOption.setText("Material &Color")
        self.background.setText("&Background Color")

    """
        Key shortcuts for actions in the gui
    """
    def set_shortcuts(self):
        self.addPlot.setShortcut(QKeySequence("L"))
        self.colorOption.setShortcut(QKeySequence("C"))
        self.nextPlot.setShortcut("Right")
        self.previousPlot.setShortcut("Left")
        self.reset_limit.setShortcut(QKeySequence("R"))
        self.heatMap.setShortcut(QKeySequence("E"))
        self.contourDisplay.setShortcut("Enter")
        self.background.setShortcut(QKeySequence("B"))
        self.heatMap.setShortcut(QKeySequence("H"))

    def keyPressEvent(self, event):
        if event.key() == QKeySequence("P"):
            self.p_count_callback()
        elif event.key() == QKeySequence("Q"):
            self.error_message("Hello there general Kenobi")
        elif event.key() == QKeySequence("F"):
            self.stop_cell_mass_callback()

    """
        Sets the connections to certain user actions.
        such as click on "mesh" we will run the function display_callback
    """
    def set_connections(self):
        self.connect(self.pushButton, SIGNAL("clicked()"), self.display_callback)
        self.connect(self.changeLimits, SIGNAL("clicked()"), self.set_limits_callback)
        self.connect(self.reset_limit, SIGNAL("clicked()"), self.reset_limits_callback)
        self.connect(self.contourDisplay, SIGNAL("clicked()"), self.display_contourheatmap_callback)
        self.connect(self.resetContour, SIGNAL("clicked()"), self.reset_contour_callback)
        self.connect(self.clearPlot, SIGNAL("clicked()"), self.clear_plot_callback)
        self.connect(self.nextPlot, SIGNAL("clicked()"), self.next_plot_callback)
        self.connect(self.previousPlot, SIGNAL("clicked()"), self.previous_plot_callback)
        #self.connect(self.overrideChkBox, SIGNAL("clicked()"), self.override_callback)
        self.connect(self.addPlot, SIGNAL("triggered()"), self.file_load_callback)
        self.connect(self.colorOption, SIGNAL("triggered()"), self.change_color_callback)
        self.connect(self.countCellMasses, SIGNAL("triggered()"), self.count_cell_mass_callback)
        self.connect(self.background, SIGNAL("triggered()"), self.change_background_color_callback)
        self.connect(self, SIGNAL("triggered()"), self.p_count_callback)
        # self.connect(self.terminal_qt, SIGNAL("clicked()"), self.terminal_callback)
        # self.connect(self.terminal_x11, SIGNAL("clicked()"), self.terminal_callback)
        self.connect(self.contour_type, SIGNAL("activated()"), self.set_contour_limit_callback)
        self.contour_type.currentIndexChanged[str].connect(self.set_contour_limit_callback)
        self.connect(self.withVof, SIGNAL("clicked()"), self.vof_callback)
        self.connect(self.withMesh, SIGNAL("clicked()"), self.mesh_callback)
        self.connect(self.movie, SIGNAL("triggered()"), self.movie_callback)
        self.connect(self.operator_2, SIGNAL("triggered()"), self.operator_callback)
        self.connect(self.withMirror_x, SIGNAL("clicked()"), self.mirror_callback)
        self.connect(self.withMirror_y, SIGNAL("clicked()"), self.mirror_callback)
        self.connect(self.cMax, SIGNAL("textChanged()"), self.cmin_callback)

    def cmin_callback(self, q):
        print "callback"

    def p_count_callback(self):
        if self.pink == 2:
            self.kill_thread()
            self.control.change_background_color("pink")
            self.start_thread()
            self.pink = 0
        else:
            self.pink = self.pink + 1

    """
        When the listening thread receives a message it sends the controller the position that was clicked
        The controller then sends back the vertex and cell parameters 
    """
    def click_on_plot_callback(self, q):
        st = q.split(",") # the message from gnuplot
        vertex_param, cell_param, k = self.control.get_mouse_click_parameters(st[0], st[1])
        if k != -1:
            self.update_table(vertex_param, cell_param)

    """
        Ease function, kills and starts the thread
    """
    def start_and_kill_thread(self):
        # we kill the thread just to be sure... and ofc close the socket just to be extra sure
        self.kill_thread()
        self.start_thread()

    """
        We start the listening thread, he gets the gnuplot_click as his operation
    """
    def start_thread(self):
        self.thread = threading.Thread(target=self.gnuplot_click)
        self.should_stop = False
        self.thread.start()

    """
        Main function of the listening thread.
        We start the connection to some port that the gnuplot interface is also connected to,
        and start the loop to see if he received a message from gnuplot.
    """
    def gnuplot_click(self):
        ac = ut.AsyncConn(port=self.port)
        self.control.start_click_gnuplot(ac.port)
        while not self.should_stop:
            if ac.msg != "":
                self.click_on_plot_callback(ac.msg)
                ac.msg = ""
            poll()
            time.sleep(0.01)
        ac.close()

    """
        Each time we want to update the viewer we have to kill the listening thread. 
    """
    def kill_thread(self):
        self.control.stop_mouse_loop()
        if self.thread.is_alive():
            self.should_stop = True
            time.sleep(0.1)

    """
        Updates the physical data table, called from the "listening" thread
        Receives a dictionary that has the vertex values and cell values.
        
        In the action of count cell mass, this function also adds to the list the coordinates of the clicked cells
    """
    def update_table(self, vertex_values, cell_values):
        digit = '%.3e'
        i = vertex_values["i_j"]["i"]
        j = vertex_values["i_j"]["j"]
        i1 = str(i + 1)
        j1 = str(j + 1)
        i = str(i)
        j = str(j)

        x = digit % vertex_values["i_j"]["x"]
        y = digit % vertex_values["i_j"]["y"]
        u = digit % vertex_values["i_j"]["v"]
        v = digit % vertex_values["i_j"]["u"]
        self.tableVertex.setItem(0, 0, QTableWidgetItem("({0}, {1})".format(i, j)))
        self.tableVertex.setItem(0, 1, QTableWidgetItem(str(x)))
        self.tableVertex.setItem(0, 2, QTableWidgetItem(str(y)))
        self.tableVertex.setItem(0, 3, QTableWidgetItem(str(u)))
        self.tableVertex.setItem(0, 4, QTableWidgetItem(str(v)))

        # FOR COUNT CELL MASSES IN A BOUNDING POLYGON
        if self.list_vertices_flag:
            self.list_vertices["i"].append(i)
            self.list_vertices["j"].append(j)
            self.list_vertices["x"].append(x)
            self.list_vertices["y"].append(y)
            leng = len(self.list_vertices["x"])
            if leng > 1:
                self.control.plot_line(x, y, self.list_vertices["x"][leng - 2], self.list_vertices["y"][leng - 2])

        # For the (i, j + 1) row:
        x = digit % vertex_values["i_j1"]["x"]
        y = digit % vertex_values["i_j1"]["y"]
        u = digit % vertex_values["i_j1"]["v"]
        v = digit % vertex_values["i_j1"]["u"]
        self.tableVertex.setItem(1, 0, QTableWidgetItem("({0}, {1})".format(i, j1)))
        self.tableVertex.setItem(1, 1, QTableWidgetItem(str(x)))
        self.tableVertex.setItem(1, 2, QTableWidgetItem(str(y)))
        self.tableVertex.setItem(1, 3, QTableWidgetItem(str(u)))
        self.tableVertex.setItem(1, 4, QTableWidgetItem(str(v)))

        # For the (i + 1, j) row:
        x = digit % vertex_values["i1_j"]["x"]
        y = digit % vertex_values["i1_j"]["y"]
        u = digit % vertex_values["i1_j"]["v"]
        v = digit % vertex_values["i1_j"]["u"]
        self.tableVertex.setItem(2, 0, QTableWidgetItem("({0}, {1})".format(i1, j)))
        self.tableVertex.setItem(2, 1, QTableWidgetItem(str(x)))
        self.tableVertex.setItem(2, 2, QTableWidgetItem(str(y)))
        self.tableVertex.setItem(2, 3, QTableWidgetItem(str(u)))
        self.tableVertex.setItem(2, 4, QTableWidgetItem(str(v)))

        # For the (i + 1, j + 1) row:
        x = digit % vertex_values["i1_j1"]["x"]
        y = digit % vertex_values["i1_j1"]["y"]
        u = digit % vertex_values["i1_j1"]["v"]
        v = digit % vertex_values["i1_j1"]["u"]
        self.tableVertex.setItem(3, 0, QTableWidgetItem("({0}, {1})".format(i1, j1)))
        self.tableVertex.setItem(3, 1, QTableWidgetItem(str(x)))
        self.tableVertex.setItem(3, 2, QTableWidgetItem(str(y)))
        self.tableVertex.setItem(3, 3, QTableWidgetItem(str(u)))
        self.tableVertex.setItem(3, 4, QTableWidgetItem(str(v)))

        j = 0
        cntr_names = self.control.get_contour_names()
        for i in cntr_names:
            if j < tablecell_offset:
                cntr_name = self.tableCell.horizontalHeaderItem(j).text()
                x = digit % cell_values[str(cntr_name)]["value"]
                self.tableCell.setItem(0, j, QTableWidgetItem(str(x)))
            else:
                cntr_name = self.tableCell_2.horizontalHeaderItem(j - tablecell_offset).text()
                x = digit % cell_values[str(cntr_name)]["value"]
                self.tableCell_2.setItem(0, j - tablecell_offset, QTableWidgetItem(str(x)))
            j = j + 1

    def end_program(self):
        self.kill_thread()
        self.control.kill_process()
        self.control.remove_files()

