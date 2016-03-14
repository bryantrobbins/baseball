const HTTP = Symbol();

/**
 * TODO the endpoints need to be updated
 */
class BaseballDataService{
    constructor($http){
		this[HTTP] = $http;
    }

    getTables(){
        return this[HTTP].get('http://localhost:8004/tables');
    }

    getTableMetadata(table){
        return this[HTTP].get('http://localhost:8004/metadata');
    }

    getExportData(){
        return this[HTTP].get('http://localhost:8004/getExportData');
    }
}

BaseballDataService.$inject = ['$http'];

export default BaseballDataService;