function Filter(api, $rootScope) {
    return {
        restrict: 'E',
        replace: true,
        scope: {
        	authors: '=',
        	hide: '=',
        },
        templateUrl: '/html/directives/filter.html',
        link: function (scope, element) {
        },
        controller: function($scope) {

            $scope.inFilter = function(author) {
                var ret = false;
                return ret;
            };

            $scope.removeFilter = function(author) {
                var filters2 = [];

                angular.forEach($rootScope.filters, function(item2) {
                    if (item2 !== item) {
                        filters2.push(item2);
                    }
                });

                $rootScope.filters = filters2;
            };

            $scope.addFilter = function(item) {
                $rootScope.filters.push(item);
            };

        	$scope.toggle = function(item) {
                if ($scope.inFilter(item)) {
                    $scope.removeFilter(item);
                } else {
                    $scope.addFilter(item);
                }
        	};

        },
    };
}