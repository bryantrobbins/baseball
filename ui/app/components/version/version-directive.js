'use strict';

export default angular.module('app.version.version-directive', [])
.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]).name;
