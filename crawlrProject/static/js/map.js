var map = null;
var start = null;
var geocoder = null;
var directionsService = null;
var directionsDisplay = null;

function initMap() {
  geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 9,
    center: {lat: 41.85, lng: -87.65},
  });
  directionsDisplay = new google.maps.DirectionsRenderer;
  directionsDisplay.setMap(map);
  directionsService = new google.maps.DirectionsService;
  var iA = document.getElementById('addr');
  var autocomplete = new google.maps.places.Autocomplete(iA);
}
