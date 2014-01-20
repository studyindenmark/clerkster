function MainNav($location, api) {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            toggleMenu: '='
        },
        templateUrl: '/html/directives/mainNav.html',
        link: function (scope, element) {
            scope.isCurrentPath = function (path) {
                var split1 = path.split('/');
                var split2 = $location.path().split('/');
                return split1[1] === split2[1];
            };

            api.getUser().success(function(data) {
                scope.user = data;
            });
        }
    };
}