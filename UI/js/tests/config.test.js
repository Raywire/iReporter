const user = {
  token: 'token',
  name: 'John',
  email: 'john@doe.com',
  username: 'johndoe',
  isAdmin: true,
  isLoggedIn: 'False'
};

function givenUserExists(email, password) {
  Users.add(email, password);
}

var Users = {
  users: [],

  exists: function (email, password) {
    return this.users.length > 0;
  },

  add: function (email, password) { 
    this.users.push({email: email, password: password});
   }
}

