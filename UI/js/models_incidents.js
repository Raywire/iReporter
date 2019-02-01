const tokenModels = user.token;
const profileUserName = user.username;

const convertToLocalTime = (utcdatetime) => {
  let localDateTime = new Date(utcdatetime).toISOString();

  localDateTime = moment(localDateTime).format('ddd, MMM Do YYYY, h:mm:ss a Z'); // Fri, Jan 4th 2019, 7:18:05 pm +3:00;
  return localDateTime;
};

const humanize = (utcdatetime) => {
  const datetimeiso = new Date(utcdatetime).toISOString();
  const humanizedDate = moment(datetimeiso).fromNow();
  return humanizedDate;
};

// Function to post an incident by type

const postData = (event, incidenttype) => {
  event.preventDefault();
  document.getElementById('title').style.borderBottomColor = '#ccc';
  document.getElementById('comment').style.borderBottomColor = '#ccc';
  document.getElementById('location').style.borderBottomColor = '#ccc';
  document.getElementById('fa-spin').style.display = 'block';

  const uri = config.root + incidenttype;

  const title = document.getElementById('title').value;
  const comment = document.getElementById('comment').value;
  const location = document.getElementById('location').value;

  const options = {
    method: 'POST',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
    body: JSON.stringify({
      title,
      comment,
      location,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        document.getElementById('fa-spin').style.display = 'none';

        return response.json();
      }
      document.getElementById('fa-spin').style.display = 'none';
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
        if (Object.prototype.hasOwnProperty.call(j.message, 'comment')) {
          document.getElementById('comment').style.borderBottomColor = 'red';
          warningNotification({
            title: 'Warning',
            message: 'Comment cannot be empty or start with special characters',
          });
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'title')) {
          document.getElementById('title').style.borderBottomColor = 'red';
          warningNotification({
            title: 'Warning',
            message: 'Title cannot be empty or start with special characters',
          });
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'location')) {
          document.getElementById('location').style.borderBottomColor = 'red';
          warningNotification({
            title: 'Warning',
            message: 'Location cannot be empty',
          });
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        successNotification({
          title: 'Success',
          message: 'Incident has been created',
        });

        if (incidenttype === 'interventions') {
          getData('intervention', 'all', 'all');
        } else if (incidenttype === 'redflags') {
          getData('redflag', 'all', 'all');
        }
        document.getElementById('postData').reset();
        document.getElementById('modal-window-create').style.display = 'none';
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// Function to get all incidents by type, createdBy and search parameter

let getData = (incidenttype, incidentcreator, searchdata) => {
  const uri = `${config.root}${incidenttype}s`;

  const options = {
    method: 'GET',
    mode: 'cors',
    cache: 'default',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        try {
          document.getElementById('fa-spin-data').style.display = 'none';
          showLoader();
        } catch (error) {
          console.log(error);
        }

        return response.json();
      }
      try {
        document.getElementById('fa-spin-data').style.display = 'none';
      } catch (error) {
        console.log(error);
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
        if (j.message === 'No interventions' || j.message === 'No redflags') {
          let result = '';
          result += `
                  <div class='column-100'>
                    <div class='card'>
                      <div class='container'>
                          <p><i class='fa fa-flag fa-3x' aria-hidden='true'></i></p>
                          <h4 class='theme-blue'><b>No Incidents</b></h4> 
                      </div>
                    </div>               
                  </div> 
                  `;
          document.getElementById('incident-data').innerHTML = result;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        let creator = '';
        let usernameIncidents = [];
        let searchedIncidents = [];
        const incidents = j.data;

        if (searchdata === 'all' || searchdata === '') {
          usernameIncidents = incidents;
          searchedIncidents = incidents;
        } else {
          usernameIncidents = searchedIncidents = incidents.filter((incident) => {
            return incident.title.toLowerCase() === searchdata.toLowerCase() || incident.id === parseInt(searchdata) || incident.username === searchdata.toLowerCase() || incident.status === searchdata.toLowerCase();
          });
        }

        if (incidentcreator !== 'all') {
          usernameIncidents = searchedIncidents.filter((incident) => {
            const filteredIncidents = incident.username === incidentcreator;
            if (filteredIncidents) {
              return filteredIncidents;
            }
            let result = '';
            result += `
                      <div class='column-100'>
                        <div class='card'>
                          <div class='container'>
                              <p><i class='fa fa-star-half-o fa-3x' aria-hidden='true'></i></p>
                              <h4 class='theme-blue'><b>No incidents found</b></h4>
                          </div>
                        </div>               
                      </div>               
                        </div>               
                      </div> 
                        </div>
                      </div> 
                  </div> 
                      </div>               
                  </div> 
                      </div> 
                  </div> 
                      </div> 
                    `;
            document.getElementById('incident-data').innerHTML = result;
          });
        }

        const Fn = function Pagination() {
          const prevButton = document.getElementById('button_prev');
          const nextButton = document.getElementById('button_next');
          const perPage = document.getElementById('perPage').value;

          let currentPage = 1;
          let recordsPerPage = parseInt(perPage, 10);
          let startNumber = 1;
          const totalNumber = usernameIncidents.length;

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
          };

          let addEventListeners = () => {
            nextButton.addEventListener('click', nextPage);
            prevButton.addEventListener('click', prevPage);
          };

          let selectedPage = () => {
            const pageNumber = document.getElementById('pageNumber').getElementsByClassName('clickPageNumber');
            for (let i = 0; i < pageNumber.length; i += 1) {
              if (i === currentPage - 1) {
                pageNumber[i].style.opacity = '1.0';
              } else {
                pageNumber[i].style.opacity = '0.5';
              }
            }
          };

          const checkButtonOpacity = () => {
            currentPage === 1 ? prevButton.classList.add('opacity') : prevButton.classList.remove('opacity');
            currentPage === numPages() ? nextButton.classList.add('opacity') : nextButton.classList.remove('opacity');
            document.getElementById('button_next').disabled = currentPage === numPages() ? true : false;
            document.getElementById('button_prev').disabled = currentPage === 1 ? true : false; 
              document.getElementById('button_prev').disabled = currentPage === 1 ? true : false; 
            document.getElementById('button_prev').disabled = currentPage === 1 ? true : false; 
              document.getElementById('button_prev').disabled = currentPage === 1 ? true : false; 
            document.getElementById('button_prev').disabled = currentPage === 1 ? true : false; 
          };

          let changePage = (page) => {
            const result = document.getElementById('incident-data');

            if (page < 1) {
              page = 1;
            }
            if (page > (numPages() - 1)) {
              page = numPages();
            }

            result.innerHTML = '';

            if (usernameIncidents.length === 0) {
              let result = '';
              result += `
                        <div class='column-100'>
                        <div class='card'>
                            <div class='container'>
                              
                                <p><i class='fa fa-star-half-o fa-3x' aria-hidden='true'></i></p>
                                <h4 class='theme-blue'><b>No incidents found</b></h4>
                              
                            </div>
                          </div>               
                            </div>               
                              </div>
                            </div>               
                          </div>               
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
              return document.getElementById('incident-data').innerHTML = result;
            }

            for (let i = (page - 1) * recordsPerPage; i < (page * recordsPerPage) && i < usernameIncidents.length; i++) {
              const humanizedTime = humanize(usernameIncidents[i].createdon);
              let link = '';
              let icon = '';

              if (usernameIncidents[i].username === profileUserName) {
                creator = 'Me';
              } else {
                creator = usernameIncidents[i].username;
              }
              if (usernameIncidents[i].type === 'redflag') {
                link = 'view_redflag.html?redflag_id';
                icon = 'fa fa-flag red';
              } else if (usernameIncidents[i].type === 'intervention') {
                link = 'view_intervention.html?intervention_id';
                icon = 'fa fa-handshake-o theme-blue';
              }

              result.innerHTML += `
                            <div class='column'>
                              <div class='card'>
                                  <div class='container2 justify'>
                                    <a href='${link}=${usernameIncidents[i].id}'>
                                      <p><i class='${icon} fa-2x' aria-hidden='true'></i></p>
                                      <h4 class='black truncate'><b>${usernameIncidents[i].title}</b></h4>
                                      <p>${usernameIncidents[i].status}</p>
                                      <p class='italic font-small'>${humanizedTime}</p>
                                    </a>          
                                      </a>          
                                    </a>          
                                      </a>          
                                    </a>          
                                    <a href='view_by_username.html?type=${usernameIncidents[i].type}&username=${usernameIncidents[i].username}'><p class='italic font-small'><span class='theme-blue'>By ${creator}</span></p>
                                    <p class='black align-right'><i class='fa fa-external-link theme-blue' aria-hidden='true'></i></p>
                                    </a>
                                  </div>
                                </div>               
                                  </div>               
                                </div>               
                                  </div>               
                              </div>
                                  </div>               
                                </div>               
                            </div>
                        `;
            }
            checkButtonOpacity();
            selectedPage();
          };

          let prevPage = () => {
            showLoader();
            if (currentPage > 1) {
              currentPage -= 1;
              changePage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber -= recordsPerPage;
              virtualEndNumber -= recordsPerPage;
              endNumber -= recordsPerPage;
              incidentNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${virtualEndNumber}</span>  of ${totalNumber}`;
            }
            if (currentPage === 1) {
              endNumber = virtualEndNumber;
            }
            hideLoader(1000);
          };

          let nextPage = () => {
            showLoader();
            if (currentPage < numPages()) {
              currentPage += 1;
              changePage(currentPage);
              document.getElementById('currentPage').innerHTML = currentPage;
              startNumber += recordsPerPage;
              endNumber += recordsPerPage;
              virtualEndNumber += recordsPerPage;
              if (endNumber > totalNumber) {
                endNumber = totalNumber;
              }
              if (endNumber === startNumber) {
                incidentNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
              } else {
                document.getElementById('startNumber').innerHTML = startNumber;
                document.getElementById('endNumber').innerHTML = endNumber;
              }
            }
            hideLoader(1000);
          };

          let clickPage = () => {
            document.addEventListener('click', function (e) {
              if (e.target.nodeName === 'SPAN' && e.target.classList.contains('clickPageNumber')) {
                currentPage = e.target.textContent;
                changePage(currentPage);
              }
            });
          };

          let pageNumbers = () => {
            const pageNumber = document.getElementById('pageNumber');
            pageNumber.innerHTML = '';
            let numberOfPages = numPages();
            if (currentPage === 0) {
              currentPage = 1;
              numberOfPages = 1;
            }

            pageNumber.innerHTML = `<span class=''><span id='currentPage'>${currentPage}</span> / ${numberOfPages}</span>`;
          };

          let numPages = () => {
            return Math.ceil(usernameIncidents.length / recordsPerPage);
          };

          let incidentNumber = document.getElementById('incident_number');

          if (startNumber === endNumber || endNumber === 0) {
            incidentNumber.innerHTML = `<span id='startNumber'>${startNumber}</span> of ${totalNumber}`;
          } else {
            incidentNumber.innerHTML = `<span id='startNumber'>${startNumber}</span><span id='dash'>-</span><span id='endNumber'>${endNumber}</span>  of ${totalNumber}`;
          }
        };
        const pagination = new Fn();
        pagination.init();

        hideLoader(1000);
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// Function to get an incident by Id

const getDataById = (incidenttype, incidentId) => {
  const uri = `${config.root}${incidenttype}/${incidentId}`;

  const options = {
    method: 'GET',
    mode: 'cors',
    cache: 'default',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        document.getElementById('fa-spin-data').style.display = 'none';
        document.getElementById('btnGeolocate').disabled = false;
        return response.json();
      }
      document.getElementById('fa-spin-data').style.display = 'none';
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
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          document.getElementById('message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        let result = '';
        let imageUrl = '';
        let creator = '';
        j.data.map((incident) => {
          const {
            title,
            comment,
            status,
            createdon,
            location,
            username,
            images,
            videos,
            type,
          } = incident;
          const localDateTime = convertToLocalTime(createdon);

          if (username === profileUserName) {
            creator = 'Me';
            const ownerButtons = document.querySelectorAll('.btnOwner');
            for (let i = 0; i < ownerButtons.length; i += 1) {
              ownerButtons[i].style.display = 'inline';
            }
          } else {
            creator = username;
            document.getElementById('btnGeolocate').style.display = 'inline';
            try {
              document.getElementById('btnEditStatus').style.display = 'inline';
            } catch (error) {}
          }
          if (images === null || images === undefined) {
            imageUrl = 'img/loading.jpg';
          } else {
            imageUrl = 'img/loading.jpg';
            getFileData('images', images);
          }
          if (videos != null) {
            getFileData('videos', videos);
          }
          const paragraph = comment.split('\n');
          let commentData = '';

          for (let i = 0; i < paragraph.length; i += 1) {
            commentData += `
            <p class='comment-data-item'>${paragraph[i]}</p>
            `;
          }
          result += `
                <div class='incident-header'>
                  <h2>${title}</h2>
                  <h3><span class='black'>Status:</span> <span id='status-data' class='italic'>${status}</span></h3>
                  <h4><span class='black'>Created On:</span> <span class='italic'>${localDateTime}</span></h4>
                  <h4><span class='black'>By:</span> <a href='view_by_username.html?type=${type}&username=${username}'><span class='theme-blue'>${creator}</span></a></h4>
                  <hr class='incident-line'>
                </div>
                <div class='row  bg-color'>
                  <div class='column-50 bg-color'>
                    <p class='img-details'><img id='main-image' src='${imageUrl}' alt='Image for ${title}'></p>
                    <p class='vid-details'></p>
                  </div>
                  <div class='column-50' id='comment-data'  bg-color align-justify'>
                   ${commentData}
                  </div>
                </div>  
                `;
          localStorage.setItem('coordinates', location);
          document.getElementById('incident-data').innerHTML = result;
          document.getElementById('title').value = title;
          document.getElementById('comment').value = comment;
          document.getElementById('location').value = location;
        });
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// Function to delete an incident  by id

const deleteData = (incidenttype, incidentId) => {
  document.getElementById('fa-spin-data-delete').style.display = 'block';
  document.getElementById('error-message').innerHTML = '';

  const uri = `${config.root}${incidenttype}/${incidentId}`;

  const options = {
    method: 'DELETE',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
  };
  const request = new Request(uri, options);

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
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          document.getElementById('error-message').innerHTML = j.message;
        }
        if (j.message === 'Only the creator of this record can delete it') {
          document.getElementById('error-message').innerHTML = j.message;
        }
        if (j.message === 'Incident can only be deleted when the status is draft') {
          document.getElementById('error-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data.message === 'Intervention record has been deleted' || j.data.message === 'Redflag record has been deleted') {
          document.getElementById('error-message').innerHTML = j.data.message;
          if (incidenttype === 'redflags') {
            window.location.replace('redflags.html');
          } else if (incidenttype === 'interventions') {
            window.location.replace('interventions.html');
          }
        }
      }
      document.getElementById('fa-spin-data-delete').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('fa-spin-data-delete').style.display = 'none';
    });
};

// Function to get files by file name
let getFileData = (filetype, filename) => {

  const uri = `${config.root}uploads/${filetype}/${filename}`;

  const options = {
    method: 'GET',
    mode: 'cors',
    headers: new Headers({
      'x-access-token': tokenModels,
    }),
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      if (filetype === 'images') {
        const imgElem = document.getElementById('main-image');
        const imgUrl = j;
        imgElem.src = imgUrl;
      }
      if (filetype === 'videos') {
        const videoUrl = j;
        const videoElement = document.createElement('video');
        if (videoElement.canPlayType('video/mp4')) {
          videoElement.setAttribute('src', videoUrl);
        } else {
          videoElement.setAttribute('src', videoUrl);
        }
        videoElement.setAttribute('controls', 'controls');
        videoElement.setAttribute('class', 'main-video');
        document.getElementsByClassName('vid-details')[0].appendChild(videoElement);
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// Function to edit the location
const editLocation = (event, incidentType, incidentId) => {
  event.preventDefault();
  document.getElementById('fa-spin-edit').style.display = 'block';

  const uri = `${config.root}${incidentType}/${incidentId}/location`;

  const location = document.getElementById('location').value;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
    body: JSON.stringify({
      location,
    }),
  };
  const request = new Request(uri, options);

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
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (j.message === 'Only the user who created this record can edit it') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (j.message === 'Incident can only be edited when the status is draft') {
          warningNotification({
            title: 'Warning',
            message: 'Location can only be edited when the status is draft',
          });
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data[0].message === "Updated intervention record's location" || j.data[0].message === "Updated redflag record's location") {
          successNotification({
            title: 'Success',
            message: j.data[0].message,
          });
          localStorage.setItem('coordinates', location);
        }
      }
      document.getElementById('fa-spin-edit').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('fa-spin-edit').style.display = 'none';
    });
};

// Function to edit comment
const editComment = (event, incidentType, incidentId) => {
  event.preventDefault();
  document.getElementById('fa-spin-edit').style.display = 'block';
  document.getElementById('comment').style.borderBottomColor = '#ccc';

  const uri = `${config.root}${incidentType}/${incidentId}/comment`;

  const comment = document.getElementById('comment').value;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
    body: JSON.stringify({
      comment,
    }),
  };
  const request = new Request(uri, options);

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
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'comment')) {
          document.getElementById('comment').style.borderBottomColor = 'red';
          warningNotification({
            title: 'Warning',
            message: 'Comment cannot be empty or start with special characters and whitespace',
          });
        }
        if (j.message === 'Only the user who created this record can edit it') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (j.message === 'Incident can only be edited when the status is draft') {
          warningNotification({
            title: 'Warning',
            message: 'Comment can only be edited when the status is draft',
          });
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data[0].message === "Updated intervention record's comment" || j.data[0].message === "Updated redflag record's comment") {
          successNotification({
            title: 'Success',
            message: j.data[0].message,
          });
          const paragraph = comment.split('\n');
          let commentData = '';

          for (let i = 0; i < paragraph.length; i += 1) {
            commentData += `
            <p class='comment-data-item'>${paragraph[i]}</p>
            `;
          }
          document.getElementById('comment-data').innerHTML = commentData;
        }
      }
      document.getElementById('fa-spin-edit').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('fa-spin-edit').style.display = 'none';
    });
};

