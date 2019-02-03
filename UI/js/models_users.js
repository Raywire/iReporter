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

        const Fn = function Pagination() {
          const prevButton = document.getElementById('button_prev');
          const nextButton = document.getElementById('button_next');
          const perPage = document.getElementById('perPage').value;
          const userNumber = document.getElementById('user_number');

          let currentPage = 1;
          let usersPerPage = parseInt(perPage, 10);
          let startNumber = 1;
          const totalNumber = users.length;

          if (usersPerPage > totalNumber) {
            usersPerPage = totalNumber;
          }
          let endNumber = usersPerPage;
          let virtualEndNumber = usersPerPage;

          const selectedPage = () => {
            const pageNumber = document.getElementById('pageNumber').getElementsByClassName('clickPageNumber');
            for (let i = 0; i < pageNumber.length; i += 1) {
              if (i === currentPage - 1) {
                pageNumber[i].style.opacity = '1.0';
              } else {
                pageNumber[i].style.opacity = '0.5';
              }
            }
          };

          const numPages = () => {
            const numOfPages = Math.ceil(users.length / usersPerPage);
            return numOfPages;
          };

          const checkButtonOpacity = () => {
            if (currentPage === 1) {
              prevButton.classList.add('opacity');
            } else {
              prevButton.classList.remove('opacity');
            }
            if (currentPage === numPages()) {
              nextButton.classList.add('opacity');
            } else {
              nextButton.classList.remove('opacity');
            }

            document.getElementById('button_next').disabled = currentPage === numPages();
            document.getElementById('button_prev').disabled = currentPage === 1;
          };

          const changePage = (page) => {
            const result = document.getElementById('user-data');
            let pageN = page;

            if (pageN < 1) {
              pageN = 1;
            }
            if (pageN > (numPages() - 1)) {
              pageN = numPages();
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
              document.getElementById('button_next').disabled = true;
              document.getElementById('button_prev').disabled = true;
              nextButton.classList.add('opacity');
              prevButton.classList.add('opacity');
              document.getElementById('user-data').innerHTML = resultNone;
              // return true;
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
              selectedPage();
            }
          };

          const prevPage = () => {
            showLoader();
            if (currentPage > 1) {
              currentPage -= 1;
              changePage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber -= usersPerPage;
              virtualEndNumber -= usersPerPage;
              endNumber -= usersPerPage;
              userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${virtualEndNumber}</span>  of ${totalNumber}`;
            }
            if (currentPage === 1) {
              endNumber = virtualEndNumber;
            }
            hideLoader(1000);
          };

          const nextPage = () => {
            showLoader();
            if (currentPage < numPages()) {
              currentPage += 1;
              changePage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber += usersPerPage;
              endNumber += usersPerPage;
              virtualEndNumber += usersPerPage;
              if (endNumber > totalNumber) {
                endNumber = totalNumber;
              }
              if (endNumber === startNumber) {
                userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
              } else {
                userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${endNumber}</span>  of ${totalNumber}`;
              }
            }
            hideLoader(1000);
          };

          const addEventListeners = () => {
            nextButton.addEventListener('click', nextPage);
            prevButton.addEventListener('click', prevPage);
          };

          const clickPage = () => {
            document.addEventListener('click', (e) => {
              if (e.target.nodeName === 'SPAN' && e.target.classList.contains('clickPageNumber')) {
                currentPage = e.target.textContent;
                changePage(currentPage);
              }
            });
          };

          const pageNumbers = () => {
            const pageNumber = document.getElementById('pageNumber');
            pageNumber.innerHTML = '';
            let numberOfPages = numPages();
            if (currentPage === 0) {
              currentPage = 1;
              numberOfPages = 1;
            }

            pageNumber.innerHTML = `<span class=''><span id='currentPage'>${currentPage}</span> / ${numberOfPages}</span>`;
          };

          this.init = () => {
            changePage(1);
            pageNumbers();
            selectedPage();
            clickPage();
            addEventListeners();
          };

          if (startNumber === endNumber || endNumber === 0) {
            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
          } else {
            userNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${endNumber}</span>  of ${totalNumber}`;
          }
        };

        const pagination = new Fn();
        pagination.init();
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
  const request = new Request(promoteUserUri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === 'Only admin can access this route') {
          logout();
        }
        if (j.message === 'User does not exist') {
          document.getElementById('status-message').innerHTML = j.message;
        }
        if (Object.prototype.hasOwnProperty.call(j, 'isadmin')) {
          document.getElementById('isadmin').style.borderBottomColor = 'red';
          document.getElementById('status-message').innerHTML = '(Accepted values: True, False)';
        }
        if (j.message === 'You cannot change the status of this user' || j.message === 'You cannot change your own admin status') {
          document.getElementById('status-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data.message === 'User status has been updated') {
          document.getElementById('status-message').style.color = 'green';
          document.getElementById('status-message').innerHTML = j.data.message;
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

  const activeStatusUri = `${config.root}users/${usernameid}/activate`;

  const activity = document.getElementById('activity').value;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
    body: JSON.stringify({
      isactive: activity,
    }),
  };
  const request = new Request(activeStatusUri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === "You cannot change this user's active status") {
          document.getElementById('activity-message').innerHTML = j.message;
        }
        if (j.message === 'user does not exist') {
          document.getElementById('activity-message').innerHTML = j.message;
        }
        if (Object.prototype.hasOwnProperty.call(j, 'isactive')) {
          document.getElementById('activity-message').innerHTML = '(Accepted values: True, False)';
        }
        if (j.message === 'You cannot change your own active status') {
          document.getElementById('activity-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data.message === 'User active status has been updated') {
          document.getElementById('activity-message').style.color = 'green';
          document.getElementById('activity-message').innerHTML = j.data.message;
          document.getElementById('activity').value = activity;
          document.getElementById('activity-data').innerHTML = activity.toLowerCase();
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
  const request = new Request(deleteUserUri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === 'user does not exist') {
          document.getElementById('error-message').innerHTML = j.message;
        }
        if (j.message === 'You cannot delete this user') {
          document.getElementById('error-message').innerHTML = j.message;
        }
        if (j.message === 'A user who has posted incidents cannot be deleted') {
          document.getElementById('error-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data.message === 'user record has been deleted') {
          document.getElementById('error-message').innerHTML = j.data.message;
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
