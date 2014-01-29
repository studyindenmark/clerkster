function PagesService(api, $rootScope) {
  var cache = {};

  function fetchPage(id, callback) {
    api.getPage(id).success(function(page) {
      if (cache.hasOwnProperty(id)) {
        var cached = cache[id];
        cached.name = page.name;
        cached.last_fetched = page.last_fetched;
        cached.authors = page.authors;
      } else {
        cache[id] = page;
      }

      if (callback) {
        callback(page);
      }

      if (!page.last_fetched) {
        setTimeout(function() {
          fetchPage(id); // Note: no callback.
        }, 1000);
      }
    });
  }

  var pages = {
    hasLoaded: false,
    list: [],

    get: function(id, callback) {
      if (cache.hasOwnProperty(id)) {
        callback(cache[id]);
        return;
      }

      fetchPage(id, callback);
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
