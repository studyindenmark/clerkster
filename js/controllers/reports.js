function ReportsController($scope, $routeParams, api) {
    $scope.pageId = $routeParams.page_id;
    $scope.user = {};

    api.getUser().success(function(data) {
      $scope.user = data;
    });
}
