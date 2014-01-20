function MainController($scope){$scope.$on("$routeChangeSuccess",function(){window.scrollTo(0,0)})}function PostsController($scope,$location,$timeout,$rootScope,api){$scope.posts=[],$scope.search=!1,$scope.searchText="",void 0===$rootScope.filters&&($rootScope.filters=[]),$scope.showFilter=!1,$scope.hideProgramFilter=function(){$scope.showFilter=!1},$scope.lowerVirtualKeyboard=function(){$("input.search-box").blur()},$scope.hideProgramFilter=function(){$scope.showFilter=!1},api.getPosts().success(function(data){$scope.posts=data}),$scope.toggleSearch=function(flag){$scope.search=void 0===flag?!$scope.search:flag,$scope.search?setTimeout(function(){$("input.search").focus()},100):$scope.searchText=""},$scope.getNumberOfFilters=function(){return $rootScope.filters.length}}function ReportsController(){}function Filter(api,$rootScope){return{restrict:"E",replace:!0,scope:{authors:"=",hide:"="},templateUrl:"/html/directives/filter.html",link:function(){},controller:function($scope){$scope.inFilter=function(){var ret=!1;return ret},$scope.removeFilter=function(){var filters2=[];angular.forEach($rootScope.filters,function(item2){item2!==item&&filters2.push(item2)}),$rootScope.filters=filters2},$scope.addFilter=function(item){$rootScope.filters.push(item)},$scope.toggle=function(item){$scope.inFilter(item)?$scope.removeFilter(item):$scope.addFilter(item)}}}}function MainNav($location,api){return{restrict:"E",replace:!0,scope:{toggleMenu:"="},templateUrl:"/html/directives/mainNav.html",link:function(scope){scope.isCurrentPath=function(path){var split1=path.split("/"),split2=$location.path().split("/");return split1[1]===split2[1]},api.getUser().success(function(data){scope.user=data})}}}function ApiService($http){return{getPosts:function(){return $http.get("/api/posts")},getUser:function(){return $http.get("/api/user")},getReports:function(){return $http.get("/api/reports")},getReport:function(reportId){return $http.get("/api/reports/"+reportId)}}}angular.module("clerkster",["ngAnimate","ngSanitize","ngRoute","angular-loading-bar"]).directive("filter",Filter).directive("mainNav",MainNav).factory("api",ApiService).config(["$routeProvider","$locationProvider",function($routeProvider,$locationProvider){$locationProvider.html5Mode(!0),$routeProvider.when("/posts",{templateUrl:"/html/partials/posts.html",controller:PostsController}).when("/reports",{templateUrl:"/html/partials/reports.html",controller:ReportsController}).otherwise({redirectTo:"/posts"})}]);