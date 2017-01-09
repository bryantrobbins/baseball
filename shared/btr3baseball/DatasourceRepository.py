import pkg_resources
import json

resource_package = __name__
resource_path_format = 'datasource/{}.json'

class DatasourceRepository:
    def __init__(self):
        self.availableSources = json.loads(pkg_resources.resource_string(resource_package, resource_path_format.format('all')))['available']
        self.data = {}
        for source in availableSources:
            self.data[source] = json.loads(pkg_resources.resource_string(resource_package, resource_path_format.format(source)))
    
    def listDatasources(self):
        return self.availableSources

    def getDatasource(self, sourceId):
        if sourceId in self.data:
            return self.data[sourceId]
        else:
            return None
