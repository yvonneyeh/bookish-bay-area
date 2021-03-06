"use strict";

function initialize() {

    const defaultLocation = new google.maps.LatLng(37.787971,-122.418472)
  
    var contentString =
        '<div id="content">'+ "<p></p>"+'</div>';
  
    const mapOptions = {
      zoom: 11,
      center: defaultLocation
    };
  
    const map = new google.maps.Map(
        document.getElementById('map-canvas'),
        mapOptions);
  
    const infoWindow = new google.maps.InfoWindow({
        maxwidth: 200
    });
  
    const locations = {{ book_locations|tojson|safe }};
    console.log("locations = ", locations);
  
    // Attach markers to each location in returned JSON
          var location, marker, contentString;
  
          for (var key in locations) {
              location = locations[key];
              console.log("the key is ", key )
  
              // Define the marker
              marker = new google.maps.Marker({
                  position: new google.maps.LatLng(location.lat, location.lng),
                  map: map,
                  title: location.name
              });
  
              // Define the content of the infoWindow
              contentString = (
                  '<div class="window-content">' +
                      location.name +
                  '</div>');
  
        // Inside the loop call bindInfoWindow passing it the marker,
        // map, infoWindow and contentString
        bindInfoWindow(marker, map, infoWindow, contentString);
      }
  
  // This function is outside the for loop.
      // When a marker is clicked it closes any currently open infowindows
      // Sets the content for the new marker with the content passed through
      // then it open the infoWindow with the new content on the marker that's clicked
      function bindInfoWindow(marker, map, infoWindow, html) {
          google.maps.event.addListener(marker, 'click', function () {
              infoWindow.close();
              infoWindow.setContent(html);
              infoWindow.open(map, marker);
          });
      }
  }
  
  google.maps.event.addDomListener(window, 'load', initialize);