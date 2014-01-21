function MainNav($location, api) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
    },
    templateUrl: '/html/directives/mainNav.html',
    link: function (scope, element) {
      scope.isCurrentPage = function (id) {
        var split = $location.path().split('/');
        return id === split[1];
      };

      api.getUser().success(function(data) {
        scope.user = data;
      });
    }
  };
}