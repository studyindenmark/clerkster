function PagesService(api, $rootScope) {
  var cache = {};

  var pages = {
    hasLoaded: false,
    list: [],

    get: function(id, callback) {
      if (cache.hasOwnProperty(id)) {
        callback(cache[id]);
        return;
      }

      api.getPage(id).success(function(data) {
        cache[id] = data;
        callback(data);
      });
    },

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
