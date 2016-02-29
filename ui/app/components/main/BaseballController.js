import _ from 'lodash';


const BASEBALL = new WeakMap();
const FILTER = new WeakMap();
const MESSAGES = {
    NOTHING_SELECTED:"Nothing is selected yet",
    ENTER_FORMULA:"Please enter in a formula."
};

const METADATA_TABLE_HEADERS = [{id: 'colName', displayVal: 'Column'},{id: 'colType', displayVal: 'Data Type'}, {id: 'colDesc', displayVal:'Description'}];

class BaseballController {
    /*@ngInject*/
    constructor($filter, BaseballDataService){
        BASEBALL.set(this, BaseballDataService);
        FILTER.set(this, $filter);
        BaseballDataService.getTables().success((resp) => {
            this.dataSets = resp;
        });

        this.metadataTable = {
            filterable:true,
            columns: METADATA_TABLE_HEADERS,
            data: [],
            query:{
                order: 'column'
            }
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
                this.metadataTable.data = resp.colMetaData;
            });
        }
    }

    getCurrentSelectedDataSet(){
    	if (this.selectedDataSet === undefined) {
            return MESSAGES.NOTHING_SELECTED;
        }
       	return this.selectedDataSet;
    }

    // Return the set of datasets 
    // Expecting a return of an array 
    // Empty array will indicate that nothing is found
    getFormula(){
        if(this.formula === undefined || this.formula.trim().length === 0) {
           return MESSAGES.ENTER_FORMULA;
        }
        return this.formula;
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