function getData(incident_type){
                      
    let uri = root + incident_type;

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];
    // console.log(token);

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
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
              j['data'].forEach((incident) => {
                const { id, title, status, createdon, username, type } = incident
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
                          <p class='italic font-small'>By ${username}</p>
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

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];

    let options = {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
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
              j['data'].map((incident) => {
                const { title, comment, status, createdon, location, username } = incident
                result += `
                <h2>${title}</h2>
                <h3><span class="black">Status:</span> <span id='status-data' class="italic">${status}</span></h3>
                <h4><span class="black">Created On:</span> <span class="italic">${createdon}</span></h4>
                <h4><span class="black">By:</span> <span class="theme-blue">${username}</span></h4>
                <div class="row  bg-color">
                  <div class="column-50 bg-color">
                    
                    <p class='img-details'><img src="img/bad-road.jpeg" alt=""></p>
                    <p><img src="" alt=""></p>
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

    let cookie = document.cookie.split(";");
    let tokenKeyValue = cookie[0];
    let tokenSplit = tokenKeyValue.split("token=");
    let token = tokenSplit[1];

    let options = {
        method: 'DELETE',
        mode: "cors",
        headers: new Headers({
          "Content-Type": "application/json; charset=utf-8",
          "x-access-token": token
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