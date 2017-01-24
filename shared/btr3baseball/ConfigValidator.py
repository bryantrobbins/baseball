from __future__ import print_function
from ExpressionValidator import ExpressionValidator
from DatasetRepository import DatasetRepository

class ConfigValidator:

    def __init__(self, config = {}):
        self.config = config
        self.dataRepo = DatasetRepository()
        self.funcs = []
        self.cols = []

    def validateConfig(self):
        self.loadDataset()
#        for t in config.transforms:
#            self.validateTransform(t)

    def validateTransform(self, trans):
        if trans.type == 'selectCols':
            self.selectCols(trans)
        if trans.type == 'selectRows':
            self.selectRows(trans)
        if trans.type == 'groupCols':
            self.groupCols(trans)
        if trans.type == 'defineCol':
            self.defineCol(trans)

    def loadDataset(self):
        if('dataset' not in self.config):
            raise MissingConfigItemException('dataset')
        ds = self.config['dataset']
        print('Loading dataset with name {}'.format(ds))
        if(ds not in self.dataRepo.listDatasets()):
            raise UnknownDatasetException(ds)
        self.cols = self.dataRepo.getDataset(ds)

    def selectRows(self, trans):
        print('Performing selectRow transform')
        if('column' not in trans):
            raise MissingTransformConfigItemException('selectRows', 'column')
        if(trans.column not in colnames()):
            raise UnknownColumnException(trans.column)
        
        col = getColumn(trans.column)
        
        if('operator' not in trans):
            raise MissingTransformConfigItemException('selectRows', 'column')
        if(trans.operator not in self.selectRowOps):
            raise UnknownSelectRowsOperator(trans.operator)
        
        if(criteria not in trans):
            raise MissingTransformConfigItemException('selectRows', 'criteria')
        
        utype = criType(trans.criteria)
        if(utype != col.type):
            raise SelectRowsCriteriaTypeException (col.name, col.type, utype)

    def selectCols(self, trans):
        print('Performing selectCol transform')
    
    def groupCols(self, trans):
        print('Performing groupCols transform')

    def defineCol(self, trans):
        print('Performing defineCol transform')

