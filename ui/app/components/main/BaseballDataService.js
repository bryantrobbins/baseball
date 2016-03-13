import $q from 'q';
const HTTP = Symbol();

class BaseballDataService{
    constructor($http,$resource){
        this[HTTP] = $http;

		//Add back in when httpBackend is switched to Boot
		/**this.tables = $resource('http://localhost:8004/tables',{},{
			query: {method: 'get', isArray: true}
		});
		this.metadata = $resource('http://localhost:8004/metadata',{},{
			query: {method: 'get', isArray: false}
		});**/
    }

    getTables(){
	    return this[HTTP].get('/getDataSetNames');	
        //return this.tables.query();
    }

    getTableMetadata(table){

        return this[HTTP].get('/getDataSetMetadata');

		//return $q.resolve(this.metadata.query());

		
    }
}

export default BaseballDataService;