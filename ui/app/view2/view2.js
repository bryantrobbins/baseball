'use strict';

var view2Module = angular.module('app.view2', []);

function view2Controller(){
    console.info("This is view 2 controller");
}

export default view2Module.controller('view2Controller', view2Controller).name