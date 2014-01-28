function PageController($scope, $location, $routeParams, $q, api) {
  $scope.pageId = $routeParams.page_id;
  $scope.author = $routeParams.author || '';
  $scope.from = $routeParams.from || null;
  $scope.to = $routeParams.to || null;
  $scope.message = $routeParams.message || null;

  api.getPage($scope.pageId).success(function(data) {
    $scope.page = data;
  });

  var q =[];

  if ($scope.author) {
    q.push('author:' + $scope.author);
  }

  if ($scope.from) {
    q.push('created_time >= ' + $scope.from);
  }

  if ($scope.to) {
    q.push('created_time <= ' + $scope.to);
  }

  if ($scope.message) {
    q.push('message = \\"' + $scope.message + '\\"');
  }

  q = q.join(' AND ');

  api.search($scope.pageId, q).success(function(data) {
    $scope.posts = data;
    $scope.empty = $scope.posts.length === 0;
  });

  $scope.update = function() {
    $location.search('author', $scope.author || null);
    $location.search('from', $scope.from || null);
    $location.search('to', $scope.to || null);
    $location.search('message', $scope.message || null);
  };
}

