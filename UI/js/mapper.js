function addLocation() {

    let coordinates = document.getElementById('location').value;
    let latlon = coordinates.split(', ');
    let lat = parseFloat(latlon[0]);
    let lng = parseFloat(latlon[1]);
    if(coordinates===''){
      lat = -1.2921;
      lng = 36.8219;
    }

    var markers = [];
    var mapProp= {
      center:new google.maps.LatLng(lat,lng),
      zoom:6,
    };

    var map = new google.maps.Map(document.getElementById('addMarker'),mapProp);

    //Add marker of current location
    var incidentLocation = {lat, lng};
    addNewMarkers(incidentLocation);

    // Update lat/long value of div when anywhere in the map is clicked    
    google.maps.event.addListener(map,'click',function(event) {
        let position = event.latLng.lat()+', '+event.latLng.lng();            
        document.getElementById('location').value = position;
    });

    // Create new marker on single click event on the map
    google.maps.event.addListener(map,'click',function(event) {
      deleteMarker();
      addNewMarkers(event.latLng);             
    });           
    function addNewMarkers(position) {
    var marker = new google.maps.Marker({
      position,
      map
    });
    markers.push(marker);
  }
    function deleteMarker() {
      for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
      }
      markers = [];
    }                                         
  }

  var btnEdit = document.getElementById('btnEdit');
  google.maps.event.addDomListener(btnEdit, 'click', addLocation);