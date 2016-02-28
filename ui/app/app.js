'use strict';

import md from 'angular-material';
import state from 'angular-ui-router';
import baseball from './components/main/baseball.js';
import 'angular-material/angular-material.min.css';

// Declare app level module which depends on views, and components
angular.module('app', [md,state,baseball, 'ngMockE2E'])
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
            'Leema','The Nationals Suck :('];
        var metaResponse = {
            rowDesc: "Each row is a Team",
            colMetaData:[
                {colName:'playerID', colType:'String', colDesc:'The ID'},
                {colName:'yearID', colType:'Number', colDesc:'The Year'},
                {colName:'stint', colType:'Number', colDesc:'How long the player played'},
                {colName:'teamID', colType:'String', colDesc:'The team of the player'},
                {colName:'lgID', colType:'String', colDesc:'The Fuck is this?'},
                {colName:'G',colType:'String',colDesc:'Go'},
                {colName:'AB', colType:'String', colDesc:'I think this is at bat'},
                {colName:'R', colType:'Number', colDesc:'Runs'},
                {colName:'H', colType:'Number', colDesc:'Hits'},
                {colName:'2B', colType:'Number', colDesc:'Doubles'},
                {colName:'3B', colType:'Number', colDesc:'Triples'},
                {colName:'HR', colType:'Number', colDesc:'Home Runs'},
                {colName:'RBI', colType:'Number', colDesc:'Runs Batted In'},
                {colName:'SB', colType:'Number', colDesc:'Stolen Bases'},
                {colName:'CS', colType:'Number', colDesc:'Caught Stealing'},
                {colName:'BB', colType:'Number', colDesc:'Big Balls'},
                {colName:'SO', colType:'Number', colDesc:'Significant Others'},
                {colName:'IBB',colType:'Number', colDesc:'In Before Baseball'},
                {colName:'HBP',colType:'Number', colDesc:'Hello Big Puppy'},
                {colName:'SH',colType:'Number', colDesc:'Shits Taken'},
                {colName:'SF',colType:'Number', colDesc:'Shits Farted'},
                {colName:'GIDP', colType:'Number', colDesc:'Giddy P'}]};

        $httpBackend.whenGET(/.*\.tpl\.html/).passThrough();
        $httpBackend.whenGET(/.*\.svg/).passThrough();
        $httpBackend.whenGET(/.*\.css/).passThrough();

        $httpBackend.whenGET('/getDataSetNames').respond(tableResponse);
        $httpBackend.whenGET('/getDataSetMetadata').respond(metaResponse);
    });