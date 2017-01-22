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
        if trans.type == 'selectCols':
            self.selectCols(trans)
        if trans.type == 'selectRows':
            self.selectRows(trans)
        if trans.type == 'groupCols':
            self.groupCols(trans)
        if trans.type == 'defineCol':
            self.defineCol(trans)

    def loadDataset(self, dsName):
        print('Loading dataset with name {}'.format(dsName))
    
    def selectCols(self, trans):
        print('Performing selectCol transform')
    
    def selectRows(self, trans):
        print('Performing selectRow transform')
    
    def groupCols(self, trans):
        print('Performing groupCols transform')

    def defineCol(self, trans):
        print('Performing defineCol transform')

