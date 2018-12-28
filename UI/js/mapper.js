function addLocation() {
    var markers = [];
    var mapProp= {
      center:new google.maps.LatLng(-1.2921,36.8219),
      zoom:6,
    };
    var map = new google.maps.Map(document.getElementById("addMarker"),mapProp);
    // Update lat/long value of div when anywhere in the map is clicked    
    google.maps.event.addListener(map,'click',function(event) {
        let location = event.latLng.lat()+', '+event.latLng.lng();            
        document.getElementById('location').value = location;
    });

    // Create new marker on single click event on the map
    google.maps.event.addListener(map,'click',function(event) {
      deleteMarker();
      addNewMarkers(event.latLng);             
    });           
    function addNewMarkers(location) {
    var marker = new google.maps.Marker({
      position: location,
      map: map,
      // icon: "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
      //   title: event.latLng.lat()+', '+event.latLng.lng()
    });
    markers.push(marker);
  }
    function deleteMarker() {
      for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
      }
      markers = [];
    };                                          
  }

  var btnEdit = document.getElementById('btnEdit');
  google.maps.event.addDomListener(btnEdit, 'click', addLocation);  
  