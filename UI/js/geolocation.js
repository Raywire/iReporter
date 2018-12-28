function myMap() {
  let coordinates = localStorage.getItem('coordinates');
  let latlon = coordinates.split(", ");
  let lat = parseFloat(latlon[0]);
  let lon = parseFloat(latlon[1]);

  var markers = [];
  var mapProp= {
    center:new google.maps.LatLng(lat,lon),
    zoom:6,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
  var geocoder = new google.maps.Geocoder;

  var incidentLocation = {lat: lat, lng: lon};

  addNewMarkers(incidentLocation);
  geocodeLatLng(geocoder,coordinates);
  
  function addNewMarkers(location) {
    var marker = new google.maps.Marker({
      position: location,
      map: map,
      title: lat+', '+lon
    });
    markers.push(marker);
  }                                         
}

function geocodeLatLng(geocoder, coordinates) {
    var input = coordinates;
    var location = [];
    var latlngStr = input.split(',', 2);
    var latlng = {lat: parseFloat(latlngStr[0]), lng: parseFloat(latlngStr[1])};
    geocoder.geocode({'location': latlng}, function(results, status) {
      if (status === 'OK') {
        if (results[0]) {
          location[0] = results[0].formatted_address;
        } else {
            location[0] ='No results found';
        }
        document.getElementById('locationArea').innerHTML = location[0];
      } else {
        location[0] = 'Geocoder failed due to: ' + status;
      }
    });
    return location;
  }


var btnGeolocate = document.getElementById('btnGeolocate');
google.maps.event.addDomListener(btnGeolocate, 'click', myMap);