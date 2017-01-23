"""
Authors: Sean Donohoe and Kyle Wiese

String templates for index.html
"""

keywordTag = """
<div class="form-group">
    <h3 style="display: inline; margin-right: 10px">{}</h3><input onclick="checkUpdate('{}')" type="checkbox" value="{}" name="{}-selected"><br>
    <div id={} style="margin-left:15%; width: 95%; display:none">
        <h5 style="display:inline">Don't spend longer than</h5>
        <select name="{}-upperHour" class="form-control" style="display:inline; width:10%; margin: 5px">
           {} 
        </select>
        <p style="display:inline">hours</p>
        <select name="{}-upperMinute" class="form-control" style="display:inline; width:10%; margin: 5px">
            <option value=0 selected>0</option>
            <option value=1800>30</option>
        </select>
        <p style="display:inline">minutes here</p><br>
        <h5 style="display:inline">Interest Multiplier</h5>
        <select name="{}-multiplier" class="form-control" style="display:inline; width:10%; margin: 5px">
            <option value=1 selected>1</option>
            <option value=2>2</option>
            <option value=3>3</option>
            <option value=4>4</option>
            <option value=5>5</option>
        </select><br>
        <h5 style="display:inline">Number of {} places visited: </h5>
        <select name="{}-equality" class="form-control" style="display:inline; width:15%; margin: 5px">
            <option value="NONE" selected>Unlimited</option>
            <option value="EQ"> = </option>
            <option value="LTE"> &le; </option>
            <option value="GTE"> &ge; </option>
        </select>
        <input type="number" class="form-control" style="display:inline; width:10%" name="{}-strictness" value="0" min="0" step="1"/>
    </div>
</div>
"""

keywordHourOptionTagSelected = """
<option value={} selected>{}</option>
"""

keywordHourOptionTag = """
<option value={}>{}</option>
"""

indexBegin = """
<!DOCTYPE html>
<html>
    <head>
        <title>Crawlr</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script>
            function checkUpdate(keyword) {
                var e = document.getElementById(keyword)
                if(e.style.display == 'block')
                    e.style.display = 'none'
                else
                    e.style.display = 'block'
            }
        </script>

	<script>
		var map = null;
		var start = null;
		var geocoder = null;
		var directionsService = null;
		var directionsDisplay = null;
	</script>

        
        <script>
            $(document).ready(function () {
                $('#pathdata').on('submit', function(e) {
                    e.preventDefault();
                    document.getElementById("queryPage").style.display = 'none';
                    document.getElementById("loading").style.display = 'block';
                    $.ajax({
                        type: 'post',
                        url: '/getRoute/',
                        data: $('#pathdata').serialize(),
                        dataType: 'json',
                        success: function(data) {
                            var ok = false;
                            document.getElementById("loading").style.display = 'none';
			    document.getElementById("results").style.display = 'block';
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
				}
                            });
			    if (ok == false) {
				document.getElementById("results").style.display = 'none';
                                document.getElementById("nopath").style.display = 'block';
			    }
                        }
                    });
                });
            });
        </script>
	<style>
		html, body {
			height: 100%;
			margin: 0;
			padding: 0;
		}
	</style>
    </head>

    <body>
	<nav class="navbar navbar-default">
	  <div class="container-fluid">
	    <div class="navbar-header">
	      <a class="navbar-brand" href= "/" >Crawlr</a>
	    </div> 
	  </div>
	</nav>

	<div class="container" id="queryPage">
	    <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <form id="pathdata">
                <div class="form-group">
                    <h4>Starting Address</h4>
                    <input class="form-control" type="text" id="addr" style="width:50%" name="start_address" placeholder="Address"><br>
                    <h4>Search Radius</h4>
                    <select class="form-control" name="searchRadius" style="width: 50%">
                        <option value=805 selected>0.5 miles</option>
                        <option value=1287>0.8</option>
                        <option value=1770>1.1 miles</option>
                    </select>
                    <h4>Average Budget</h4>
                    <select class="form-control" name="budget" style="width: 50%">
                        <option value=0>$</option>
                        <option value=1>$$</option>
                        <option value=2 selected>$$$</option>
                        <option value=3>$$$$</option>
                        <option value=4>$$$$$</option>
                    </select>
                    <h4>How Much Time do You Have?</h4>
                    <select name="userHour" class="form-control" style="display:inline;width: 15%">
                        <option value=0>0</option>
                        <option value=3600 selected>1</option>
                        <option value=7200>2</option>
                        <option value=10800>3</option>
                        <option value=14400>4</option>
                        <option value=18000>5</option>
                        <option value=21600>6</option>
                        <option value=25200>7</option>
                        <option value=28800>8</option>
                    </select>
                    <p style="display:inline; margin: 5px">hours</p>
                    <select name="userMinute" class="form-control" style="display:inline;width: 15%">
                        <option value=0>0</option>
                        <option value=1800 selected>30</option> 
                    </select> 
                    <p style="display:inline; margin: 5px">minutes</p>
                </div>
                <h4>Keywords</h4>
                <div style="margin-left: 10%">
"""

indexEnd = """
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div> 
        <div class="container" id="loading" style="display: none">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h4 style="text-align:center; display:inline">Calculating your adventure...</h4>
            <i class="fa fa-spinner fa-spin" style="font-size:24px; color: blue"></i>
        </div>
        <div class="container" id="results" style="display: none; height: 100%; width: 100%">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h1 class="display-3">Your Route</h1>
	    <div style="border-radius: 5px; overflow: scroll; background-color: #666666; display: inline; width: 48%; float: left">
	    	<ol id="finalpath" class="list-group" style="margin: 10px">
		</ol>
	    </div>
	    <div id="map" style="display: inline; float: right; height: 50%; width: 50%"></div>
       </div>
       <div class="container" id="nopath" style="display: none">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h3 style="margin: 0 auto; width: 50%">Sorry, we couldn't find a route for you!</h3>
        </div>
	<script>
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
	</script>
	<script async defer
	src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAwLw6rb6ifekvYt1vKA2jFvgG9AMCskRQ&libraries=places&callback=initMap">
	</script>
   </body>
</html>
"""


