from __future__ import print_function
from ExpressionValidator import *

class ConfigValidator:
    self.funcs = []
    self.cols = [] 

    def __init__(self, config):
        self.config = config

    def validateConfig(self):
        for t in config.transforms:
            validateTransform(t)

    def validateTransform(self, trans):
        if trans.type == 'load':
            loadDataset(trans)
        if trans.type == 'selectCols':
            selectCols(trans)
        if trans.type == 'selectRows':
            selectRows(trans)
        if trans.type == 'groupCols':
            groupCols(trans)
        if trans.type == 'defineCol':
            defineCol(trans)
