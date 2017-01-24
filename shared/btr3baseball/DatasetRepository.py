import pkg_resources
import json

resource_package = __name__
resource_path_format = 'datasource/{}.json'

class DatasetRepository:
    def __init__(self):
        jstr = pkg_resources.resource_string(resource_package, resource_path_format.format('all')).decode("utf-8") 
        self.availableSources = json.loads(jstr)['available']
        self.data = {}
        for source in self.availableSources:
            self.data[source] = json.loads(pkg_resources.resource_string(resource_package, resource_path_format.format(source)).decode("utf-8"))
    
    def listDatasets(self):
        return self.availableSources

    def getDataset(self, sourceId):
        if sourceId in self.data:
            return self.data[sourceId]
        else:
            return None
