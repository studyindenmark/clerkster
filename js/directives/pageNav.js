function PageNav($location, api) {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      pageId: '=',
    },
    templateUrl: '/html/directives/pageNav.html',
    link: function (scope, element) {
      scope.isCurrentTab = function (tabName) {
        var split = $location.path().split('/');
        return tabName === split[3];
      };
    }
  };
}