function PageController($scope, $routeParams, $q, api) {
  $scope.pageId = $routeParams.page_id;
  $scope.author = '';

  api.getPage($scope.pageId).success(function(data) {
    $scope.page = data;
  });

  api.getPosts($scope.pageId).success(function(data) {
    $scope.posts = data;
    $scope.empty = $scope.posts.length === 0;
  });

  $scope.search = function() {
    var q = '';

    if ($scope.author) {
      q = 'author:' + $scope.author;
    }
    
    api.search($scope.pageId, q).success(function(data) {
      $scope.posts = data;
      $scope.empty = $scope.posts.length === 0;
    });
  };
}