// Function to edit status
const editStatus = (event, incidentType, incidentId) => {
  event.preventDefault();
  document.getElementById('fa-spin-edit-status').style.display = 'block';

  const uri = `${config.root}${incidentType}/${incidentId}/status`;

  const status = document.getElementById('status').value;

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
    body: JSON.stringify({
      status,
    }),
  };
  const request = new Request(uri, options);

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
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'status')) {
          document.getElementById('status').style.borderBottomColor = 'red';
          warningNotification({
            title: 'Warning',
            message: 'Accepted values: draft, under investigation, rejected, resolved',
          });
        }
        if (j.message === 'Only an admin can change the status of the record') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
      }

      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data[0].message === "Updated intervention record's status" || j.data[0].message === "Updated redflag record's status") {
          successNotification({
            title: 'Success',
            message: j.data[0].message,
          });
          document.getElementById('status').value = status;
          document.getElementById('status-data').innerHTML = status;
        }
      }
      document.getElementById('fa-spin-edit-status').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('fa-spin-edit-status').style.display = 'none';
    });
};

// Function to upload image
const uploadImage = (event, incidentType, incidentId) => {
  event.preventDefault();
  document.getElementById('fa-spin-upload').style.display = 'block';
  document.getElementById('upload-message').innerHTML = '';
  document.getElementById('upload-message').style.color = 'red';

  const uri = `${config.root}${incidentType}/${incidentId}/addImage`;

  let formData = new FormData();
  const fileData = document.getElementById('fileImage').files[0];

  if (fileData === null || fileData === undefined) {
    document.getElementById('fa-spin-upload').style.display = 'none';
    document.getElementById('upload-message').innerHTML = 'Please select a file';
    return false;
  }

  console.log(fileData);
  console.log(fileData.name);
  const fileExtension = fileData.name.split('.')[1];
  const uploadedFileName = `${incidentId.toString()}.${fileExtension}`;
  console.log(uploadedFileName);

  formData.append('uploadFile', fileData, fileData.name);

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'x-access-token': tokenModels,
    }),
    body: formData,
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      console.log(j);
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
        if (j.message === 'You cannot upload a photo for this incident') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
        if (j.message === 'File type not supported' || j.message === 'No uploadFile name in form') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data[0].message === 'Image added to intervention record' || j.data[0].message === 'Image added to red-flag record') {
          document.getElementById('upload-message').style.color = 'green';
          document.getElementById('upload-message').innerHTML = j.data[0].message;
          getFileData('images', uploadedFileName);
        }
      }
      document.getElementById('fa-spin-upload').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('upload-message').innerHTML = 'An error occured check if status is draft and try again';
      document.getElementById('fa-spin-upload').style.display = 'none';
    });
};

