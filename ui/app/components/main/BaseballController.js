import _ from 'lodash';


const BASEBALL = new WeakMap();
const FILTER = new WeakMap();

class BaseballController {
    /*@ngInject*/
    constructor($filter, BaseballDataService){
        BASEBALL.set(this, BaseballDataService);
        FILTER.set(this, $filter);
        BaseballDataService.getTables().success((resp) => {
            this.dataSets = resp;
        });

        this.query = {
            order: 'column'
        };
    }


    static BaseballFilter($filter){
        return function(values, input){
            if(!input || input.trim() === ''){
                return values;
            }else{
                return $filter('filter')(values,input);
            }
        };
    }

    fetchMetadata(){
        if(this.dataSets && this.dataSets.indexOf(this.selectedDataSet) !== -1) {
            BASEBALL.get(this).getTableMetadata(this.selectedDataSet).success((resp) => {
                this.metadata = resp;
            });
        }
    }

    getCurrentSelectedDataSet(){
    	if (this.selectedDataSet === undefined)
    		return "Nothing is selected yet";
       	return this.selectedDataSet;
    }

    // Return the set of datasets 
    // Expecting a return of an array 
    // Empty array will indicate that nothing is found

    getFormula(){
        if(this.formula === undefined)
        {
           return "Please enter in a formula.";
        }
        else
        {
            return this.formula;
        }
    }

    sortData(){
        console.info("reorder was called");
        this.metadata.colMetaData = _.sortBy(this.metadata.colMetaData, (element)=>{
            return element.colName;
        });
    }
}

//This is such a hack.
BaseballController.BaseballFilter.$inject = ['$filter'];

export default BaseballController;