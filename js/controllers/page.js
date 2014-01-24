function PageController($scope, $routeParams, $q, api) {
  $scope.pageId = $routeParams.page_id;

  api.getPosts($scope.pageId).success(function(data) {
    $scope.posts = data;
    $scope.empty = $scope.posts.length === 0;
  });
}

