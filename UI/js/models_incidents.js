let tokenModels = token;

let profileUserName = username;

function convertToLocalTime(utcdatetime){
  let localDateTime = new Date(utcdatetime).toISOString();

  localDateTime = moment(localDateTime).format('ddd, MMM Do YYYY, h:mm:ss a Z'); //Fri, Jan 4th 2019, 7:18:05 pm +3:00;
  return localDateTime;
}
function humanize(utcdatetime){
  let datetimeiso = new Date(utcdatetime).toISOString();
  let humanizedDate = moment(datetimeiso).fromNow();
  return humanizedDate;  
}

function postData(event, incident_type){
  event.preventDefault();   
  document.getElementById('title').style.borderBottomColor = "#ccc";
  document.getElementById('comment').style.borderBottomColor = "#ccc";
  document.getElementById('location').style.borderBottomColor = "#ccc";
  document.getElementById('fa-spin').style.display = "block";

  let uri = root + incident_type;             

  let title = document.getElementById('title').value;
  let comment = document.getElementById('comment').value;
  let location = document.getElementById('location').value;

  let options = {
      method: 'POST',
      mode: "cors",
      headers: new Headers({
        "Content-Type": "application/json; charset=utf-8",
        "x-access-token": tokenModels
      }),
      body: JSON.stringify({title:title,comment:comment,location:location})
  }
  let req = new Request(uri, options);

  fetch(req)
      .then((response)=>{
          if(response.ok){
            document.getElementById('fa-spin').style.display = "none";

            return response.json();
          }else{
            document.getElementById('fa-spin').style.display = "none";
            return response.json();
          }
      })
      .then( (j) =>{
        if(j.hasOwnProperty('message')){
          if(j['message'] == 'Token is missing'){
            logout();
          }
          if(j['message'] == 'Token is invalid'){
            logout();
          }
          if(j['message'].hasOwnProperty('comment')){
            document.getElementById('comment').style.borderBottomColor = "red";
            warningNotification({ 
              title: 'Warning',
              message: 'Comment cannot be empty or start with special characters', 
            });
          }
          if(j['message'].hasOwnProperty('title')){
            document.getElementById('title').style.borderBottomColor = "red";
            warningNotification({ 
              title: 'Warning',
              message: 'Title cannot be empty or start with special characters', 
            });
          }
          if(j['message'].hasOwnProperty('location')){
            document.getElementById('location').style.borderBottomColor = "red";
            warningNotification({ 
              title: 'Warning',
              message: 'Location cannot be empty', 
            });
          }                           
        }
        if(j.hasOwnProperty('data')){
          successNotification({ 
              title: 'Success',
              message: 'Incident has been created', 
            });
          
          // window.location.reload(true);
        }
                                    
      })
      .catch( (err) =>{
          console.log(err);                         
      });
}

function getData(incident_type, incident_creator){
                      
    let uri = root + incident_type + 's';

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": tokenModels
        })
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              document.getElementById('fa-spin-data').style.display = "none";
              return response.json();
            }else{
              document.getElementById('fa-spin-data').style.display = "none";
              return response.json();
            }
        })
        .then( (j) =>{
          
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'No interventions' || j['message'] == 'No redflags'){
                let result = '';
                result += `
                  <div class="column-100">
                  <div class="card">
                      <div class="container">
                        
                          <p><i class="fa fa-flag fa-3x" aria-hidden="true"></i></p>
                          <h4 class="theme-blue"><b>No Incidents</b></h4>
                        
                      </div>
                    </div>               
                </div> 
                  `;
                  document.getElementById('incident-data').innerHTML = result;
              }
          }
          if(j.hasOwnProperty('data')){
            let result = '';
            let link = '';
            let creator = '';
            let usernameIncidents = [];
            let incidents = j['data'];
            if(incident_creator == 'all'){
              usernameIncidents = incidents;
            }else{
              usernameIncidents = incidents.filter(incident => {
                filteredIncidents = incident.username === incident_creator;
                if (filteredIncidents){
                  return filteredIncidents;
                }else{
                  let result = '';
                  result += `
                    <div class="column-100">
                    <div class="card">
                        <div class="container">
                          
                            <p><i class="fa fa-star-half-o fa-3x" aria-hidden="true"></i></p>
                            <h4 class="theme-blue"><b>You have not posted any incidents</b></h4>
                          
                        </div>
                      </div>               
                  </div> 
                    `;
                    document.getElementById('incident-data').innerHTML = result;                  
                }
                
              })
            }

            usernameIncidents.forEach((incident) => {
                const { id, title, status, createdon, username, type } = incident
                let humanizedTime = humanize(createdon);
                
                if(username == profileUserName){
                  creator = 'Me';
                }else{
                  creator = username;
                }
                if(type == 'redflag'){
                    link = 'view_redflag.html?redflag_id';
                    icon = 'fa fa-flag red';
                }else if(type == 'intervention'){
                    link = 'view_intervention.html?intervention_id'
                    icon = 'fa fa-handshake-o theme-blue';
                }
                result += `
                <div class="column">
                  <div class="card">
                      <div class="container2 justify">
                        <a href="${link}=${id}">
                          <p><i class="${icon} fa-2x" aria-hidden="true"></i></p>
                          <h4 class="black truncate"><b>${title}</b></h4>
                        </a>
                          <a href="view_by_username.html?type=${type}&username=${username}"><p class='italic font-small'><span class="theme-blue">By ${creator}</span></p></a>
                          <p>${status}</p>
                          <p class='italic font-small'>${humanizedTime}</p>
                          <p class="black align-right"><i class="fa fa-external-link theme-blue" aria-hidden="true"></i></p>
                        
                      </div>
                    </div>               
                </div> 
                `;
                document.getElementById('incident-data').innerHTML = result;
              });
          }
                                      
        })
        .catch( (err) =>{
            
            document.getElementById('message').innerHTML = err;
        });
}

