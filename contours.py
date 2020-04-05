import process_interface as p_interface
import file_handler as fh
import os
import sys, math
import numpy as np
from threading import Thread
import utils as ut
import time


class Contours(object):
    def __init__(self):
        self.data = 0

    def update_data(self, contour_data, contour_limit):
        self.contours = contour_data
        self.contour_limits = contour_limit

    def get_contour_limits(self, cntr_id=0):
        return self.get_contour_limits(self.get_contour_id(cntr_id))

    def get_contour_limits(self, cont_name=""):
        return self.contour_limits[str(cont_name).upper()]["min"], self.contour_limits[str(cont_name).upper()]["max"]

    def get_contour_id(self, cntr_name):
        return self.contour_limits[str(cntr_name).upper()]["id"]

    def operator_data(self, operator, cntr_name):
        operator = str(operator)
        cntr_id = self.get_contour_id(cntr_name)
        cntr = self.get_contour_data(cntr_type=cntr_name)
        for i in range(len(cntr)):
            cntr[i], b = ut.parse_execute_operator(operator, {"x": cntr[i]})
        self.contour_limits[cntr_name]["max"], b = ut.parse_execute_operator(
            operator, {"x": float(self.contour_limits[cntr_name]["max"])})
        self.contour_limits[cntr_name]["min"], b = ut.parse_execute_operator(
            operator, {"x": float(self.contour_limits[cntr_name]["min"])})
        self.contours[cntr_id] = cntr

    def get_contour_data(self, cntr_type):
        return self.contours[self.get_contour_id(cntr_type)]

    def get_contour_names(self):
        return self.contour_limits.keys()

    def get_contour_value(self, cntr_name, i):
        return self.contours[self.get_contour_id(cntr_name)][int(i)]

