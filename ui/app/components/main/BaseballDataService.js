const HTTP = Symbol();

class BaseballDataService{
    constructor($http){
        this[HTTP] = $http;
    }

    getTables(){
        return this[HTTP].get('/getDataSetNames');
    }

    getTableMetadata(table){
        return this[HTTP].get('/getDataSetMetadata');
    }
}

export default BaseballDataService;