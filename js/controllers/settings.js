function SettingsController($scope, $routeParams, api, user) {
  $scope.user = user;
  var timeout = null;

  $scope.save = function() {

    $scope.saved = false;

  	if (timeout) {
  		clearTimeout(timeout);
  	}

  	timeout = setTimeout(function() {
  		api.saveSettings({author: user.author}).success(function() {
        $scope.saved = true;
  		});
  	}, 1000);

  };
}
