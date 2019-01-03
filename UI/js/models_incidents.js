let cookieModels = document.cookie.split(";");
let tokenKeyModels = cookieModels[0];
let tokenSplitModels = tokenKeyModels.split("token=");
let tokenModels = tokenSplitModels[1];

let userUsername = username.split("=");
userUsername = userUsername[1];

function postData(event, incident_type){
  event.preventDefault();   
  document.getElementById('title').style.borderBottomColor = "gray";
  document.getElementById('comment').style.borderBottomColor = "gray";
  document.getElementById('location').style.borderBottomColor = "gray";
  document.getElementById('fa-spin').style.display = "block";
  document.getElementById('submit').value = "Creating";

  let uri = root + incident_type;             

  let title = document.getElementById('title').value;
  let comment = document.getElementById('comment').value;
  let location = document.getElementById('location').value;

  let cookie = document.cookie.split(";");
  let tokenKeyValue = cookie[0];
  let tokenSplit = tokenKeyValue.split("token=");
  let token = tokenSplit[1];
  // console.log(token);

  let options = {
      method: 'POST',
      mode: "cors",
      headers: new Headers({
        "Content-Type": "application/json; charset=utf-8",
        "x-access-token": token
      }),
      body: JSON.stringify({title:title,comment:comment,location:location})
  }
  let req = new Request(uri, options);

  fetch(req)
      .then((response)=>{
          if(response.ok){
            document.getElementById('fa-spin').style.display = "none";
            // document.getElementById('submit').value = "Add Red Flag";

            return response.json();
          }else{
            document.getElementById('fa-spin').style.display = "none";
            // document.getElementById('submit').value = "Add Red Flag";
            return response.json();
          }
      })
      .then( (j) =>{
        // console.log(j);
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
                return incident.username === incident_creator;
              })
            }
            // let usernameIncidents = incidents.filter(incident => {
            //   return incident.username === incident_creator;
            // })
            usernameIncidents.forEach((incident) => {
                const { id, title, status, createdon, username, type } = incident
                if(username == userUsername){
                  creator = 'Me';
                }else{
                  creator = username;
                }
                if(type == 'redflag'){
                    link = 'view_redflag.html?redflag_id';
                }else if(type == 'intervention'){
                    link = 'view_intervention.html?intervention_id'
                }
                result += `
                <div class="column">
                  <div class="card">
                      <div class="container2">
                        <a href="${link}=${id}">
                          <p><i class="fa fa-flag red fa-3x" aria-hidden="true"></i></p>
                          <h4 class="black truncate"><b>${title}</b></h4>
                        </a>
                          <a href="view_by_username.html?type=${type}&username=${username}"><p class='italic font-small'><span class="theme-blue">By ${creator}</span></p></a>
                          <p>${status}</p>
                          <p class='italic font-small'>${createdon}</p>
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
                if(username == userUsername){
                  creator = 'Me';
                }else{
                  creator = username;
                }
                if(images == null){
                  imageUrl = 'img/bad-road.jpeg';
                }else{
                  getFileData('images', images)
                }
                result += `
                <h2>${title}</h2>
                <h3><span class="black">Status:</span> <span id='status-data' class="italic">${status}</span></h3>
                <h4><span class="black">Created On:</span> <span class="italic">${createdon}</span></h4>
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
            // document.getElementById('message').innerHTML = err;
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
          console.log(j);
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
            }                          
          }
          document.getElementById('fa-spin-data-delete').style.display = "none";
                                      
        })
        .catch( (err) =>{
            console.log(err);
            document.getElementById('error-message').innerHTML = err;
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

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];

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
            // if(j['message'] == 'Only the user who created this record can edit it'){
            //   warningNotification({ 
            //         title: 'Warning',
            //         message: j['message'], 
            //   });
            // }
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
    document.getElementById('comment').style.borderBottomColor = "gray";

    let uri = root + intervention_type + '/' + intervention_id + '/comment';

    let comment = document.getElementById('comment').value;

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];

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

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];

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
  
  formData.append('uploadFile', fileData, fileData.name);
  formData.append('name', 'uploadFile');


  let cookie = document.cookie.split(";");
  let tokenKeyValue = cookie[0];
  let tokenSplit = tokenKeyValue.split("token=");
  let token = tokenSplit[1];

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

          // if(j['message'] == 'Only the user who created this record can edit it'){
          //   document.getElementById('upload-message').innerHTML = j['message'];
          // }
          if(j['message'] == 'Incident can only be edited when the status is draft'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }
          if(j['message'] == 'File type not supported'){
            document.getElementById('upload-message').innerHTML = j['message'];
          }

        }
        if(j.hasOwnProperty('data')){
          if(j['data'][0]['message'] == "Image added to intervention record" || j['data'][0]['message'] == "Image added to red-flag record"){
            document.getElementById('upload-message').style.color = "green";
            document.getElementById('upload-message').innerHTML = j['data'][0]['message'];
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