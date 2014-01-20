function PostsController($scope, $location, $timeout, $rootScope, api) {
    $scope.posts = [];
    $scope.search = false;
    $scope.searchText = "";

    // TODO move filters to separate service
    if ($rootScope.filters === undefined)
        $rootScope.filters = [];

    $scope.showFilter = false;

    $scope.hideProgramFilter = function() {
        $scope.showFilter = false;
    };

    $scope.lowerVirtualKeyboard = function() {
        $('input.search-box').blur();
    };

    $scope.hideProgramFilter = function() {
        $scope.showFilter = false;
    };

    api.getPosts().success(function(data) {
        $scope.posts = data;
    });

    $scope.toggleSearch = function(flag) {
        if (flag === undefined) {
            $scope.search = !$scope.search;
        } else {
            $scope.search = flag;
        }

        if ($scope.search) {
            setTimeout(function() {
                $('input.search').focus();
            }, 100);
        } else {
            $scope.searchText = "";
        }
    };

    $scope.getNumberOfFilters = function() {
        return $rootScope.filters.length;
    };
}

