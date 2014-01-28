function WelcomeController($scope, $routeParams, api) {
	api.getPages().success(function(data) {
		$scope.pages = data;
	});
}