const uploadVideo = (event, incidentType, incidentId) => {
  event.preventDefault();
  document.getElementById('fa-spin-upload-2').style.display = 'block';
  document.getElementById('upload-message-2').innerHTML = '';
  document.getElementById('upload-message-2').style.color = 'red';

  const uri = `${config.root}${incidentType}/${incidentId}/addVideo`;

  let formData = new FormData();
  const fileData = document.getElementById('fileVideo').files[0];

  if (fileData === null || fileData === undefined) {
    document.getElementById('fa-spin-upload-2').style.display = 'none';
    document.getElementById('upload-message-2').innerHTML = 'Please select a file';
    return false;
  }

  console.log(fileData);
  console.log(fileData.name);
  const fileExtension = fileData.name.split('.')[1];
  const uploadedFileName = `${incidentId.toString()}.${fileExtension}`;
  console.log(uploadedFileName);

  formData.append('uploadFile', fileData, fileData.name);

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'x-access-token': tokenModels,
    }),
    body: formData,
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      console.log(j);
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === 'Intervention does not exist' || j.message === 'Redflag does not exist') {
          document.getElementById('upload-message-2').innerHTML = j.message;
        }
        if (j.message === 'You cannot upload a video for this incident') {
          document.getElementById('upload-message-2').innerHTML = j.message;
        }
        if (j.message === 'File type not supported' || j.message === 'No uploadFile name in form') {
          document.getElementById('upload-message-2').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data[0].message === 'Video added to intervention record' || j.data[0].message === 'Video added to red-flag record') {
          document.getElementById('upload-message-2').style.color = 'green';
          document.getElementById('upload-message-2').innerHTML = j.data[0].message;
          document.getElementById('uploadVideo').reset();
          getFileData('videos', uploadedFileName);
        }
      }
      document.getElementById('fa-spin-upload-2').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('upload-message-2').innerHTML = 'An error occured check if status is draft and try again';
      document.getElementById('fa-spin-upload-2').style.display = 'none';
    });
};

