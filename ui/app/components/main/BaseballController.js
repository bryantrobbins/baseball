const BASEBALL = new WeakMap();

class BaseballController {
    constructor(BaseballDataFactory){
        console.info(BaseballDataFactory);
        BASEBALL.set(this, BaseballDataFactory);
        this.hello = "Welcome to the BaseBall Workbench where all your primal needs will be satisfied";
        this.selectedDataSet = undefined;
        BaseballDataFactory.getTables().success((resp) => {
            this.dataSets = resp;
        })

    }

    playBall(){
        return "PLAY BALL!";
    }

    getListOfDataSets(){

    }

    getCurrentSelectedDataSet(){
    	if (this.selectedDataSet == undefined)
    		return "Nothing is selected yet";
       	return this.selectedDataSet;
    }

    // Return the set of datasets 
    // Expecting a return of an array 
    // Empty array will indicate that nothing is found

    getFormula(){
        if(this.formula == undefined)
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