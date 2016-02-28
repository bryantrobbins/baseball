class BaseballController {
    constructor(){
        this.hello = "Welcome to the BaseBall Workbench where all your primal needs will be satisfied";
        this.selectedDataSet = undefined;
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
    getDataSets(searchText)
    {
    	if (searchText === "blah")
    		return ["blah"];
    	else if (searchText === "undefined")
    		return [];
    	return ["blah1", "blah2", "blah3"];
    }

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

export default BaseballController;