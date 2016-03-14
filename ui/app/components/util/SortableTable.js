/**
 * a directive for a filterable, sortable table
**/

import _ from 'lodash';

const FILTER = new WeakMap();

class SortableTableController{
    constructor($filter){
        FILTER.set($filter);
        this.selectedColumns = [];
        this.filters = {};
    }
}

SortableTableController.$inject = ['$filter'];

class ColumnarFilter{
    constructor(){

    }

    static Filter() {
        return function (values, input) {
            if (_.size(input) === 0) {
                return values;
            } else {
                var result = values;
                _.forEach(input, (value, column) => {
                    result = _.intersection(result, _.filter(values, (o) => {
                            return o[column].indexOf(value) !== -1;
                        })
                    );
                });
                return result;
            }
        };
    }
}

class SortableTableDirective{
    constructor(){
        this.template = require('./sortableTable.tpl.html');
        this.restrict = 'EA';
        this.scope = {
            config:"="
        };
        this.controller = SortableTableController;
        this.controllerAs = 'ctrl';
    }
}

class SortableTableCardDirective{
    constructor(){
        this.template = require('./cardSortableTable.tpl.html');
        this.restrict = 'EA';
        this.scope = {
            title:"=",
            config:"="
        };
        this.controller = SortableTableController;
        this.controllerAs = 'ctrl';
    }
}

//yeah i'm pretty sure there's a better way of doing this...
export default {
    SortableTableCardDirective:SortableTableCardDirective,
    SortableTableDirective:SortableTableDirective,
    ColumnarFilter:ColumnarFilter
};
