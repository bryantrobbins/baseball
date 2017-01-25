from __future__ import print_function
from ExpressionValidator import ExpressionValidator
from DatasetRepository import DatasetRepository
import re

class ConfigValidator:

    selectRowOps = ['lt', 'gt', 'le', 'ge', 'eq', 'neq']

    def __init__(self, config = {}):
        self.config = config
        self.dataRepo = DatasetRepository()
        self.funcs = []
        self.cols = []

    def validateConfig(self):
        self.loadDataset()
        for t in self.config['transformations']:
            self.validateTransform(t)

    def validateTransform(self, trans):
        if trans['type'] == 'columnSelect':
            self.columnSelect(trans)
        if trans['type'] == 'rowSelect':
            self.rowSelect(trans)
        if trans['type'] == 'rowSum':
            self.rowSum(trans)
        if trans['type'] == 'columnDefine':
            self.columnDefine(trans)

    def loadDataset(self):
        if('dataset' not in self.config):
            raise MissingGlobalConfigItemException('dataset')
        ds = self.config['dataset']
        print('Loading dataset with name {}'.format(ds))
        if(ds not in self.dataRepo.listDatasets()):
            raise UnknownDatasetException(ds)
        self.cols = self.dataRepo.getDataset(ds)['columns']

    def rowSelect(self, trans):
        print('Performing selectRow transform')
        if('column' not in trans):
            raise MissingTransformConfigItemException('selectRows', 'column')
        if(trans['column'] not in self.colnames()):
            raise UnknownColumnException(trans['column'])
        
        col = self.getColumn(trans['column'])
        
        if('operator' not in trans):
            raise MissingTransformConfigItemException('selectRows', 'column')
        if(trans['operator'] not in self.selectRowOps):
            raise UnknownSelectRowsOperator(trans['operator'])
        
        if('criteria' not in trans):
            raise MissingTransformConfigItemException('selectRows', 'criteria')
        
        utype = self.criType(trans['criteria'])
        if(utype != col['type']):
            raise SelectRowsCriteriaTypeException (col['name'], col['type'], utype)

    def columnSelect(self, trans):
        print('Performing columnSelect transform')
    
    def rowSum(self, trans):
        print('Performing rowSum transform')

    def columnDefine(self, trans):
        print('Performing columnDefine transform')

    def colnames(self):
        return [ c['name'] for c in self.cols ]
    
    def getColumn(self, colname):
        return next(filter(lambda c : c['name'] == colname, self.cols))
    
    def criType(self, criteria):
        matchResult = re.match(r'\d+\.?(\d+)?', criteria)
        if matchResult:
            return 'N'
        else:
            return 'S'

class MissingGlobalConfigItemException(Exception):
    def __init__(self, itemName):
        super(UnknownColumnException, self).__init__('Missing global config item {}'.format(itemName))

class MissingTransformConfigItemException(Exception):
    def __init__(self, typeName, itemName):
        super(UnknownColumnException, self).__init__('Missing transformation config item {} for type {}'.format(typeName, itemName))

class UnknownColumnException(Exception):
    def __init__(self, colName):
        super(UnknownColumnException, self).__init__('Unknown column name {}'.format(colName))

class UnknownDatasetException(Exception):
    def __init__(self, dsName):
        super(UnknownColumnException, self).__init__('Unknown dataset name {}'.format(dsName))
