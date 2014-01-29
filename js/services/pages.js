function PagesService(api, $rootScope) {

  var pages = {
    hasLoaded: false,
    list: [],
    fetch: function() {
      var self = this;
      api.getPages().success(function(data) {
        self.list = data;
        self.hasLoaded = true;
        $rootScope.$broadcast('pages_loaded', self);
      });
    },
  };

  return pages;
}
