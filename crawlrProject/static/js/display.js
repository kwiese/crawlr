$(document).ready(function () {
  $('#pathdata').on('submit', function(e) {
    e.preventDefault();
    document.getElementById("queryPage").style.display = 'none';
    document.getElementById("loading-parent").style.display = 'block';
    document.getElementById('timestamp').value = Date(Date.UTC());
    $.ajax({
      type: 'post',
      data: $('#pathdata').serialize(),
      dataType: 'json',
      success: function(data) {
        var ok = false;
				var error = "";
        document.getElementById("loading").style.display = 'none';
        document.getElementById("results").style.display = 'block';
        document.getElementById("feedback").style.display = 'block';
        google.maps.event.trigger(map, 'resize');
        $.each(data, function(k, v) {
          if (k == "path"){
            if (data[k].length > 0) {
              ok = true;
              for (var i in data[k]) {
                var j = 65 + (parseInt(i));
                var sss = String.fromCharCode(j);
                $("#finalpath").append("<li class='list-group-item' style='margin: 5px'>"+ sss + ") "  + data[k][i] + "</li>");
              }
            } else {
              document.getElementById("results").style.display = 'none';
              document.getElementById("nopath").style.display = 'block';
              document.getElementById("feedback").style.display = 'block';
            }
          } else if (k == "addresses"){
            if (data[k].length > 0) {
              ok = true;
              var bounds = new google.maps.LatLngBounds();
              var numCalls = data[k].length;
              var waypts = [];
              var o = null;
              var d = null;

              for (var i in data[k]) {
                var entry = data[k][i];

                if (i == 0) {
                  o = entry;
                } else if (i == data[k].length - 1) {
                  d = entry;
                } else {
                  waypts.push({
                    location: entry,
                    stopover: true
                  });
                }
              }
              directionsService.route({
                origin: o,
                destination: d,
                waypoints: waypts,
                optimizeWaypoints: false,
                travelMode: 'WALKING',
              }, function(response, status) {
                if (status == 'OK') {
                  directionsDisplay.setDirections(response);
                } else {
                  alert('Directions request failed: ' + status);
                }
              });
            }
          } else if (k == "error"){
						error = data[k];
						ok = false;
					}
        });
        if (ok == false) {
          document.getElementById("results").style.display = 'none';
          document.getElementById("nopath").style.display = 'block';
					document.getElementById("nopath").innerHTML = error;
        }
      }
    });
  });
  $('#feedback-form').on('submit', function(e) {
    e.preventDefault();
    document.getElementById("feedback").style.display = 'none';
    document.getElementById("feedback-submitted").style.display = 'block';
    $.ajax({
      type: 'post',
      url: '/feedback/',
      data: $('#feedback-form').serialize(),
      dataType: 'json',
      success: function(data) {
      }
    });
  });
});
