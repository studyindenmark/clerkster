function UserService(api) {
  var user = {
  	name: '',
  	email: '',
  	last_fetched: '',
    fetch: function() {
      var self = this;
      api.getUser().success(function(data) {
        self.name = data.name;
        self.email = data.email;
        self.avatar_url = data.avatar_url;
        self.last_fetched = data.last_fetched;

        if (!data.last_fetched) {
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
