function UserService(api) {
  var user = {
  	name: '',
  	email: '',
  	last_fetched: '',
  };

  api.getUser().success(function(data) {
    user.name = data.name;
    user.email = data.email;
    user.avatar_url = data.avatar_url;
    user.last_fetched = data.last_fetched;
  });

  return user;
}
