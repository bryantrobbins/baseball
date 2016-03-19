
const DIALOG = Symbol();
const EXPORT_TABLE_HEADERS = [{id: 'name', displayVal: 'Export Type'}];

class ExportController {
    constructor($mdDialog, BaseballDataService){
        this[DIALOG] = $mdDialog;
        BaseballDataService.getExportData().then((response) => {
            this.exportsTable.data = response.data;
        });

        this.exportsTable = {
            title: 'Available Exports',
            filterable:false,
            columns: EXPORT_TABLE_HEADERS,
            data: [],
            selected: []
        };
    }

    closeDialog(){
        this[DIALOG].hide();
    }
}

ExportController.$inject = ['$mdDialog', 'BaseballDataService'];

export default ExportController;