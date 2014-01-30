function SettingsController($scope, $routeParams, api, user) {
  $scope.user = user;
  var timeout = null;

  $scope.save = function() {

  	if (timeout) {
  		clearTimeout(timeout);
  	}

  	timeout = setTimeout(function() {
  		api.saveSettings({author: user.author}).success(function() {
		  	console.log('saving author', user.author);
  		});
  	}, 1000);

  };
}
