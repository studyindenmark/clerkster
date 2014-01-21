function WelcomeController($scope, $routeParams, api) {
	$scope.pages = [];
	$scope.loading = true;

	api.getPages().success(function(data) {
		$scope.pages = data;
		$scope.loading = false;
	});
}