const loadProfileData = () => {
  const profilePhoneNumber = localStorage.getItem('profilePhoneNumber');
  const firstname = localStorage.getItem('profileFirstName');
  const lastname = localStorage.getItem('profileLastName');
  const othername = localStorage.getItem('profileOtherName');
  const profileEmail = localStorage.getItem('profileEmail');
  const emailVerified = localStorage.getItem('profileEmailVerified');
  const profilePhotoUrl = localStorage.getItem('profilePhotoUrl');

  const profileName = `${firstname} ${lastname} ${othername}`;

  document.getElementById('name').innerHTML = profileName;
  document.getElementById('email').innerHTML = profileEmail;
  document.getElementById('verified').innerHTML = emailVerified;
  document.getElementById('username').innerHTML = user.username;

  if (profilePhotoUrl === 'null' || profilePhotoUrl === '') {
    document.getElementById('profilePhoto').src = 'img/img_avatar3.jpeg';
  } else {
    document.getElementById('profilePhoto').src = profilePhotoUrl;
  }

  document.getElementById('firstnameProfile').value = firstname;
  document.getElementById('lastnameProfile').value = lastname;
  document.getElementById('othernameProfile').value = othername;
  document.getElementById('emailProfile').value = profileEmail;
  document.getElementById('phonenumberProfile').value = profilePhoneNumber;
};

