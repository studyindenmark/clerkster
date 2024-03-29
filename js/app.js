angular.module('clerkster', ['ngAnimate', 'ngSanitize', 'ngRoute', 'angular-loading-bar'])
    .directive('mainNav', MainNav)
    .factory('api', ApiService)
    .factory('pages', PagesService)
    .factory('user', UserService)
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider
            .when('/settings', {
                templateUrl: '/html/partials/settings.html',
                controller: SettingsController,
            })
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
