'use strict';

import md from 'angular-material';
import state from 'angular-ui-router';
import view1 from './view1/view1.js';
import view2 from './view2/view2.js';
import version from './components/version/version.js';
import 'angular-material/angular-material.min.css';

// Declare app level module which depends on views, and components
angular.module('app', [state,view1,view2,version])
    .config(($stateProvider, $urlRouterProvider, $httpProvider, $provide)  => {

        $urlRouterProvider.otherwise('/placehold');

        $stateProvider.state('view1', {
            url: '/view1',
            template: require('./view1/view1.tpl.html')
        });

        $stateProvider.state('view2', {
            url: '/view2',
            template: require('./view2/view2.tpl.html')
        });
    });