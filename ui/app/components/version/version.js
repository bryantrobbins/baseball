'use strict';

import interpolate from './interpolate-filter'
import version from './version-directive'

export default angular.module('app.version', [interpolate, version])

.value('version', '0.1').name;