function getDataById(incident_type, incidentId){
            
    let uri = root + incident_type +'/' + incidentId;

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": tokenModels
        })
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              document.getElementById('fa-spin-data').style.display = "none";
              document.getElementById("btnGeolocate").disabled = false;
              return response.json();
            }else{
              document.getElementById('fa-spin-data').style.display = "none";
              return response.json();
            }
        })
        .then( (j) =>{
          console.log(j);
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'Intervention does not exist' || j['message'] == 'Redflag does not exist'){
              document.getElementById('message').innerHTML = j['message'];
            }
          }
          if(j.hasOwnProperty('data')){
            let result = '';
            let imageUrl = '';
              j['data'].map((incident) => {
                const { title, comment, status, createdon, location, username, images, type } = incident
                let localDateTime = convertToLocalTime(createdon);

                if(username == profileUserName){
                  creator = 'Me';
                  let ownerButtons = document.querySelectorAll('.btnOwner'), i;
                  for(i = 0; i < ownerButtons.length; ++i){
                    ownerButtons[i].style.display = 'inline';
                  }
                }else{
                  creator = username;
                  document.getElementById('btnGeolocate').style.display = 'inline';
                  try{
                    document.getElementById('btnEditStatus').style.display = 'inline';
                  }catch(error){}
                  
                }
                if(images == null){
                  imageUrl = 'img/bad-road.jpeg';
                }else{
                  getFileData('images', images)
                }
                result += `
                <h2>${title}</h2>
                <h3><span class="black">Status:</span> <span id='status-data' class="italic">${status}</span></h3>
                <h4><span class="black">Created On:</span> <span class="italic">${localDateTime}</span></h4>
                <h4><span class="black">By:</span> <a href="view_by_username.html?type=${type}&username=${username}"><span class="theme-blue">${creator}</span></a></h4>
                <div class="row  bg-color">
                  <div class="column-50 bg-color">
                    <p class='img-details'><img id='main-image' src="${imageUrl}" alt="${title}"></p>
                  </div>
                  <div class="column-50  bg-color align-justify">
                    <p id='comment-data'>${comment}</p>
                  </div>
                </div>  
                `;
                localStorage.clear();
                localStorage.setItem('coordinates', location);
                document.getElementById('incident-data').innerHTML = result;
                document.getElementById('title').value = title;
                document.getElementById('comment').value = comment;
                document.getElementById('location').value = location;
              });

          }
                                      
        })
        .catch( (err) =>{
            console.log(err);
        });
}

function deleteData(incident_type, incidentId){
    document.getElementById('fa-spin-data-delete').style.display = "block";
    document.getElementById('error-message').innerHTML = '';

    let uri = root + incident_type + '/' + incidentId;

    let options = {
        method: 'DELETE',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": tokenModels
        })
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              return response.json();
            }else{
              return response.json();
            }
        })
        .then( (j) =>{
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'Intervention does not exist' || j['message'] == 'Redflag does not exist'){
              document.getElementById('error-message').innerHTML = j['message'];
            }
            if(j['message'] == 'Only the creator of this record can delete it'){
              document.getElementById('error-message').innerHTML = j['message'];
            }
            if(j['message'] == 'Incident can only be deleted when the status is draft'){
              document.getElementById('error-message').innerHTML = j['message'];
            }

          }
          if(j.hasOwnProperty('data')){
            if(j['data']['message'] == 'Intervention record has been deleted' || j['data']['message'] == 'Redflag record has been deleted'){
              document.getElementById('error-message').innerHTML = j['data']['message'];
              if(incident_type == 'redflags'){
                window.location.replace("redflags.html");
              }else if(incident_type == 'interventions'){
                window.location.replace("interventions.html");
              }
            }                          
          }
          document.getElementById('fa-spin-data-delete').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('fa-spin-data-delete').style.display = "none";
        });
}

