function PostsController($scope, $routeParams, $q, api) {
  $scope.posts = [];
  $scope.pageId = $routeParams.page_id;

  function waitUntilPageIsFetched() {
    var deferred = $q.defer();

    function check() {
      api.getFetchLog($scope.pageId).success(function(logItems) {
        if (logItems.length > 0) {
          $scope.fetching = false;
          deferred.resolve();
        } else {
          $scope.fetching = true;
          setTimeout(check, 5000);
        }
      });
    }

    check();

    return deferred.promise;
  }

  function getPosts() {
    return api.getPosts($scope.pageId).success(function(data) {
      $scope.posts = data;
      $scope.empty = $scope.posts.length === 0;
    });
  }

  waitUntilPageIsFetched().then(getPosts);
}

