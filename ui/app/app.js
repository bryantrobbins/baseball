'use strict';

import md from 'angular-material';
import state from 'angular-ui-router';
import baseball from './components/main/baseball.js';
import 'angular-material/angular-material.min.css';

// Declare app level module which depends on views, and components
angular.module('app', [md,state,baseball])
    .config(($stateProvider, $urlRouterProvider, $mdThemingProvider)  => {

        $urlRouterProvider.otherwise('/baseball');

        $stateProvider.state('baseball', {
            url: '/baseball',
            controller: 'BaseballController',
            controllerAs: 'BaseballCtrl',
            template: require('./components/main/baseball.tpl.html')
        });

        $mdThemingProvider.theme('default')
            .primaryPalette('green')
            // If you specify less than all of the keys, it will inherit from the
            // default shades
            .accentPalette('purple');
    });