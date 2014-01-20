function ApiService($http) {
    
    return {

        getPosts: function() {
            return $http.get('/api/posts');
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
