function WelcomeController($scope, $routeParams, api, user, pages) {
	var interval;

	$scope.user = user;
  $scope.pages = pages;
  $scope.progress = 0;

  function getPages() {
    api.getPages().success(function(data) {
      $scope.pages = data;
    });
  }

  if (!user.last_fetched) {
		interval = setInterval(function() {
			$scope.progress += (100 - $scope.progress) * 0.1;
      if (user.last_fetched) {
        clearInterval(interval);
      }
		}, 10);
	}
}
