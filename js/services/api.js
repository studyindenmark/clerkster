function ApiService($http) {
    
    return {

        getPosts: function(id) {
            return $http.get('/api/pages/' + id + '/posts');
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

        getReports: function() {
            return $http.get('/api/reports');
        },

        getReport: function(reportId) {
            return $http.get('/api/reports/' + reportId);
        },

    };
}
