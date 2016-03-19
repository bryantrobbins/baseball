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
        return this[HTTP].get('/api/getMetadata/'+table.id);
    }

    getExportData(){
        return this[HTTP].get('/api/getExportData');
    }

    submitQuery(bundle){
        console.info(JSON.stringify(bundle));
        return this[HTTP].post('/api/submitJob', bundle);
    }
}

BaseballDataService.$inject = ['$http'];

export default BaseballDataService;