const updateUserData = (event, usernameid) => {
  event.preventDefault();
  document.getElementById('fa-spin-updateProfile').style.display = 'block';
  document.getElementById('firstnameProfile').style.borderColor = '#ccc';
  document.getElementById('lastnameProfile').style.borderColor = '#ccc';
  document.getElementById('othernameProfile').style.borderColor = '#ccc';
  document.getElementById('phonenumberProfile').style.borderColor = '#ccc';
  document.getElementById('emailProfile').style.borderColor = '#ccc';

  const uri = `${config.root}users/${usernameid}`;

  const firstname = document.getElementById('firstnameProfile').value;
  const lastname = document.getElementById('lastnameProfile').value;
  const othernames = document.getElementById('othernameProfile').value;
  const phonenumber = document.getElementById('phonenumberProfile').value;
  const email = document.getElementById('emailProfile').value;

  const data = {
    firstname,
    lastname,
    email,
  };

  if (othernames !== '') {
    data.othernames = othernames;
  }
  if (phonenumber !== '') {
    data.phoneNumber = phonenumber;
  }

  const options = {
    method: 'PUT',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': tokenModels,
    }),
    body: JSON.stringify(data),
  };
  const request = new Request(uri, options);

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
        if (j.message === 'User does not exist') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'firstname')) {
          document.getElementById('firstnameProfile').style.borderColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'lastname')) {
          document.getElementById('lastnameProfile').style.borderColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'othernames')) {
          document.getElementById('othernameProfile').style.borderColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'email')) {
          document.getElementById('emailProfile').style.borderColor = 'red';
        }
        if (Object.prototype.hasOwnProperty.call(j.message, 'phoneNumber')) {
          document.getElementById('phonenumberProfile').style.borderColor = 'red';
        }
        if (j.message === 'email already exists') {
          warningNotification({
            title: 'Warning',
            message: j.message,
          });
        }

        if (j.message === 'Your profile has been updated') {
          localStorage.setItem('profilePhoneNumber', phonenumber);
          localStorage.setItem('profileFirstName', firstname);
          localStorage.setItem('profileLastName', lastname);
          localStorage.setItem('profileOtherName', othernames);
          localStorage.setItem('profileEmail', email);
          loadProfileData();
          successNotification({
            title: 'Success',
            message: `${j.message} for ${usernameid}`,
          });
        }
      }

      document.getElementById('fa-spin-updateProfile').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('fa-spin-updateProfile').style.display = 'none';
    });
};

