function PostsController($scope, $routeParams, api) {
    $scope.posts = [];
    $scope.page = null;

    api.getPage($routeParams.page_id).success(function(data) {
        $scope.page = data;
    });

    api.getPosts().success(function(data) {
        $scope.posts = data;
    });

}

