let isLoggedIn = getCookie('isLoggedIn');

if (isLoggedIn === 'True') {
    window.location.replace("home.html");
}

let signIn = (event) => {
    event.preventDefault();
    document.getElementById('error-message').innerHTML = "";

    document.getElementById('username').style.borderBottomColor = "white";
    document.getElementById('password').style.borderBottomColor = "white";
    document.getElementById('error-message').style.color = "red";
    document.getElementById('fa-spin').style.display = "block";
    document.getElementById('submit').value = "Signing In";

    let uri = config.root + 'auth/login';

    let username = document.getElementById('username').value.toLowerCase();
    let password = document.getElementById('password').value;

    let options = {
        method: 'POST',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
        }),
        body: JSON.stringify({
            username: username,
            password: password
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('fa-spin').style.display = "none";
                document.getElementById('submit').value = "Sign In";

                return response.json();
            } else {
                document.getElementById('fa-spin').style.display = "none";
                document.getElementById('submit').value = "Sign In";
                return response.json();
            }
        })
        .then((j) => {

            if (j.hasOwnProperty('message')) {
                if (j['message'].hasOwnProperty('password')) {
                    document.getElementById('username').style.borderBottomColor = "red";
                }
                if (j['message'].hasOwnProperty('username')) {
                    document.getElementById('username').style.borderBottomColor = "red";
                }
                if (j['message'] === 'password or username is invalid') {
                    document.getElementById('username').style.borderBottomColor = "red";
                    document.getElementById('password').style.borderBottomColor = "red";
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] === 'account has been disabled') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                document.getElementById('error-message').style.color = "green";
                document.getElementById('error-message').innerHTML = "Login successful";

                let userData = j['data'][0]['user'];
                let access_token = j['data'][0]['token'];
                if (userData['othernames'] != null) {
                    othernames = userData['othernames'];
                } else {
                    othernames = '';
                }
                if (userData['phoneNumber'] != null) {
                    phonenumber = userData['phoneNumber'];
                } else {
                    phonenumber = '';
                }
                let name = userData['firstname'] + ' ' + userData['lastname'] + ' ' + othernames;
                let email = userData['email'];
                let username = userData['username'];
                let isAdmin = userData['isAdmin'];
                localStorage.setItem('profileName', name);
                localStorage.setItem('profilePhoneNumber', phonenumber);
                localStorage.setItem('profileFirstName', userData['firstname']);
                localStorage.setItem('profileLastName', userData['lastname']);
                localStorage.setItem('profileOtherName', othernames);
                localStorage.setItem('profileEmail', email);

                let expirationTime = 59;
                setCookie("token", access_token, expirationTime);
                setCookie("username", username, expirationTime);
                setCookie("isAdmin", isAdmin, expirationTime);
                setCookie("isLoggedIn", "True", expirationTime);

                window.location.replace("home.html");
            }

        })
        .catch((err) => {
            console.log(err);
        });
}

let signUp = (event) => {
    event.preventDefault();
    document.getElementById('error-message').innerHTML = "";
    document.getElementById('firstname').style.borderBottomColor = "white";
    document.getElementById('lastname').style.borderBottomColor = "white";
    document.getElementById('username').style.borderBottomColor = "white";
    document.getElementById('email').style.borderBottomColor = "white";
    document.getElementById('password').style.borderBottomColor = "white";
    document.getElementById('confirm_password').style.borderBottomColor = "white";
    document.getElementById('error-message').style.color = "red";
    document.getElementById('fa-spin').style.display = "block";
    document.getElementById('submit').value = "Signing Up";

    let uri = config.root + 'auth/signup';

    let firstname = document.getElementById('firstname').value;
    let lastname = document.getElementById('lastname').value;
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    let data = {
        firstname: firstname,
        lastname: lastname,
        username: username,
        email: email,
        password: password
    };

    if (password != confirm_password) {
        document.getElementById('fa-spin').style.display = "none";
        document.getElementById('submit').value = "Sign Up";
        document.getElementById('error-message').innerHTML = "Passwords do not match";
        document.getElementById('password').style.borderBottomColor = "red";
        document.getElementById('confirm_password').style.borderBottomColor = "red";
        return false;
    }

    let options = {
        method: 'POST',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
        }),
        body: JSON.stringify(data)
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('fa-spin').style.display = "none";
                document.getElementById('submit').value = "Sign Up";

                return response.json();
            } else {
                document.getElementById('fa-spin').style.display = "none";
                document.getElementById('submit').value = "Sign Up";
                return response.json();
            }
        })
        .then((j) => {
            if (j.hasOwnProperty('message')) {
                if (j['message'].hasOwnProperty('password')) {
                    document.getElementById('error-message').innerHTML = j['message']['password'];
                    document.getElementById('password').style.borderBottomColor = "red";
                }
                if (j['message'].hasOwnProperty('firstname')) {
                    document.getElementById('firstname').style.borderBottomColor = "red";
                }
                if (j['message'].hasOwnProperty('lastname')) {
                    document.getElementById('lastname').style.borderBottomColor = "red";
                }
                if (j['message'].hasOwnProperty('username')) {
                    document.getElementById('username').style.borderBottomColor = "red";
                }
                if (j['message'].hasOwnProperty('email')) {
                    document.getElementById('email').style.borderBottomColor = "red";
                }
                if (j['message'] == 'email already exists') {
                    document.getElementById('email').style.borderBottomColor = "red";
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] == 'username already exists') {
                    document.getElementById('username').style.borderBottomColor = "red";
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] == 'You have been registered successfully') {
                    document.getElementById('error-message').style.color = "green";
                    document.getElementById('error-message').innerHTML = j['message'];
                    window.location.replace("signin.html");
                }

            }

            if (j.hasOwnProperty('data')) {
                window.location.replace("signin.html");
            }

        })
        .catch((error) => {
            console.log(error);
        });
}

