import BaseballController from './main/BaseballController';
import BaseballDataService from './main/BaseballDataService';
import BaseballQuery from './query/BaseballQuery';

var baseballModule = angular.module('app.main', [])
    .controller('BaseballController', BaseballController)
        .filter('BaseballFilter', BaseballController.BaseballFilter)
    .service('BaseballDataService', BaseballDataService)
    .directive('baseballQuery',  () => new BaseballQuery());

export default baseballModule.name;