let cookieModels = document.cookie.split(";");
let tokenKeyModels = cookieModels[0];
let tokenSplitModels = tokenKeyModels.split("token=");
let tokenModels = tokenSplitModels[1];

let userUsername = username.split("=");
userUsername = userUsername[1];

function getData(incident_type){
                      
    let uri = root + incident_type;

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
              j['data'].forEach((incident) => {
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
                          <p class='italic font-small'>By ${creator}</p>
                          <p>${status}</p>
                          <p class='italic font-small'>${createdon}</p>
                          <p class="black align-right"><i class="fa fa-external-link theme-blue" aria-hidden="true"></i></p>
                        </a>
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
                const { title, comment, status, createdon, location, username, images } = incident
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
                <h4><span class="black">By:</span> <span class="theme-blue">${creator}</span></h4>
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
