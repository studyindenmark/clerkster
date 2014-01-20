function MainNav($location, api) {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            toggleMenu: '='
        },
        templateUrl: '/html/directives/mainNav.html',
        link: function (scope, element) {
            scope.isCurrentPage = function (id) {
                var split = $location.path().split('/pages/');
                return id === split[1];
            };

            api.getUser().success(function(data) {
                scope.user = data;
            });

            api.getPages().success(function(data) {
                scope.pages = data;
            });
        }
    };
}