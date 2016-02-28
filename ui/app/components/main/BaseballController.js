const BASEBALL = new WeakMap();

class BaseballController {
    constructor(BaseballDataFactory){
        BASEBALL.set(this, BaseballDataFactory);
        this.hello = "Welcome to the Baseball Workbench";
        BaseballDataFactory.getTables().success((resp) => {
            this.dataSets = resp;
        });
    }

    getMetadata(){
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
}

BaseballController.$inject = ['BaseballDataFactory'];

export default BaseballController;