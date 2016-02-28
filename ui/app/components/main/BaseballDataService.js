const HTTP = new WeakMap();

class BaseballDataService{
    /*@ngInject*/
    constructor($http){
        HTTP.set(this, $http);
    }

    getTables(){
        return HTTP.get(this).get('/getDataSetNames');
    }

    getTableMetadata(table){
        return HTTP.get(this).get('/getDataSetMetadata');
    }
}

export default BaseballDataService;