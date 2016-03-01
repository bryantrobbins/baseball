/**
 * a directive for a filterable, sortable table
**/

import _ from 'lodash';

const FILTER = new WeakMap();

class SortableTableController{
    constructor($filter){
        'ngInject';
        FILTER.set($filter);
        this.selectedColumns = [];
        this.filters = {};
    }
}

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
        'ngInject';
        this.template = require('./sortableTable.tpl.html');
        this.restrict = 'E';
        this.scope = {
            config:"="
        };
        this.controller = SortableTableController;
        this.controllerAs = 'ctrl';
    }
}

//yeah i'm pretty sure there's a better way of doing this...
export default {
    SortableTableDirective:SortableTableDirective,
    ColumnarFilter:ColumnarFilter
};