function uploadFile(){
  
}

function getFileData(filetype, filename){

  let uri = root + 'uploads/' + filetype + '/' + filename;

  let options = {
      method: 'GET',
      mode: "cors",
      headers: new Headers({
        // "Content-Type": "application/json; charset=utf-8",
        "x-access-token": tokenModels
      })
  }
  let req = new Request(uri, options);

  fetch(req)
      .then((response)=>{
          if(response.ok){
            return response.blob();
          }else{
            return response.json();
          }
      })
      .then( (j) =>{
        console.log(j);
        let contentType = j['type'].split('/')[0];

        if (contentType == 'application'){
          return 'Image not found';
        }else if(contentType == 'image'){
          var imgElem = document.getElementById('main-image');
          var imgUrl = URL.createObjectURL(j);
          imgElem.src = imgUrl;
        }
         
                                    
      })
      .catch( (err) =>{
          console.log(err);
      });
}

function editLocation(event, intervention_type, intervention_id){
  event.preventDefault();
    document.getElementById('fa-spin-edit').style.display = "block";

    let uri = root + intervention_type + '/' + intervention_id + '/location';

    let location = document.getElementById('location').value;

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
        }),
        body: JSON.stringify({location:location})
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              return response.json();
            }else{
              return response.json();
            }
        })
        .then( (j) =>{
          console.log(j);
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'Intervention does not exist' || 'Redflag does not exist'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
            if(j['message'] == 'Incident can only be edited when the status is draft'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
          }
          if(j.hasOwnProperty('data')){
            if(j['data'][0]['message'] == "Updated intervention record's location" || j['data'][0]['message'] == "Updated redflag record's location"){
              successNotification({ 
                    title: 'Success',
                    message: j['data'][0]['message'], 
              });
              localStorage.clear();
              localStorage.setItem('coordinates', location);
            }                          
          }                        
          document.getElementById('fa-spin-edit').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('fa-spin-edit').style.display = "none";
        });
} 

function editComment(event, intervention_type, intervention_id){
  event.preventDefault();
    document.getElementById('fa-spin-edit').style.display = "block";
    document.getElementById('comment').style.borderBottomColor = "#ccc";

    let uri = root + intervention_type + '/' + intervention_id + '/comment';

    let comment = document.getElementById('comment').value;

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
        }),
        body: JSON.stringify({comment:comment})
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              return response.json();
            }else{
              return response.json();
            }
        })
        .then( (j) =>{
          console.log(j);
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'Intervention does not exist' || j['message'] == 'Redflag does not exist'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
            if(j['message'].hasOwnProperty('comment')){
                document.getElementById('comment').style.borderBottomColor = "red";
                warningNotification({ 
                    title: 'Warning',
                    message: 'Comment cannot be empty or start with special characters and whitespace', 
                });
            }    
            if(j['message'] == 'Only the user who created this record can edit it'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
            if(j['message'] == 'Incident can only be edited when the status is draft'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
          }
          if(j.hasOwnProperty('data')){
            if(j['data'][0]['message'] == "Updated intervention record's comment" || j['data'][0]['message'] == "Updated redflag record's comment"){
              successNotification({ 
                    title: 'Success',
                    message: j['data'][0]['message'], 
              });
              document.getElementById('comment-data').innerHTML = comment;
            }                          
          }                        
          document.getElementById('fa-spin-edit').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('fa-spin-edit').style.display = "none";
        });
}

function editStatus(event, intervention_type, intervention_id){
  event.preventDefault();
    document.getElementById('fa-spin-edit-status').style.display = "block";

    let uri = root + intervention_type + '/' + intervention_id + '/status';

    let status = document.getElementById('status').value;

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
        }),
        body: JSON.stringify({status:status})
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              return response.json();
            }else{
              return response.json();
            }
        })
        .then( (j) =>{
          console.log(j);
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'Intervention does not exist' || j['message'] == 'Redflag does not exist'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
            if(j['message'].hasOwnProperty('status')){
                document.getElementById('status').style.borderBottomColor = "red";
                warningNotification({ 
                    title: 'Warning',
                    message: "Accepted values: draft, under investigation, rejected, resolved", 
              });
            }    
            if(j['message'] == 'Only an admin can change the status of the record'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }

          }
          if(j.hasOwnProperty('data')){
            if(j['data'][0]['message'] == "Updated intervention record's status" || j['data'][0]['message'] == "Updated redflag record's status"){
              successNotification({ 
                    title: 'Success',
                    message: j['data'][0]['message'], 
              });
              document.getElementById('status').value = status;
              document.getElementById('status-data').innerHTML = status;
            }                          
          }                        
          document.getElementById('fa-spin-edit-status').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('fa-spin-edit-status').style.display = "none";
        });
}

