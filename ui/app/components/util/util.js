import SortableTable from './SortableTable';

var baseballUtil = angular.module('app.util', [])
    .filter('columnarFilter', SortableTable.ColumnarFilter.Filter)
    .directive('sortableTable', () => new SortableTable.SortableTableDirective())
    .directive('cardSortableTable', () => new SortableTable.SortableTableCardDirective());


export default baseballUtil.name;