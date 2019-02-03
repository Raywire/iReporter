function geocodeLatLng(geocoder, coordinates) {
  const input = coordinates;
  const location = [];
  const latlngStr = input.split(',', 2);
  const latlng = {
    lat: parseFloat(latlngStr[0]),
    lng: parseFloat(latlngStr[1]),
  };
  geocoder.geocode({
    location: latlng,
  }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
        location[0] = results[0].formatted_address;
      } else {
        location[0] = 'No results found';
      }
      document.getElementById('locationArea').innerHTML = location;
    } else {
      location[0] = `Geocoder failed due to: ${status}`;
    }
  });
  return location;
}

function myMap() {
  const coordinates = localStorage.getItem('coordinates');
  const latlon = coordinates.split(', ');
  const lat = parseFloat(latlon[0]);
  const lng = parseFloat(latlon[1]);

  const incidentMarkers = [];
  const centerMap = {
    center: new google.maps.LatLng(lat, lng), zoom: 6,
  };
  const incidentMap = new google.maps.Map(document.getElementById('googleMap'), centerMap);
  const geocoder = new google.maps.Geocoder();

  const incidentLocation = {
    lat,
    lng,
  };

  function addNewMarkers(location) {
    const marker = new google.maps.Marker({
      position: location,
      map: incidentMap,
      title: `${lat}, ${lng}`,
    });
    incidentMarkers.push(marker);
  }

  addNewMarkers(incidentLocation);
  geocodeLatLng(geocoder, coordinates);


  window.location.hash = '#googleMap';
}

const btnGeolocate = document.getElementById('btnGeolocate');
google.maps.event.addDomListener(btnGeolocate, 'click', myMap);