const uploadProfilePic = (event, usernameid) => {
  event.preventDefault();
  document.getElementById('fa-spin-upload-pic').style.display = 'block';
  document.getElementById('upload-message').innerHTML = '';
  document.getElementById('upload-message').style.color = 'red';

  const uri = `${config.root}users/${usernameid}/uploadImage`;

  let formData = new FormData();
  const fileData = document.getElementById('profilePic').files[0];

  if (fileData === null || fileData === undefined) {
    document.getElementById('fa-spin-upload-pic').style.display = 'none';
    document.getElementById('upload-message').innerHTML = 'Please select a file';
    return false;
  }

  console.log(fileData);
  console.log(fileData.name);
  const fileExtension = fileData.name.split('.')[1];
  const uploadedFileName = `${usernameid}.${fileExtension}`;
  console.log(uploadedFileName);

  formData.append('file', fileData, fileData.name);

  const options = {
    method: 'PATCH',
    mode: 'cors',
    headers: new Headers({
      'x-access-token': tokenModels,
    }),
    body: formData,
  };
  const request = new Request(uri, options);

  fetch(request)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return response.json();
    })
    .then((j) => {
      console.log(j);
      if (Object.prototype.hasOwnProperty.call(j, 'message')) {
        if (j.message === 'Token is missing') {
          logout();
        }
        if (j.message === 'Token is invalid') {
          logout();
        }
        if (j.message === 'user does not exist') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
        if (j.message === 'A user can only upload a picture to their own profile') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
        if (j.message === 'File type not supported' || j.message === 'no file part') {
          document.getElementById('upload-message').innerHTML = j.message;
        }
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        if (j.data.message === 'Your profile picture has been uploaded') {
          document.getElementById('upload-message').style.color = 'green';
          document.getElementById('upload-message').innerHTML = j.data.message;
        }
      }
      document.getElementById('fa-spin-upload-pic').style.display = 'none';
    })
    .catch((error) => {
      console.log(error);
      document.getElementById('upload-message').innerHTML = 'An error occured try again';
      document.getElementById('fa-spin-upload-pic').style.display = 'none';
    });
};

