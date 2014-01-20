function MainController($scope) {

    $scope.$on('$routeChangeSuccess', function() {
        window.scrollTo(0, 0);
    });

}