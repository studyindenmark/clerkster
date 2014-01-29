function MainNav($location, api, user) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
    },
    templateUrl: '/html/directives/mainNav.html',
    link: function (scope, element) {

      scope.user = user;

      function getPageFromUrl() {
        var split = $location.path().split('/');

        if (split[1] !== "pages") {
          return null;
        }

        return split[2];
      }

      scope.isOnWelcomeScreen = function() {
        return $location.path() === '/pages';
      };

      scope.openSelectedPage = function () {
        $location.path('/pages/' + scope.selectedPage);
      };

      scope.isCurrentPage = function (id) {
        var split = $location.path().split('/');
        return id === getPageFromUrl();
      };

      api.getPages().success(function(data) {
        scope.pages = data;
        scope.selectedPage = getPageFromUrl();
        if (!scope.selectedPage && scope.pages.length > 0) {
          scope.selectedPage = scope.pages[0].id;
        }
      });
    }
  };
}