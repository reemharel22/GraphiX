import pre_processing
import unittest

class KnownValues(unittest.TestCase):
    knownOperators = (1, "plot \"FOR_REEM_plot.gnu\" i 0 u 2:1:3 w l linecolor variable\n"),
    (2, "plot \"FOR_REEM_plot.gnu\" i 1 u 2:1:4:3 w vectors\n"),
    (3, "plot \"FOR_REEM_plot.gnu\" i 1 u 2:1:4:3 w vectors, \"FOR_REEM_plot.gnu\" i 0 u 2:1:3 w l linecolor variable\n")
