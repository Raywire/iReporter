function getData(user_data) {

    let uri = root + 'users';

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
            "x-access-token": token
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                try {
                    document.getElementById('fa-spin-data').style.display = "none";
                } catch {}

                return response.json();
            } else {
                try {
                    document.getElementById('fa-spin-data').style.display = "none";
                } catch {}
                return response.json();
            }
        })
        .then((j) => {

            if (j.hasOwnProperty('message')) {
                if (j['message'] == 'Token is missing') {
                    logout();
                }
                if (j['message'] == 'Token is invalid') {
                    logout();
                }
            }
            if (j.hasOwnProperty('data')) {
                let users = [];

                if (user_data == 'all' || user_data == '') {
                    users = j['data'];
                } else {
                    let allUsers = j['data'];
                    
                    users = allUsers.filter(user => {
                        if (user_data == 'true') {
                            user_data = true;
                        } else if (user_data == 'false') {
                            user_data = false
                        }
                        return user.username === user_data.toLowerCase() || user.firstname === user_data || user.email === user_data.toLowerCase() || user.lastname === user_data || user.isadmin === user_data.toLowerCase() || user.phonenumber === user_data;
                    })
                }

                (function () {
                    "use strict";

                    function Pagination() {

                        const prevButton = document.getElementById('button_prev');
                        const nextButton = document.getElementById('button_next');
                        const clickPageNumber = document.querySelectorAll('.clickPageNumber');
                        let perPage = document.getElementById('perPage').value;

                        let current_page = 1;
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
                            let page_number = document.getElementById('page_number').getElementsByClassName(
                                'clickPageNumber');
                            for (let i = 0; i < page_number.length; i++) {
                                if (i == current_page - 1) {
                                    page_number[i].style.opacity = "1.0";
                                } else {
                                    page_number[i].style.opacity = "0.5";
                                }
                            }
                        }

                        let checkButtonOpacity = function () {
                            current_page == 1 ? prevButton.classList.add('opacity') : prevButton.classList.remove(
                                'opacity');
                            current_page == numPages() ? nextButton.classList.add('opacity') : nextButton.classList.remove(
                                'opacity');
                        }

                        let changePage = function (page) {
                            const result = document.getElementById('user-data');

                            if (page < 1) {
                                page = 1;
                            }
                            if (page > (numPages() - 1)) {
                                page = numPages();
                            }

                            result.innerHTML = "";

                            if (users.length == 0) {
                                let result = '';
                                result += `
                                          <div class="column-100">
                                          <div class="card">
                                              <div class="container">
                                                  <p><i class="fa fa-star-half-o fa-3x" aria-hidden="true"></i></p>
                                                  <h4 class="theme-blue"><b>
                                                  We couldn't find an account for "${user_data}"
                                                  Make sure the email, username, first name, last name, phone number or status is spelled and formatted correctly
                                                  </b></h4>
                                              </div>
                                            </div>               
                                        </div> 
                                          `;
                                current_page = 0;
                                document.getElementById('startNumber').innerHTML = 0;
                                document.getElementById('endNumber').innerHTML = 0;
                                return document.getElementById('user-data').innerHTML = result;
                            }

                            for (let i = (page - 1) * recordsPerPage; i < (page * recordsPerPage) && i < users.length; i++) {

                                result.innerHTML +=
                                    `
                                      <div class="column">
                                        <div class="card">
                                            <div class="container2 align-center">
                                              <a href="view_user.html?username=${users[i].username}">
                                                <p><i class="fa fa-user-o fa-3x theme-blue" aria-hidden="true"></i></p>
                                                <h4 class="black"><b>${users[i].firstname} ${users[i].lastname}</b></h4>
                                                <p>${users[i].username}</p>
                                                <p class='italic font-small'>${users[i].email}</p>
                                                <p class='italic font-small'>Admin: ${users[i].isadmin}</p>
                                                <p class="black align-right"><i class="fa fa-external-link theme-blue" aria-hidden="true"></i></p>
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
                            if (current_page > 1) {
                                current_page--;
                                changePage(current_page);
                                document.getElementById('current_page').innerHTML = current_page;
                                startNumber -= recordsPerPage;
                                virtualEndNumber -= recordsPerPage;
                                document.getElementById('startNumber').innerHTML = startNumber;
                                document.getElementById('endNumber').innerHTML = virtualEndNumber;
                            }
                        }

                        let nextPage = function () {
                            if (current_page < numPages()) {
                                current_page++;
                                changePage(current_page);
                                document.getElementById('current_page').innerHTML = current_page;
                                startNumber += recordsPerPage;
                                endNumber += recordsPerPage;
                                virtualEndNumber += recordsPerPage;
                                if (endNumber > totalNumber) {
                                    endNumber = totalNumber;
                                }
                                if (endNumber == startNumber) {

                                }
                                document.getElementById('startNumber').innerHTML = startNumber;
                                document.getElementById('endNumber').innerHTML = endNumber;
                            }
                        }

                        let clickPage = function () {
                            document.addEventListener('click', function (e) {
                                if (e.target.nodeName == "SPAN" && e.target.classList.contains("clickPageNumber")) {
                                    current_page = e.target.textContent;
                                    changePage(current_page);
                                }
                            });
                        }

                        let pageNumbers = function () {
                            let pageNumber = document.getElementById('page_number');
                            pageNumber.innerHTML = "";
                            if (current_page == 0) {
                                current_page = 1;
                            }

                            pageNumber.innerHTML =
                                `<span class=''><span id='current_page'>${current_page}</span> of ${numPages()}</span>`;
                        }

                        let numPages = function () {
                            return Math.ceil(users.length / recordsPerPage);
                        }
                        let userNumber = document.getElementById('user_number');
                        userNumber.innerHTML =
                            `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${endNumber}</span> of ${totalNumber}`;
                    }

                    let pagination = new Pagination();
                    pagination.init();
                })();
            }

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('message').innerHTML = error;
        });
}

function getUserData() {

    let uri = root + 'users/' + usernameId;

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
            "x-access-token": token
        })
    }
    let request = new Request(uri, options);

    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('fa-spin-data').style.display = "none";

                return response.json();
            } else {
                document.getElementById('fa-spin-data').style.display = "none";
                return response.json();
            }
        })
        .then((j) => {

            if (j.hasOwnProperty('message')) {
                if (j['message'] == 'Token is missing') {
                    logout();
                }
                if (j['message'] == 'Token is invalid') {
                    logout();
                }
                if (j['message'] == 'Only admin can access this route') {
                    logout();
                }
                if (j['message'] == 'user does not exist') {
                    document.getElementById('message').innerHTML = j['message'];
                }
            }
            if (j.hasOwnProperty('data')) {
                let result = '';
                let fullname = '';
                j['data'].map((user) => {
                    const {
                        firstname,
                        lastname,
                        othernames,
                        username,
                        email,
                        phoneNumber,
                        isAdmin,
                        registered,
                        public_id
                    } = user
                    let localDateTime = convertToLocalTime(registered);
                    if (othernames == null) {
                        fullname = firstname + ' ' + lastname;
                    } else {
                        fullname = firstname + ' ' + lastname + ' ' + othernames;
                    }
                    if (phoneNumber == null) {
                        phone = 'None';
                    } else {
                        phone = phoneNumber;
                    }
                    result += `
                <h2>${fullname}</h2>
                <h3><span class="black">Admin Status:</span> <span id='status-data' class="italic">${isAdmin}</span></h3>
                <h4><span class="black">Created On:</span> <span class="italic">${localDateTime}</span></h4>
                <h4 id='comment-data'><span class="black">Public Id: </span>${public_id}</h4>
                <div class="row  bg-color">
                  <div class="column-50 bg-color">                       
                    <p><img src="img/img_avatar3.jpeg" alt=""></p>
                  </div>
                  <div class="column-50  bg-color align-justify">
                    <p id='comment-data'><span class="black">Email: </span>${email}</p>
                    <p id='comment-data'><span class="black">Phone Number: </span>${phone}</p>
                    <p id='comment-data'><span class="black">Username: </span>${username}</p>
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

function editUserData(event) {
    event.preventDefault();
    document.getElementById('fa-spin-edit-status').style.display = "block";
    document.getElementById('status-message').innerHTML = '';
    document.getElementById('status-message').style.color = "red";

    let uri = root + 'users/' + usernameId + '/promote';

    let status = document.getElementById('status').value;

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
            "x-access-token": token
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
                if (j['message'] == 'Token is missing') {
                    logout();
                }
                if (j['message'] == 'Token is invalid') {
                    logout();
                }
                if (j['message'] == 'Only admin can access this route') {
                    logout();
                }
                if (j['message'] == 'User does not exist') {
                    document.getElementById('status-message').innerHTML = j['message'];
                }
                if (j['message'].hasOwnProperty('isadmin')) {
                    document.getElementById('isadmin').style.borderBottomColor = "red";
                    document.getElementById('status-message').innerHTML = "(Accepted values: True, False)";
                }
                if (j['message'] == 'You cannot change the status of this user' || j['message'] == 'You cannot change your own admin status') {
                    document.getElementById('status-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                if (j['data']['message'] == "User status has been updated") {
                    document.getElementById('status-message').style.color = "green";
                    document.getElementById('status-message').innerHTML = j['data']['message'];
                    document.getElementById('status').value = status;
                    document.getElementById('status-data').innerHTML = status;
                }
            }
            document.getElementById('fa-spin-edit-status').style.display = "none";

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('fa-spin-edit-status').style.display = "none";
        });
}

function deleteUserData() {
    document.getElementById('fa-spin-data-delete').style.display = "block";
    document.getElementById('error-message').innerHTML = '';

    let uri = root + 'users/' + usernameId;

    let options = {
        method: 'DELETE',
        mode: "cors",
        headers: new Headers({
            "Content-Type": "application/json; charset=utf-8",
            "x-access-token": token
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
                    logout();
                }
                if (j['message'] == 'Token is invalid') {
                    logout();
                }
                if (j['message'] == 'user does not exist') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] == 'You cannot delete this user') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }
                if (j['message'] == 'A user who has posted incidents cannot be deleted') {
                    document.getElementById('error-message').innerHTML = j['message'];
                }

            }
            if (j.hasOwnProperty('data')) {
                if (j['data']['message'] == 'user record has been deleted') {
                    document.getElementById('error-message').innerHTML = j['data']['message'];
                    window.location.replace("admin.html");
                }
            }
            document.getElementById('fa-spin-data-delete').style.display = "none";

        })
        .catch((error) => {
            console.log(error);
            document.getElementById('fa-spin-data-delete').style.display = "none";
        });
}

function searchUsers(event) {
    event.preventDefault();
    showLoader();
    searchParameter = document.getElementById('searchUsers').value;
    getData(searchParameter);
    hideLoader(1000);
}

function hideLoader(timer) {
    setTimeout(hide, timer);

    function hide() {
        document.getElementById("loader").style.display = "none";
    }
}

function showLoader() {
    document.getElementById("loader").style.display = "block";
}