function uploadImage(event, intervention_type, intervention_id){
  event.preventDefault();
  document.getElementById('fa-spin-upload').style.display = "block";
  document.getElementById('upload-message').innerHTML = '';
  document.getElementById('upload-message').style.color = "red";

  let uri = root + intervention_type + '/' + intervention_id + '/addImage';

  var formData = new FormData();
  let fileData = document.getElementById('fileImage').files[0];

  if(fileData == null){
    document.getElementById('fa-spin-upload').style.display = "none";
    document.getElementById('upload-message').innerHTML = 'Please select a file';
    return false;
  }
  
  console.log(fileData);
  console.log(fileData.name);
  let fileExtension = fileData.name.split('.')[1];
  let uploadedFileName = intervention_id.toString() + '.' + fileExtension
  console.log(uploadedFileName);
  
  formData.append('uploadFile', fileData, fileData.name);
  // formData.append('name', 'uploadFile');

  let options = {
      method: 'PATCH',
      mode: "cors",
      headers: new Headers({
        "x-access-token": token,
      }),
      body: formData
  }
  let req = new Request(uri, options);

  fetch(req)
      .then((response)=>{
          if(response.ok){
            return response.json();
          }else{
            return response.json();
          }
      })
      .then( (j) =>{
        console.log(j);
        if(j.hasOwnProperty('message')){
          if(j['message'] == 'Token is missing'){
            logout();
          }
          if(j['message'] == 'Token is invalid'){
            logout();
          }
          if(j['message'] == 'Intervention does not exist' || j['message'] == 'Redflag does not exist'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }
          if(j['message'] == 'Only the user who created this record can edit it'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }
          if(j['message'] == 'Incident can only be edited when the status is draft'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }
          if(j['message'] == 'File type not supported' || j['message'] == 'No uploadFile name in form'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }

        }
        if(j.hasOwnProperty('data')){
          if(j['data'][0]['message'] == "Image added to intervention record" || j['data'][0]['message'] == "Image added to red-flag record"){
            document.getElementById('upload-message').style.color = "green";
            document.getElementById('upload-message').innerHTML = j['data'][0]['message'];
            getFileData('images', uploadedFileName);
          }                          
        }                        
        document.getElementById('fa-spin-upload').style.display = "none";
                                    
      })
      .catch( (err) =>{
          console.log(err);
          document.getElementById('upload-message').innerHTML = err;
          document.getElementById('fa-spin-upload').style.display = "none";
      });                

}

function uploadVideo(event, intervention_type, intervention_id){
  event.preventDefault();

}

function updateUserData(event, username_id){
  event.preventDefault();

}

function resetPassword(event, usernameid){
  event.preventDefault();
    document.getElementById('fa-spin-reset').style.display = "block";

    let uri = root + 'users/' + usernameid;

    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    if (password != confirm_password){
      document.getElementById('fa-spin-reset').style.display = "none";
      document.getElementById('submit').value = "Reset Password";
      document.getElementById('password').style.borderColor = "red";
      document.getElementById('confirm_password').style.borderColor = "red";
      return false;
    }

    let options = {
        method: 'PATCH',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
        }),
        body: JSON.stringify({password:password})
    }
    let req = new Request(uri, options);

    fetch(req)
        .then((response)=>{
            if(response.ok){
              return response.json();
            }else{
              return response.json();
            }
        })
        .then( (j) =>{
          if(j.hasOwnProperty('message')){
            if(j['message'] == 'Token is missing'){
              logout();
            }
            if(j['message'] == 'Token is invalid'){
              logout();
            }
            if(j['message'] == 'User does not exist'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }
            if(j['message'].hasOwnProperty('password')){
                document.getElementById('password').style.borderColor = "red";
                warningNotification({ 
                    title: 'Warning',
                    message: j['message']['password'], 
                });
            }    
            if(j['message'] == 'Only an admin or the user can update their own password'){
              warningNotification({ 
                    title: 'Warning',
                    message: j['message'], 
              });
            }

            if(j['message'] == 'User password has been changed'){
              successNotification({ 
                    title: 'Success',
                    message: j['message'] + ' for ' + j['username'], 
              });
            }

          }
      
          document.getElementById('fa-spin-reset').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('fa-spin-reset').style.display = "none";
        });
}

function checkPassword(){
  let pass1= document.getElementById('password').value;
  let confirm_pass1 = document.getElementById('confirm_password').value;

  if (pass1 == confirm_pass1){
    document.getElementById('password').style.borderColor = "green";
    document.getElementById('confirm_password').style.borderColor = "green";
  }else{
    document.getElementById('password').style.borderColor = "red";
    document.getElementById('confirm_password').style.borderColor = "red";
  }
}