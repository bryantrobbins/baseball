from __future__ import print_function
from ExpressionValidator import ExpressionValidator
from DatasetRepository import DatasetRepository
import re
import json

class ConfigValidator:

    selectRowOps = ['lt', 'gt', 'le', 'ge', 'eq', 'neq']

    def __init__(self, configStr = "", configObj = None):
        if configObj != None:
            self.config = json.loads(configStr)
        elif configStr != "":
            self.config = json.loads(configStr)

        self.dataRepo = DatasetRepository()
        self.funcs = []
        self.cols = []
        self.keyCols = []

    def validateConfig(self):
        self.loadDataset()
        for t in self.config['transformations']:
            self.validateTransform(t)
        
        self.checkOutput()
        return True

    def validateTransform(self, trans):
        if trans['type'] == 'columnSelect':
            self.columnSelect(trans)
        elif trans['type'] == 'rowSelect':
            self.rowSelect(trans)
        elif trans['type'] == 'rowSum':
            self.rowSum(trans)
        elif trans['type'] == 'columnDefine':
            self.columnDefine(trans)
        else:
            raise UnknownTransformTypeException(trans['type'])

    def loadDataset(self):
        if('dataset' not in self.config):
            raise MissingGlobalConfigItemException('dataset')
        ds = self.config['dataset']
        if(ds not in self.dataRepo.listDatasets()):
            raise UnknownDatasetException(ds)
        self.cols = self.dataRepo.getDataset(ds)['columns']
        self.keyCols = self.dataRepo.getDataset(ds)['keyCols']

    def checkOutput(self):
        if('output' not in self.config):
            raise MissingGlobalConfigItemException('output')

        output = self.config['output']

        if output['type'] == 'leaderboard':
            self.checkLeaderboard(output)
        else:
            raise UnknownOutputTypeException(output['type'])

    def checkLeaderboard(self, output):
        directionValues = ['asc', 'desc']
        if('column' not in output):
            raise MissingOutputConfigItemException('column')
        
        if('direction' not in output):
            raise MissingOutputConfigItemException('direction')

        if(output['column'] not in self.colnames()):
            raise UnknownColumnException(output['column'])
        
        if(output['direction'] not in directionValues):
            raise UnknownLeaderboardDirectionException(output['direction'])
        
    def rowSelect(self, trans):
        col = self.getColumn(trans)
        
        if('operator' not in trans):
            raise MissingTransformConfigItemException('rowSelect', 'operator')
        if(trans['operator'] not in self.selectRowOps):
            raise UnknownSelectRowsOperatorException(trans['operator'])
        
        if('criteria' not in trans):
            raise MissingTransformConfigItemException('rowSelect', 'criteria')
        
        utype = self.criType(trans['criteria'])
        if(utype != col['type']):
            raise RowSelectCriteriaTypeException (col['name'], col['type'], utype)

    def columnSelect(self, trans):
        self.cols = self.getColumns(trans)

    def rowSum(self, trans):
        cols = self.getColumns(trans) + self.colFilterNumeric()
        self.cols = { v['name']:v for v in cols }.values()

    def columnDefine(self, trans):
        if('column' not in trans):
            raise MissingTransformConfigItemException('columnDefine', 'column')

        if('expression' not in trans):
            raise MissingTransformConfigItemException('columnDefine', 'expression')

        if not self.strCheck(trans['column']):
            raise BadColumnNameException(trans['column'])

        if trans['column'] in self.cols:
            raise BadColumnNameException(trans['column'])

        ev = ExpressionValidator({}, self.cols)
        result = ev.validateExpression(trans['expression'])
        node = result.ast.__getattribute__('value')
        colDef = {'name': trans['column'], 'type': 'N' }

        if node.__class__.__name__ == 'Str':
            colDef['type'] = 'S'

        self.cols.append(colDef)        

    def colnames(self):
        return [ c['name'] for c in self.cols ]

    def colFilter(self, colName):
        return next(iter(filter(lambda c : c['name'] == colName, self.cols)))

    def colFilterNumeric(self):
        return filter(lambda c : c['type'] == 'N', self.cols)
        
    def getColumn(self, trans):
        if('column' not in trans):
            raise MissingTransformConfigItemException(trans['type'], 'column')

        if(trans['column'] not in self.colnames()):
            raise UnknownColumnException(trans['column'])

        return self.colFilter(trans['column'])

    def getColumns(self, trans):
        if('columns' not in trans):
            raise MissingTransformConfigItemException(trans['type'], 'columns')
        
        cols = []
        for col in trans['columns']:
            if(col not in self.colnames()):
                raise UnknownColumnException(trans['column'])
            cols.append(self.colFilter(col))

        for col in self.keyCols:
            cols.append(self.colFilter(col))

        return cols

    def criType(self, criteria):
        matchResult = re.match(r'\d+\.?(\d+)?', criteria)
        if matchResult:
            return 'N'
        else:
            return 'S'

    def strCheck(self, colName):
        matchResult = re.match(r'[A-z0-9]+', colName)
        if matchResult:
            return True
        else:
            return False

class MissingGlobalConfigItemException(Exception):
    def __init__(self, itemName):
        super(MissingGlobalConfigItemException, self).__init__('Missing global config item {}'.format(itemName))

class MissingTransformConfigItemException(Exception):
    def __init__(self, typeName, itemName):
        super(MissingTransformConfigItemException, self).__init__('Missing transformation config item {} for type {}'.format(typeName, itemName))

class MissingOutputConfigItemException(Exception):
    def __init__(self, itemName):
        super(MissingOutputConfigItemException, self).__init__('Missing output config item {}'.format(itemName))

class UnknownColumnException(Exception):
    def __init__(self, colName):
        super(UnknownColumnException, self).__init__('Unknown column name {}'.format(colName))

class BadColumnNameException(Exception):
    def __init__(self, colName):
        super(BadColumnNameException, self).__init__('Invalid name {} for user-defined column'.format(colName))

class UnknownDatasetException(Exception):
    def __init__(self, dsName):
        super(UnknownDatasetException, self).__init__('Unknown dataset name {}'.format(dsName))

class UnknownSelectRowsOperatorException(Exception):
    def __init__(self, opName):
        super(UnknownSelectRowsOperatorException, self).__init__('Unknown operator name {}'.format(opName))

class UnknownTransformTypeException(Exception):
    def __init__(self, transName):
        super(UnknownTransformTypeException, self).__init__('Unknown transformation type {}'.format(transName))

class UnknownOutputTypeException(Exception):
    def __init__(self, outputName):
        super(UnknownOutputTypeException, self).__init__('Unknown output type {}'.format(outputName))

class UnknownLeaderboardDirectionException(Exception):
    def __init__(self, givenDir):
        super(UnknownOutputTypeException, self).__init__('Unknown value {} given for direction in leaderboard config'.format(givenDir))

