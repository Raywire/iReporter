let getUsers = (userdata) => {

    let uri = config.root + 'users';

    let options = {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({
            'Content-Type': 'application/json; charset=utf-8',
            'x-access-token': user.token
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                try {
                    document.getElementById('fa-spin-data').style.display = 'none';
                } catch (error) {}

                return response.json();
            } else {
                try {
                    document.getElementById('fa-spin-data').style.display = 'none';
                } catch (error) {}
                return response.json();
            }
        })
        .then((j) => {

            if (j.hasOwnProperty('message')) {
                if (j['message'] === 'Token is missing') {
                    logout();
                }
                if (j['message'] === 'Token is invalid') {
                    logout();
                }
            }
            if (j.hasOwnProperty('data')) {
                let users = [];

                if (userdata === 'all' || userdata === '') {
                    users = j['data'];
                } else {
                    let allUsers = j['data'];

                    users = allUsers.filter(user => {
                        if (userdata === 'true') {
                            userdata = true;
                        } else if (userdata === 'false') {
                            userdata = false
                        }
                        if (userdata === true || userdata === false) {
                            return user.isadmin === userdata
                        }
                        return user.username === userdata.toLowerCase() || user.firstname === userdata || user.email === userdata.toLowerCase() || user.lastname === userdata || user.phonenumber === userdata;
                    })
                }

                (function () {
                    'use strict';

                    function Pagination() {

                        const prevButton = document.getElementById('button_prev');
                        const nextButton = document.getElementById('button_next');
                        let perPage = document.getElementById('perPage').value;

                        let currentPage = 1;
                        let recordsPerPage = parseInt(perPage);
                        let startNumber = 1;
                        let totalNumber = users.length;

                        if (recordsPerPage > totalNumber) {
                            recordsPerPage = totalNumber;
                        }
                        let endNumber = recordsPerPage;
                        let virtualEndNumber = recordsPerPage;


                        this.init = function () {
                            changePage(1);
                            pageNumbers();
                            selectedPage();
                            clickPage();
                            addEventListeners();
                        }

                        let addEventListeners = function () {
                            nextButton.addEventListener('click', nextPage);
                            prevButton.addEventListener('click', prevPage);
                        }

                        let selectedPage = function () {
                            let pageNumber = document.getElementById('pageNumber').getElementsByClassName(
                                'clickPageNumber');
                            for (let i = 0; i < pageNumber.length; i++) {
                                if (i === currentPage - 1) {
                                    pageNumber[i].style.opacity = '1.0';
                                } else {
                                    pageNumber[i].style.opacity = '0.5';
                                }
                            }
                        }

                        let checkButtonOpacity = function () {
                            currentPage === 1 ? prevButton.classList.add('opacity') : prevButton.classList.remove(
                                'opacity');
                            currentPage === numPages() ? nextButton.classList.add('opacity') : nextButton.classList.remove(
                                'opacity');

                            document.getElementById('button_next').disabled = currentPage === numPages() ? true : false;
                            document.getElementById('button_prev').disabled = currentPage === 1 ? true : false;
                        }

                        let changePage = function (page) {
                            const result = document.getElementById('user-data');

                            if (page < 1) {
                                page = 1;
                            }
                            if (page > (numPages() - 1)) {
                                page = numPages();
                            }

                            result.innerHTML = '';

                            if (users.length === 0) {
                                let result = '';
                                result += `
                                          <div class='column-100'>
                                          <div class='card'>
                                              <div class='container'>
                                                  <p><i class='fa fa-star-half-o fa-3x' aria-hidden='true'></i></p>
                                                  <h4 class='theme-blue'><b>
                                                  We couldn't find an account for '${userdata}'
                                                  Make sure the email, username, first name, last name, phone number or status is spelled and formatted correctly
                                                  </b></h4>
                                              </div>
                                            </div>               
                                        </div> 
                                          `;
                                currentPage = 0;
                                document.getElementById('startNumber').innerHTML = 0;
                                document.getElementById('button_next').disabled = true;
                                document.getElementById('button_prev').disabled = true;
                                nextButton.classList.add('opacity');
                                return document.getElementById('user-data').innerHTML = result;
                            }
                            let faIcon;
                            let blocked;
                            for (let i = (page - 1) * recordsPerPage; i < (page * recordsPerPage) && i < users.length; i++) {
                                if (users[i].isactive === false) {
                                    faIcon = 'fa-ban red';
                                    blocked = 'blocked';
                                } else {
                                    faIcon = 'fa-unlock theme-blue';
                                    blocked = '';
                                }

                                result.innerHTML +=
                                    `
                                      <div class='column'>
                                        <div class='card'>
                                            <div class='container2 align-center  ${blocked}'>
                                              <a href='view_user.html?username=${users[i].username}'>
                                                <p class='black align-left'><i class='fa ${faIcon}' aria-hidden='true'></i></p>
                                                <p><i class='fa fa-user-o fa-3x theme-blue' aria-hidden='true'></i></p>
                                                <h4 class='black'><b>${users[i].firstname} ${users[i].lastname}</b></h4>
                                                <p>${users[i].username}</p>
                                                <p class='italic font-small'>${users[i].email}</p>
                                                <p class='italic font-small'>Admin: ${users[i].isadmin}</p>
                                                <p class='black align-right'><i class='fa fa-external-link theme-blue' aria-hidden='true'></i></p>
                                              </a>
                                            </div>
                                          </div>               
                                      </div>
                                `;
                            }
                            checkButtonOpacity();
                            selectedPage();
                        }

                        let prevPage = function () {
                            showLoader();
                            if (currentPage > 1) {
                                currentPage--;
                                changePage(currentPage);
                                document.getElementById('currentPage').innerHTML = currentPage;
                                startNumber -= recordsPerPage;
                                virtualEndNumber -= recordsPerPage;
                                userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${virtualEndNumber}</span>  of ${totalNumber}`;
                            }
                            if (currentPage === 1) {
                                endNumber = virtualEndNumber;
                            }
                            hideLoader(1000);
                        }

                        let nextPage = function () {
                            showLoader();
                            if (currentPage < numPages()) {
                                currentPage++;
                                changePage(currentPage);
                                document.getElementById('currentPage').innerHTML = currentPage;
                                startNumber += recordsPerPage;
                                endNumber += recordsPerPage;
                                virtualEndNumber += recordsPerPage;
                                if (endNumber > totalNumber) {
                                    endNumber = totalNumber;
                                }
                                if (endNumber === startNumber) {
                                    userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
                                } else {
                                    document.getElementById('startNumber').innerHTML = startNumber;
                                    document.getElementById('endNumber').innerHTML = endNumber;
                                }
                            }
                            hideLoader(1000);
                        }

                        let clickPage = function () {
                            document.addEventListener('click', function (e) {
                                if (e.target.nodeName === 'SPAN' && e.target.classList.contains('clickPageNumber')) {
                                    currentPage = e.target.textContent;
                                    changePage(currentPage);
                                }
                            });
                        }

                        let pageNumbers = function () {
                            let pageNumber = document.getElementById('pageNumber');
                            pageNumber.innerHTML = '';
                            let numberOfPages = numPages();
                            if (currentPage === 0) {
                                currentPage = numberOfPages = 1;
                            }

                            pageNumber.innerHTML =
                                `<span class=''><span id='currentPage'>${currentPage}</span> / ${numberOfPages}</span>`;
                        }

                        let numPages = function () {
                            return Math.ceil(users.length / recordsPerPage);
                        }
                        let userNumber = document.getElementById('user_number');
                        if (startNumber === endNumber || endNumber === 0) {
                            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
                        } else {
                            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${endNumber}</span>  of ${totalNumber}`;
                        }
                    }

                    let pagination = new Pagination();
                    pagination.init();
                })();
            }

        })
        .catch((error) => {
            console.log(error);
        });
}

let getUserData = (usernameid) => {

    let uri = config.root + 'users/' + usernameid;

    let options = {
        method: 'GET',
        mode: 'cors',
        headers: new Headers({
            'Content-Type': 'application/json; charset=utf-8',
            'x-access-token': user.token
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('fa-spin-data').style.display = 'none';

                return response.json();
            } else {
                document.getElementById('fa-spin-data').style.display = 'none';
                return response.json();
            }
        })
        .then((j) => {

            if (j.hasOwnProperty('message')) {
                if (j['message'] === 'Token is missing') {
                    logout();
                }
                if (j['message'] === 'Token is invalid') {
                    logout();
                }
                if (j['message'] === 'Only admin can access this route') {
                    logout();
                }
                if (j['message'] === 'user does not exist') {
                    document.getElementById('message').innerHTML = j['message'];
                }
            }
            if (j.hasOwnProperty('data')) {
                let result = '';
                let fullname = '';
                let phone = '';
                j['data'].map((user) => {
                    const {
                        firstname,
                        lastname,
                        othernames,
                        username,
                        email,
                        phoneNumber,
                        isAdmin,
                        isActive,
                        registered,
                        public_id
                    } = user;
                    let localDateTime = convertToLocalTime(registered);
                    if (othernames === null) {
                        fullname = firstname + ' ' + lastname;
                    } else {
                        fullname = firstname + ' ' + lastname + ' ' + othernames;
                    }
                    if (phoneNumber === null) {
                        phone = 'None';
                    } else {
                        phone = phoneNumber;
                    }
                    result += `
                <div class='incident-header'>
                    <h2>${fullname}</h2>
                    <h3><span class='black'>Active:</span> <span id='activity-data' class='italic'>${isActive}</span></h3>
                    <h3><span class='black'>Admin Status:</span> <span id='status-data' class='italic'>${isAdmin}</span></h3>
                    <h4><span class='black'>Created On:</span> <span class='italic'>${localDateTime}</span></h4>
                    <h4 id='comment-data'><span class='black'>Public Id: </span>${public_id}</h4>
                    <hr class='incident-line'>
                </div>
                <div class='row  bg-color'>
                  <div class='column-50 bg-color'>                       
                    <p><img src='img/img_avatar3.jpeg' alt=''></p>
                  </div>
                  <div class='column-50  bg-color align-justify'>
                    <p id='comment-data'><span class='black'>Email: </span>${email}</p>
                    <p id='comment-data'><span class='black'>Phone Number: </span>${phone}</p>
                    <p id='comment-data'><span class='black'>Username: </span>${username}</p>
                  </div>
                </div>  
                `;
                    document.getElementById('user-data').innerHTML = result;

                });

            }

        })
        .catch((error) => {
            console.log(error);
        });
}

let editUserData = (event, usernameid) => {
    event.preventDefault();
    document.getElementById('fa-spin-edit-status').style.display = 'block';
    document.getElementById('status-message').innerHTML = '';
    document.getElementById('status-message').style.color = 'red';

    let uri = config.root + 'users/' + usernameid + '/promote';

    let status = document.getElementById('status').value;

    let options = {
        method: 'PATCH',
        mode: 'cors',
        headers: new Headers({
            'Content-Type': 'application/json; charset=utf-8',
            'x-access-token': user.token
        }),
        body: JSON.stringify({
            isadmin: status
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
                if (j['message'] === 'Token is missing') {
                    logout();
                }
                if (j['message'] === 'Token is invalid') {
                    logout();
                }
                if (j['message'] === 'Only admin can access this route') {
                    logout();
                }
                if (j['message'] === 'User does not exist') {
                    document.getElementById('status-message').innerHTML = j['message'];
                }
                if (j['message'].hasOwnProperty('isadmin')) {
                    document.getElementById('isadmin').style.borderBottomColor = 'red';
                    document.getElementById('status-message').innerHTML = '(Accepted values: True, False)';
                }
                if (j['message'] === 'You cannot change the status of this user' || j['message'] === 'You cannot change your own admin status') {
                    document.getElementById('status-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                if (j['data']['message'] === 'User status has been updated') {
                    document.getElementById('status-message').style.color = 'green';
                    document.getElementById('status-message').innerHTML = j['data']['message'];
                    document.getElementById('status').value = status;
                    document.getElementById('status-data').innerHTML = status.toLowerCase();
                }
            }
            document.getElementById('fa-spin-edit-status').style.display = 'none';

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('fa-spin-edit-status').style.display = 'none';
        });
}

let changeActiveStatus = (event, usernameid) => {
    event.preventDefault();
    document.getElementById('fa-spin-activity').style.display = 'block';
    document.getElementById('activity-message').innerHTML = '';
    document.getElementById('activity-message').style.color = 'red';

    let uri = config.root + 'users/' + usernameid + '/activate';

    let activity = document.getElementById('activity').value;

    let options = {
        method: 'PATCH',
        mode: 'cors',
        headers: new Headers({
            'Content-Type': 'application/json; charset=utf-8',
            'x-access-token': user.token
        }),
        body: JSON.stringify({
            isactive: activity
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
                if (j['message'] === 'Token is missing') {
                    logout();
                }
                if (j['message'] === 'Token is invalid') {
                    logout();
                }
                if (j['message'] === "You cannot change this user's active status") {
                    document.getElementById('activity-message').innerHTML = j['message'];
                }
                if (j['message'] === 'user does not exist') {
                    document.getElementById('activity-message').innerHTML = j['message'];
                }
                if (j['message'].hasOwnProperty('isactive')) {
                    document.getElementById('activity-message').innerHTML = '(Accepted values: True, False)';
                }
                if (j['message'] === 'You cannot change your own active status') {
                    document.getElementById('activity-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                if (j['data']['message'] === 'User active status has been updated') {
                    document.getElementById('activity-message').style.color = 'green';
                    document.getElementById('activity-message').innerHTML = j['data']['message'];
                    document.getElementById('activity').value = activity;
                    document.getElementById('activity-data').innerHTML = activity.toLowerCase();
                }
            }
            document.getElementById('fa-spin-activity').style.display = 'none';

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('fa-spin-activity').style.display = 'none';
        });
}

let deleteUserData = (event, usernameid) => {
    event.preventDefault();
    document.getElementById('fa-spin-data-delete').style.display = 'block';
    document.getElementById('error-message').innerHTML = '';

    let uri = config.root + 'users/' + usernameid;

    let options = {
        method: 'DELETE',
        mode: 'cors',
        headers: new Headers({
            'Content-Type': 'application/json; charset=utf-8',
            'x-access-token': user.token
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
                if (j['message'] === 'Token is missing') {
                    logout();
                }
                if (j['message'] === 'Token is invalid') {
                    logout();
                }
                if (j['message'] === 'user does not exist') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] === 'You cannot delete this user') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] === 'A user who has posted incidents cannot be deleted') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                if (j['data']['message'] === 'user record has been deleted') {
                    document.getElementById('error-message').innerHTML = j['data']['message'];
                    window.location.replace('admin.html');
                }
            }
            document.getElementById('fa-spin-data-delete').style.display = 'none';

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('fa-spin-data-delete').style.display = 'none';
        });
}

let searchUsers = (event) => {
    event.preventDefault();
    showLoader();
    let searchParameter = document.getElementById('searchUsers').value;
    getUsers(searchParameter);
    hideLoader(1000);
}