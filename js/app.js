angular.module('clerkster', ['ngAnimate', 'ngSanitize', 'ngRoute', 'angular-loading-bar'])
    .directive('mainNav', MainNav)
    .factory('api', ApiService)
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider
            .when('/pages/:page_id', {
                templateUrl: '/html/partials/posts.html',
                controller: PostsController,
            })
            .when('/pages/:page_id/reports', {
                templateUrl: '/html/partials/reports.html',
                controller: ReportsController,
            })
            .otherwise({redirectTo: '/'});
    }]);
