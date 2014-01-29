function WelcomeController($scope, $routeParams, api, user) {
	var interval;

	$scope.user = user;
  $scope.progress = 0;

  function getPages() {
    api.getPages().success(function(data) {
      $scope.pages = data;
    });
  }

  if (user.last_fetched) {
    getPages();
  } else {
		interval = setInterval(function() {
			$scope.progress += (100 - $scope.progress) * 0.1;
      if (user.last_fetched) {
        clearInterval(interval);
        getPages();
      }
		}, 10);
	}
}
