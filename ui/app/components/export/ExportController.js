
const DIALOG = Symbol();
const DATA_SVC = Symbol();
const EXPORT_TABLE_HEADERS = [{id: 'name', displayVal: 'Export Type'}];

class ExportController {
    constructor($mdDialog, BaseballDataService){
        this[DIALOG] = $mdDialog;
        this[DATA_SVC] = BaseballDataService;
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

    submitQuery(){
        var bundle = {
            table: this.selectedDataSet,
            metadata: this.selectedMetadata,
            exports: this.exportsTable.data
        };

        this[DATA_SVC].submitQuery(bundle);
    }

    closeDialog(){
        this[DIALOG].hide();
    }
}

ExportController.$inject = ['$mdDialog', 'BaseballDataService'];

export default ExportController;