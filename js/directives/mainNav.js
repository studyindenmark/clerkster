function MainNav($location, user, pages) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
    },
    templateUrl: '/html/directives/mainNav.html',
    link: function (scope, element) {
      function getPageFromUrl() {
        var split = $location.path().split('/');

        if (split[1] !== "pages") {
          return null;
        }

        return split[2];
      }

      scope.isOnPageScreen = function() {
        var split = $location.path().split('/');
        return split.length > 2 && split[1] === 'pages';
      };

      scope.openSelectedPage = function () {
        $location.path('/pages/' + scope.selectedPage);
      };

      scope.isCurrentPage = function (id) {
        var split = $location.path().split('/');
        return id === getPageFromUrl();
      };

      scope.user = user;
      scope.pages = pages;
      scope.selectedPage = getPageFromUrl();

      scope.$on('pages_loaded', function() {
        if (!scope.selectedPage && scope.pages.list.length > 0) {
          scope.selectedPage = scope.pages.list[0].id;
        }
      });
    }
  };
}