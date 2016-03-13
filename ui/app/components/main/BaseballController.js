import _ from 'lodash';


const BASEBALL = Symbol();
const MESSAGES = {
    NOTHING_SELECTED:"Nothing is selected yet",
    ENTER_FORMULA:"Please enter in a formula."
};

const METADATA_TABLE_HEADERS = [{id: 'colName', displayVal: 'Column'},{id: 'colType', displayVal: 'Data Type'}, {id: 'colDesc', displayVal:'Description'}];

class BaseballController {
    constructor(BaseballDataService){
        this[BASEBALL] = BaseballDataService;
		BaseballDataService.getTables().then((resp) => {
			this.dataSets = resp.data;
        });
        this.filters = {
            groupBy: {
                desc: "Group By"
            },
            orderBy: {
                desc: "Order By"
            }

        };

        this.metadataTable = {
            title: 'Available Data',
            subTitle: '',
            filterable:true,
            columns: METADATA_TABLE_HEADERS,
            data: [],
            selected: [],
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
          this[BASEBALL].getTableMetadata(this.selectedDataSet).then((resp) => {
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
}

export default BaseballController;