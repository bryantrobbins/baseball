import SortableTable from './SortableTable';

var baseballUtil = angular.module('app.util', [])
    .filter('columnarFilter', SortableTable.SortableTableController.ColumnarFilter)
    .directive('sortableTable', () => new SortableTable.SortableTableDirective);

export default baseballUtil.name;