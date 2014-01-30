function UserService(api, pages) {
  var user = {
  	name: '',
    author: '',
    first_name: '',
    last_name: '',
  	email: '',
  	last_fetched: '',
    isLoaded: false,
    fetch: function() {
      var self = this;
      api.getUser().success(function(data) {
        self.isLoaded = true;
        self.name = data.name;
        self.author = data.author;
        self.first_name = data.first_name;
        self.last_name = data.last_name;
        self.email = data.email;
        self.avatar_url = data.avatar_url;
        self.last_fetched = data.last_fetched;

        if (data.last_fetched) {
          pages.fetch();
        } else {
          setTimeout(function() {
            self.fetch();
          }, 1000);
        }
      });
    }
  };

  user.fetch();

  return user;
}
