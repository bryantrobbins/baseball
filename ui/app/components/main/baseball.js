'use strict';


import BaseballController from './BaseballController';
import BaseballDataService from './BaseballFactories';

var baseballModule = angular.module('app.main', [])
    .controller('BaseballController', BaseballController)
    .factory('BaseballDataFactory', BaseballDataService.BaseballDataFactory);

export default baseballModule.name;