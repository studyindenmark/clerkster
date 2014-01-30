function ApiService($http) {
  return {
    search: function(id, q) {
      return $http.get('/api/pages/' + id +'/search?q=' + q);
    },
    
    getPages: function() {
      return $http.get('/api/pages');
    },

    getPage: function(id) {
      return $http.get('/api/pages/' + id);
    },

    getUser: function() {
      return $http.get('/api/user');
    },

    saveSettings: function(args) {
      return $http.post('/api/settings', args);
    },
  };
}
