import BaseballController from './BaseballController';
import BaseballDataService from './BaseballDataService';

var baseballModule = angular.module('app.main', [])
    .controller('BaseballController', BaseballController)
        .filter('BaseballFilter', BaseballController.BaseballFilter)
    .service('BaseballDataService', BaseballDataService);

export default baseballModule.name;