let requestReset = (event) => {
    event.preventDefault();
    document.getElementById('error-message').innerHTML = '';
    document.getElementById('fa-spin').style.display = "block";

    let useremail = document.getElementById('useremail').value;

    let uri = config.root + 'users/' + useremail + '/resetPassword';

    let options = {
        method: 'POST',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
        }),
        body: JSON.stringify({
            resetlink: config.resetlink
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('fa-spin').style.display = "none";

                return response.json();
            } else {
                document.getElementById('fa-spin').style.display = "none";
                return response.json();
            }
        })
        .then((j) => {
            let reset_message = `If a user account exists for ${useremail}, an email will be sent with further instructions`;
            if (j.hasOwnProperty('message')) {

                if (j['message'].hasOwnProperty('resetlink')) {
                    document.getElementById('error-message').innerHTML = 'resetlink key is missing';
                }
                if (j['message'] == 'user does not exist') {
                    document.getElementById('error-message').style.color = 'green';
                    document.getElementById('error-message').innerHTML = reset_message;
                    setTimeout(function () {
                        window.location.replace("signin.html");
                    }, 5000);
                }
                if (j['message'] == 'Reset link has been sent to your email') {
                    document.getElementById('error-message').style.color = 'green';
                    document.getElementById('error-message').innerHTML = reset_message;
                    setTimeout(function () {
                        window.location.replace("signin.html");
                    }, 5000);
                }
                if (j['message'] == 'Password reset failed please try again') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }

            }

        })
        .catch((err) => {
            console.log(err);

        });
}

let resetPassword = (event, profileusername, resettoken) => {
    event.preventDefault();
    document.getElementById('fa-spin-reset').style.display = "block";

    let uri = config.root + 'users/' + profileusername;

    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    if (password != confirm_password) {
        document.getElementById('fa-spin-reset').style.display = "none";
        document.getElementById('password').style.borderColor = "red";
        document.getElementById('confirm_password').style.borderColor = "red";
        return false;
    }

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
            "x-access-token": resettoken
        }),
        body: JSON.stringify({
            password: password
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json();
            }
        })
        .then((j) => {
            if (j.hasOwnProperty('message')) {
                if (j['message'] == 'Token is missing') {
                    document.getElementById('error-message').innerHTML = 'Token is missing';
                }
                if (j['message'] == 'Token is invalid') {
                    document.getElementById('error-message').innerHTML = 'Token is invalid or has expired';
                }
                if (j['message'] == 'User does not exist') {
                    warningNotification({
                        title: 'Warning',
                        message: j['message'],
                    });
                }
                if (j['message'].hasOwnProperty('password')) {
                    document.getElementById('password').style.borderColor = "red";
                    warningNotification({
                        title: 'Warning',
                        message: j['message']['password'],
                    });
                }
                if (j['message'] == 'Only an admin or the user can update their own password') {
                    warningNotification({
                        title: 'Warning',
                        message: j['message'],
                    });
                }

                if (j['message'] == 'User password has been changed') {
                    successNotification({
                        title: 'Success',
                        message: j['message'] + ' for ' + j['username'],
                    });
                    setTimeout(function () {
                        window.location.replace("signin.html");
                    }, 3000);

                }
            }

            document.getElementById('fa-spin-reset').style.display = "none";

        })
        .catch((err) => {
            console.log(err);
            document.getElementById('fa-spin-reset').style.display = "none";
        });
}