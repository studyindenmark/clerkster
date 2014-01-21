function MainController($scope){$scope.$on("$routeChangeSuccess",function(){window.scrollTo(0,0)})}function PostsController($scope,$routeParams,api){$scope.posts=[],$scope.loading=!0,$scope.empty=!1,api.getPosts($routeParams.page_id).success(function(data){$scope.posts=data.data,$scope.loading=!1,$scope.empty=0===$scope.posts.length})}function ReportsController(){}function MainNav($location,api){return{restrict:"E",replace:!0,scope:{toggleMenu:"="},templateUrl:"/html/directives/mainNav.html",link:function(scope){scope.isCurrentPage=function(id){var split=$location.path().split("/pages/");return id===split[1]},api.getUser().success(function(data){scope.user=data}),api.getPages().success(function(data){scope.pages=data})}}}function ApiService($http){return{getPosts:function(id){return $http.get("/api/pages/"+id+"/feed")},getPages:function(){return $http.get("/api/pages")},getPage:function(id){return $http.get("/api/pages/"+id)},getUser:function(){return $http.get("/api/user")},getReports:function(){return $http.get("/api/reports")},getReport:function(reportId){return $http.get("/api/reports/"+reportId)}}}angular.module("clerkster",["ngAnimate","ngSanitize","ngRoute","angular-loading-bar"]).directive("mainNav",MainNav).factory("api",ApiService).config(["$routeProvider","$locationProvider",function($routeProvider,$locationProvider){$locationProvider.html5Mode(!0),$routeProvider.when("/pages/:page_id",{templateUrl:"/html/partials/posts.html",controller:PostsController}).when("/pages/:page_id/reports",{templateUrl:"/html/partials/reports.html",controller:ReportsController}).otherwise({redirectTo:"/"})}]);