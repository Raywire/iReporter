function addLocation() {
  const coordinates = document.getElementById('location').value;
  const latlon = coordinates.split(', ');
  let lat = parseFloat(latlon[0]);
  let lng = parseFloat(latlon[1]);
  if (coordinates === '') {
    lat = -1.2921;
    lng = 36.8219;
  }

  let markers = [];
  const mapProp = {
    center: new google.maps.LatLng(lat, lng),
    zoom: 6,
  };

  const map = new google.maps.Map(document.getElementById('addMarker'), mapProp);

  function addNewMarkers(position) {
    const marker = new google.maps.Marker({
      position,
      map,
    });
    markers.push(marker);
  }

  function deleteMarker() {
    for (let i = 0; i < markers.length; i += 1) {
      markers[i].setMap(null);
    }
    markers = [];
  }

  // Add marker of current location
  const incidentLocation = {
    lat,
    lng,
  };
  addNewMarkers(incidentLocation);

  // Update lat/long value of div when anywhere in the map is clicked
  const updateMap = (event) => {
    const position = `${event.latLng.lat()},  ${event.latLng.lng()}`;
    document.getElementById('location').value = position;
  };
  google.maps.event.addListener(map, 'click', event => updateMap(event));

  // Create new marker on single click event on the map
  const createMarker = (event) => {
    deleteMarker();
    addNewMarkers(event.latLng);
  };
  google.maps.event.addListener(map, 'click', event => createMarker(event));
}

const btnEdit = document.getElementById('btnEdit');
google.maps.event.addDomListener(btnEdit, 'click', addLocation);
