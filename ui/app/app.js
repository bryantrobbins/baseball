import md from 'angular-material';
import state from 'angular-ui-router';
import baseball from './components/baseball.js';
import baseballUtil from './components/util/util';
import mdDataTable from 'angular-material-data-table';
import config from './app.config';
import run from './app.run';

import 'angular-material/angular-material.min.css';
import 'angular-material-data-table/dist/md-data-table.min.css';


// Declare app level module which depends on views, and components
var mainModule = angular.module('app', [md,state,baseball, baseballUtil, mdDataTable, 'ngMockE2E']);
mainModule.config(config);
mainModule.run(run.runMocked);

