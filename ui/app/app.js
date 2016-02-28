'use strict';

import md from 'angular-material';
import state from 'angular-ui-router';
import baseball from './components/main/baseball.js';
import mdDataTable from 'angular-material-data-table';

import 'angular-material/angular-material.min.css';

import 'angular-material-data-table/dist/md-data-table.min.css';


// Declare app level module which depends on views, and components
angular.module('app', [md,state,baseball, mdDataTable, 'ngMockE2E'])
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
    })
    .run(($httpBackend) => {
        //where shit gets mocked for now
        var tableResponse = ['Steves Baseball', 'BTR3Ball', 'Chaos Sluggers', 'SheppJaks Baseball',
            'Leema','The Nationals Suck'];
        var metaResponse = {
            rowDesc: "Each row is a Player Stint - a set of games that a single player participated in for a single team in a single season. A player may have multiple stints within a single season, and each will have a unique value in the 'stint' column.",
            colMetaData:[
                {colName:'playerID', colType:'String', colDesc:'The ID'},
                {colName:'yearID', colType:'Number', colDesc:'The Year'},
                {colName:'stint', colType:'Number', colDesc:'ID for this sequence of games (unique to player and year)'},
                {colName:'teamID', colType:'String', colDesc:'The team of the player'},
                {colName:'lgID', colType:'String', colDesc:'League ID'},
                {colName:'G',colType:'Count',colDesc:'Games'},
                {colName:'AB', colType:'Count', colDesc:'At Bats'},
                {colName:'R', colType:'Count', colDesc:'Runs'},
                {colName:'H', colType:'Count', colDesc:'Hits'},
                {colName:'2B', colType:'Count', colDesc:'Doubles'},
                {colName:'3B', colType:'Count', colDesc:'Triples'},
                {colName:'HR', colType:'Count', colDesc:'Home Runs'},
                {colName:'RBI', colType:'Count', colDesc:'Runs Batted In'},
                {colName:'SB', colType:'Count', colDesc:'Stolen Bases'},
                {colName:'CS', colType:'Count', colDesc:'Caught Stealing'},
                {colName:'BB', colType:'Count', colDesc:'Walks (Base on Balls)'},
                {colName:'SO', colType:'Count', colDesc:'Strikeouts'},
                {colName:'IBB',colType:'Count', colDesc:'Intentional Walks'},
                {colName:'HBP',colType:'Count', colDesc:'Hit By Pitch'},
                {colName:'SH',colType:'Count', colDesc:'Sacrifice Hits'},
                {colName:'SF',colType:'Count', colDesc:'Sacrifice Flies'},
                {colName:'GIDP', colType:'Count', colDesc:'Grounded Into Double Play'}]};

        $httpBackend.whenGET(/.*\.tpl\.html/).passThrough();
        $httpBackend.whenGET(/.*\.svg/).passThrough();
        $httpBackend.whenGET(/.*\.css/).passThrough();

        $httpBackend.whenGET('/getDataSetNames').respond(tableResponse);
        $httpBackend.whenGET('/getDataSetMetadata').respond(metaResponse);
    });
