angular.module('clerkster', ['ngAnimate', 'ngSanitize', 'ngRoute', 'angular-loading-bar'])
    .directive('mainNav', MainNav)
    .factory('api', ApiService)
    .factory('user', UserService)
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider
            .when('/pages', {
                templateUrl: '/html/partials/welcome.html',
                controller: WelcomeController,
            })
            .when('/pages/:page_id', {
                templateUrl: '/html/partials/page.html',
                controller: PageController,
            })
            .otherwise({redirectTo: '/pages'});
    }]);
