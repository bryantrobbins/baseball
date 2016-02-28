const HTTP = new WeakMap();

class BaseballDataService{
    constructor($http){
        HTTP.set(this, $http)
    }

    getTables(){
        return HTTP.get(this).get('/getDataSetNames');
    }

    getTableMetadata(){
        return HTTP.get(this).get('/getDataSetMetadata');
    }

    static BaseballDataFactory($http){
        return new BaseballDataService($http);
    }
}

BaseballDataService.$inject = ['$http'];

export default BaseballDataService;