const getIncidentNumber = (incidenttype) => {
  const uri = config.root + incidenttype;

  const options = {
    method: 'GET',
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json; charset=utf-8',
      'x-access-token': user.token,
    }),
  };
  const request = new Request(uri, options);

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
      }
      if (Object.prototype.hasOwnProperty.call(j, 'data')) {
        const incidents = j.data;
        const myIncidents = incidents.filter((incident) => {
          return incident.username === profileUserName;
        });

        const myRedflags = myIncidents.filter((incident) => {
          return incident.type === 'redflag';
        });
        const myInterventions = myIncidents.filter((incident) => {
          return incident.type === 'intervention';
        });
        const myDraftIncidents = myIncidents.filter((incident) => {
          return incident.status === 'draft';
        });
        const myResolvedIncidents = myIncidents.filter((incident) => {
          return incident.status === 'resolved';
        });
        const myUnderInvestigationIncidents = myIncidents.filter((incident) => {
          return incident.status === 'under investigation';
        });
        const myRejectedIncidents = myIncidents.filter((incident) => {
          return incident.status === 'rejected';
        });

        if (incidenttype === 'redflags') {
          document.getElementById('my-redflags').innerHTML = `<a href='view_by_username.html?type=redflag&username=${profileUserName}'>${myRedflags.length}</a>`;
          document.getElementById('my-draft-redflags').innerHTML = myDraftIncidents.length;
          document.getElementById('my-resolved-redflags').innerHTML = myResolvedIncidents.length;
          document.getElementById('my-underinvestigation-redflags').innerHTML = myUnderInvestigationIncidents.length;
          document.getElementById('my-rejected-redflags').innerHTML = myRejectedIncidents.length;
        } else if (incidenttype === 'interventions') {
          document.getElementById('my-interventions').innerHTML = `<a href='view_by_username.html?type=intervention&username=${profileUserName}'>${myInterventions.length}</a>`;
          document.getElementById('my-draft-interventions').innerHTML = myDraftIncidents.length;
          document.getElementById('my-resolved-interventions').innerHTML = myResolvedIncidents.length;
          document.getElementById('my-underinvestigation-interventions').innerHTML = myUnderInvestigationIncidents.length;
          document.getElementById('my-rejected-interventions').innerHTML = myRejectedIncidents.length;
        }
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

const perPageSelection = (incidenttype, incidentcreator) => {
  showLoader();
  getData(incidenttype, incidentcreator, 'all');
  document.getElementById('searchIncidentsForm').reset();
  hideLoader(1000);
};

const searchIncidents = (event, incidenttype, incidentcreator) => {
  event.preventDefault();
  showLoader();
  const searchParameter = document.getElementById('searchIncidents').value;

  getData(incidenttype, incidentcreator, searchParameter);
  hideLoader(3000);
};
