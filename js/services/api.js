function ApiService($http) {
    
    return {

        getPages: function() {
            return $http.get('/api/pages');
        },

        search: function(id, q) {
            return $http.get('/api/pages/' + id +'/search?q=' + q);
        },

        getPage: function(id) {
            return $http.get('/api/pages/' + id);
        },

        getUser: function() {
            return $http.get('/api/user');
        },

        getReports: function() {
            return $http.get('/api/reports');
        },

        getReport: function(reportId) {
            return $http.get('/api/reports/' + reportId);
        },

    };
}
