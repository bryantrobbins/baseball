'use strict';

var view1Module = angular.module('app.view1', [])

function view1Controller(){
    console.info("This is view 1 controller");
}

export default view1Module.controller('view1Controller', view1Controller).name