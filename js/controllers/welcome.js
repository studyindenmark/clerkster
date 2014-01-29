function WelcomeController($scope, $routeParams, user, pages) {
  $scope.user = user;
  $scope.pages = pages;
  $scope.progress = 0;

  if (!user.last_fetched) {
    var interval = setInterval(function() {
      $scope.progress += (100 - $scope.progress) * 0.1;
      if (user.last_fetched) {
        clearInterval(interval);
      }
    }, 10);
  }
}
