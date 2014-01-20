angular.module('clerkster', ['ngAnimate', 'ngSanitize', 'ngRoute', 'angular-loading-bar'])
    .directive('filter', Filter)
    .directive('mainNav', MainNav)
    .factory('api', ApiService)
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider
            .when('/posts', {
                templateUrl: '/html/partials/posts.html',
                controller: PostsController,
            })
            .when('/reports', {
                templateUrl: '/html/partials/reports.html',
                controller: ReportsController,
            })
            .otherwise({redirectTo: '/posts'});
    }]);
