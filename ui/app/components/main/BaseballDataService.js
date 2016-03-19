const HTTP = Symbol();

/**
 * TODO the endpoints need to be updated
 */
class BaseballDataService{
    constructor($http){
		this[HTTP] = $http;
    }

    getTables(){
        return this[HTTP].get('/api/getTables');
    }

    getTableMetadata(table){
        return this[HTTP].get('/api/getMetadata/'+table);
    }

    getExportData(){
        return this[HTTP].get('/api/getExportData');
    }
}

BaseballDataService.$inject = ['$http'];

export default BaseballDataService;