const getUsers = (userdata) => {
  const getUsersUri = `${config.root}users`;

  const options = {
    method: 'GET',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
  };
  const getUsersRequest = new Request(getUsersUri, options);

  fetch(getUsersRequest)
    .then((getUsersResponse) => {
      if (getUsersResponse.ok) {
        return getUsersResponse.json();
      }
      return getUsersResponse.json();
    })
    .then((usersData) => {
      if (Object.prototype.hasOwnProperty.call(usersData, 'message')) {
        if (usersData.message === 'Token is missing') {
          logout();
        }
        if (usersData.message === 'Token is invalid') {
          logout();
        }
      }
      if (Object.prototype.hasOwnProperty.call(usersData, 'data')) {
        let users = [];

        if (userdata === 'all' || userdata === '') {
          users = usersData.data;
        } else {
          const allUsers = usersData.data;

          users = allUsers.filter((user) => {
            let userStatus = '';
            if (userdata === 'true') {
              userStatus = true;
            } else if (userdata === 'false') {
              userStatus = false;
            }
            if (userStatus === true || userStatus === false) {
              return user.isadmin === userStatus;
            }
            return user.username === userdata.toLowerCase() || user.firstname === userdata
             || user.email === userdata.toLowerCase() || user.lastname === userdata
             || user.phonenumber === userdata;
          });
        }

        const UserFn = function UserPagination() {
          const previousButton = document.getElementById('button_prev');
          const nextButton = document.getElementById('button_next');
          const userNumber = document.getElementById('user_number');
          const perPage = document.getElementById('perPage').value;

          let currentPage = 1;
          let usersPerPage = parseInt(perPage, 10);
          let startNumber = 1;
          const totalNumber = users.length;

          if (usersPerPage > totalNumber) {
            usersPerPage = totalNumber;
          }
          let userEndNumber = usersPerPage;
          let virtualUserEndNumber = usersPerPage;

          const selectedUserPage = () => {
            const userPageNumber = document.getElementById('pageNumber').getElementsByClassName('clickPageNumber');
            for (let i = 0; i < userPageNumber.length; i += 1) {
              if (i === currentPage - 1) {
                userPageNumber[i].style.opacity = '1.0';
              } else {
                userPageNumber[i].style.opacity = '0.5';
              }
            }
          };

          const numUserPages = () => {
            const numOfUserPages = Math.ceil(users.length / usersPerPage);
            return numOfUserPages;
          };

          const checkButtonOpacity = () => {
            if (currentPage === 1) {
              previousButton.classList.add('opacity');
            } else {
              previousButton.classList.remove('opacity');
            }
            if (currentPage === numUserPages()) {
              nextButton.classList.add('opacity');
            } else {
              nextButton.classList.remove('opacity');
            }

            document.getElementById('button_prev').disabled = currentPage === 1;
            document.getElementById('button_next').disabled = currentPage === numUserPages();
          };

          const changeUserPage = (page) => {
            const result = document.getElementById('user-data');
            let pageN = page;

            if (pageN < 1) {
              pageN = 1;
            }
            if (pageN > (numUserPages() - 1)) {
              pageN = numUserPages();
            }

            result.innerHTML = '';

            if (users.length === 0) {
              let resultNone = '';
              resultNone += `
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
              document.getElementById('button_prev').disabled = true;
              document.getElementById('button_next').disabled = true;
              previousButton.classList.add('opacity');
              nextButton.classList.add('opacity');
              document.getElementById('user-data').innerHTML = resultNone;
            } else {
              let faIcon;
              let blocked;
              const upp = usersPerPage;
              for (let i = (pageN - 1) * upp; i < (pageN * upp) && i < users.length; i += 1) {
                if (users[i].isactive === false) {
                  faIcon = 'fa-ban red';
                  blocked = 'blocked';
                } else {
                  faIcon = 'fa-unlock theme-blue';
                  blocked = '';
                }

                result.innerHTML += `
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
              selectedUserPage();
            }
          };

          const previousUserPage = () => {
            showLoader();
            if (currentPage > 1) {
              currentPage -= 1;
              changeUserPage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber -= usersPerPage;
              virtualUserEndNumber -= usersPerPage;
              userEndNumber -= usersPerPage;
              userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='userEndNumber'>${virtualUserEndNumber}</span>  of ${totalNumber}`;
            }
            if (currentPage === 1) {
              userEndNumber = virtualUserEndNumber;
            }
            hideLoader(1000);
          };

          const nextUserPage = () => {
            showLoader();
            if (currentPage < numUserPages()) {
              currentPage += 1;
              changeUserPage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber += usersPerPage;
              userEndNumber += usersPerPage;
              virtualUserEndNumber += usersPerPage;
              if (userEndNumber > totalNumber) {
                userEndNumber = totalNumber;
              }
              if (userEndNumber === startNumber) {
                userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
              } else {
                userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='userEndNumber'>${userEndNumber}</span>  of ${totalNumber}`;
              }
            }
            hideLoader(1000);
          };

          const addEventListeners = () => {
            previousButton.addEventListener('click', previousUserPage);
            nextButton.addEventListener('click', nextUserPage);
          };

          const clickUserPage = () => {
            document.addEventListener('click', (e) => {
              if (e.target.nodeName === 'SPAN' && e.target.classList.contains('clickPageNumber')) {
                currentPage = e.target.textContent;
                changeUserPage(currentPage);
              }
            });
          };

          const userPageNumbers = () => {
            const pageNumber = document.getElementById('pageNumber');
            pageNumber.innerHTML = '';
            let numberOfPages = numUserPages();
            if (currentPage === 0) {
              numberOfPages = 1;
              currentPage = 1;
            }

            pageNumber.innerHTML = `<span class=''><span id='currentPage'>${currentPage}</span> / ${numberOfPages}</span>`;
          };

          this.init = () => {
            clickUserPage();
            changeUserPage(1);
            selectedUserPage();
            userPageNumbers();
            addEventListeners();
          };

          if (startNumber === userEndNumber || userEndNumber === 0) {
            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
          } else {
            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='userEndNumber'>${userEndNumber}</span>  of ${totalNumber}`;
          }
        };

        const userpagination = new UserFn();
        userpagination.init();
      }
    })
    .catch(() => {

    });
};

const getUserData = (usernameid) => {
  const getUserUri = `${config.root}users/${usernameid}`;

  const options = {
    method: 'GET',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
  };
  const userDataRequest = new Request(getUserUri, options);

  fetch(userDataRequest)
    .then((userDataResponse) => {
      if (userDataResponse.ok) {
        document.getElementById('fa-spin-data').style.display = 'none';

        return userDataResponse.json();
      }
      document.getElementById('fa-spin-data').style.display = 'none';
      return userDataResponse.json();
    })
    .then((userData) => {
      if (Object.prototype.hasOwnProperty.call(userData, 'message')) {
        if (userData.message === 'Token is missing') {
          logout();
        }
        if (userData.message === 'Token is invalid') {
          logout();
        }
        if (userData.message === 'Only admin can access this route') {
          logout();
        }
        if (userData.message === 'user does not exist') {
          document.getElementById('message').innerHTML = userData.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(userData, 'data')) {
        let result = '';
        let fullname = '';
        let phone = '';
        let profilePhoto = '';
        userData.data.forEach((user) => {
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
            public_id: publicId,
            photourl,
          } = user;
          const localDateTime = convertToLocalTime(registered);

          if (photourl === null) {
            profilePhoto = 'img/img_avatar3.jpeg';
          } else {
            profilePhoto = photourl;
          }

          if (othernames === null) {
            fullname = `${firstname} ${lastname}`;
          } else {
            fullname = `${firstname} ${lastname} ${othernames}`;
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
                    <h4 id='comment-data'><span class='black'>Public Id: </span>${publicId}</h4>
                    <hr class='incident-line'>
                </div>
                <div class='row  bg-color'>
                  <div class='column-50 bg-color'>                       
                    <p><img class='profilePhoto' src='${profilePhoto}' alt='Profile Photo for ${fullname}'></p>
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
    .catch(() => {

    });
};

const editUserData = (event, usernameid) => {
  event.preventDefault();
  document.getElementById('fa-spin-edit-status').style.display = 'block';
  document.getElementById('status-message').innerHTML = '';
  document.getElementById('status-message').style.color = 'red';

  const promoteUserUri = `${config.root}users/${usernameid}/promote`;

  const status = document.getElementById('status').value;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
    body: JSON.stringify({
      isadmin: status,
    }),
  };
  const promoteUserRequest = new Request(promoteUserUri, options);

  fetch(promoteUserRequest)
    .then((promoteUserResponse) => {
      if (promoteUserResponse.ok) {
        return promoteUserResponse.json();
      }
      return promoteUserResponse.json();
    })
    .then((promoteUserData) => {
      if (Object.prototype.hasOwnProperty.call(promoteUserData, 'message')) {
        if (promoteUserData.message === 'Token is missing') {
          logout();
        }
        if (promoteUserData.message === 'Token is invalid') {
          logout();
        }
        if (promoteUserData.message === 'Only admin can access this route') {
          logout();
        }
        if (promoteUserData.message === 'User does not exist') {
          document.getElementById('status-message').innerHTML = promoteUserData.message;
        }
        if (Object.prototype.hasOwnProperty.call(promoteUserData, 'isadmin')) {
          document.getElementById('isadmin').style.borderBottomColor = 'red';
          document.getElementById('status-message').innerHTML = '(Accepted values: True, False)';
        }
        if (promoteUserData.message === 'You cannot change the status of this user' || promoteUserData.message === 'You cannot change your own admin status') {
          document.getElementById('status-message').innerHTML = promoteUserData.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(promoteUserData, 'data')) {
        if (promoteUserData.data.message === 'User status has been updated') {
          document.getElementById('status-message').style.color = 'green';
          document.getElementById('status-message').innerHTML = promoteUserData.data.message;
          document.getElementById('status').value = status;
          document.getElementById('status-data').innerHTML = status.toLowerCase();
        }
      }
      document.getElementById('fa-spin-edit-status').style.display = 'none';
    })
    .catch(() => {
      document.getElementById('status-message').innerHTML = 'An error has occurred please try again';
      document.getElementById('fa-spin-edit-status').style.display = 'none';
    });
};

const changeActiveStatus = (event, usernameid) => {
  event.preventDefault();
  document.getElementById('fa-spin-activity').style.display = 'block';
  document.getElementById('activity-message').innerHTML = '';
  document.getElementById('activity-message').style.color = 'red';

  const isactive = document.getElementById('activity').value;
  const activeStatusUri = `${config.root}users/${usernameid}/activate`;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'x-access-token': user.token,
      'Content-Type': 'application/json; charset=utf-8',
    }),
    body: JSON.stringify({
      isactive,
    }),
  };
  const activeStatusRequest = new Request(activeStatusUri, options);

  fetch(activeStatusRequest)
    .then((activeStatusResponse) => {
      if (activeStatusResponse.ok) {
        return activeStatusResponse.json();
      }
      return activeStatusResponse.json();
    })
    .then((activeStatusData) => {
      if (Object.prototype.hasOwnProperty.call(activeStatusData, 'message')) {
        if (activeStatusData.message === 'Token is missing') {
          logout();
        }
        if (activeStatusData.message === 'Token is invalid') {
          logout();
        }
        if (activeStatusData.message === "You cannot change this user's active status") {
          document.getElementById('activity-message').innerHTML = activeStatusData.message;
        }
        if (activeStatusData.message === 'user does not exist') {
          document.getElementById('activity-message').innerHTML = activeStatusData.message;
        }
        if (Object.prototype.hasOwnProperty.call(activeStatusData, 'isactive')) {
          document.getElementById('activity-message').innerHTML = '(Accepted values: True, False)';
        }
        if (activeStatusData.message === 'You cannot change your own active status') {
          document.getElementById('activity-message').innerHTML = activeStatusData.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(activeStatusData, 'data')) {
        if (activeStatusData.data.message === 'User active status has been updated') {
          document.getElementById('activity-message').style.color = 'green';
          document.getElementById('activity-message').innerHTML = activeStatusData.data.message;
          document.getElementById('activity').value = isactive;
          document.getElementById('activity-data').innerHTML = isactive.toLowerCase();
        }
      }
      document.getElementById('fa-spin-activity').style.display = 'none';
    })
    .catch(() => {
      document.getElementById('activity-message').innerHTML = 'An error has occurred please try again';
      document.getElementById('fa-spin-activity').style.display = 'none';
    });
};

const deleteUserData = (event, usernameid) => {
  event.preventDefault();
  document.getElementById('fa-spin-data-delete').style.display = 'block';
  document.getElementById('error-message').innerHTML = '';

  const deleteUserUri = `${config.root}users/${usernameid}`;

  const options = {
    method: 'DELETE',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
  };
  const deleteRequest = new Request(deleteUserUri, options);

  fetch(deleteRequest)
    .then((deleteResponse) => {
      if (deleteResponse.ok) {
        return deleteResponse.json();
      }
      return deleteResponse.json();
    })
    .then((deleteData) => {
      if (Object.prototype.hasOwnProperty.call(deleteData, 'message')) {
        if (deleteData.message === 'Token is missing') {
          logout();
        }
        if (deleteData.message === 'Token is invalid') {
          logout();
        }
        if (deleteData.message === 'user does not exist') {
          document.getElementById('error-message').innerHTML = deleteData.message;
        }
        if (deleteData.message === 'You cannot delete this user') {
          document.getElementById('error-message').innerHTML = deleteData.message;
        }
        if (deleteData.message === 'A user who has posted incidents cannot be deleted') {
          document.getElementById('error-message').innerHTML = deleteData.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(deleteData, 'data')) {
        if (deleteData.data.message === 'user record has been deleted') {
          document.getElementById('error-message').innerHTML = deleteData.data.message;
          window.location.replace('admin.html');
        }
      }
      document.getElementById('fa-spin-data-delete').style.display = 'none';
    })
    .catch(() => {
      document.getElementById('error-message').innerHTML = 'An error has occurred please try again';
      document.getElementById('fa-spin-data-delete').style.display = 'none';
    });
};

const searchUsers = (event) => {
  event.preventDefault();
  showLoader();
  const searchParameter = document.getElementById('searchUsers').value;
  getUsers(searchParameter);
  hideLoader(1000);
};
