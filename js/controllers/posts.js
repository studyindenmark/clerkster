function PostsController($scope, $routeParams, api) {
    $scope.posts = [];
    $scope.loading = true;
    $scope.empty = false;

    api.getPosts($routeParams.page_id).success(function(data) {
        $scope.posts = data.data;
        $scope.loading = false;
        $scope.empty = $scope.posts.length === 0;
    });

}

