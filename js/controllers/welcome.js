function WelcomeController($scope, $routeParams, api, user) {
	api.getPages().success(function(data) {
		$scope.pages = data;
	});
}
