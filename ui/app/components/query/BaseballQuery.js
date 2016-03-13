class BaseballQueryDirective{
    constructor(){
        this.template = require('./baseballQuery.tpl.html');
        this.restrict = 'EA';
        this.scope = false;
    }
}

export default BaseballQueryDirective;