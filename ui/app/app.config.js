/*@ngInject*/
export default function config($stateProvider, $urlRouterProvider, $mdThemingProvider){
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
}

