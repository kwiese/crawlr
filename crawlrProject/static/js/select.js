var l_bounds = {
  'restaurant': 1200,
  'cafe': 300,
  'art_gallery': 1800,
  'bakery': 900,
  'bar': 1800,
  'book_store': 900,
  'clothing_store': 900,
  'library': 2700,
  'liquor_store': 900,
  'museum': 5400,
  'night_club': 1800,
  'park': 1800,
  'shopping_mall': 2700,
};

var chosen = {
  'restaurant': false,
  'cafe': false,
  'art_gallery': false,
  'bakery': false,
  'bar': false,
  'book_store': false,
  'clothing_store': false,
  'library': false,
  'liquor_store': false,
  'museum': false,
  'night_club': false,
  'park': false,
  'shopping_mall': false,
};

var num_chosen = 0;

function addKeywordSelect(){
  var entry = "<div class='form-group' id='keyword-" + num_chosen.toString() +"'>";
  entry += "<select class='form-control' id='k-" + num_chosen.toString() + "' name='k-" + num_chosen.toString() + "' onchange='displayOptions();'>";
  entry += "<option value='NONE'>Select...</option>";
  for (var key in chosen){
    if (chosen[key] == false){
      entry += "<option value='" + key + "'>" + key + "</option>";
    }
  }
  entry += "</select>";
  entry += "<div class='timeField' id='keyword-options-" + num_chosen.toString() +"'></div>";
  if (num_chosen < 3){
    entry += "<button class='btn btn-primary' name='add-" + num_chosen.toString() + "-options' onClick='num_chosen += 1; addKeywordSelect();'>Add</button>";
  }
  entry += "</div>";
  document.getElementById("keyword-selection").innerHTML = document.getElementById("keyword-selection").innerHTML + entry;
}


function displayOptions(){
  var outer_div = document.getElementById("keyword-options-"+num_chosen.toString());
  var sel = document.getElementById("k-" + num_chosen.toString());
  var key = sel.options[sel.selectedIndex].value;
  var entry = "<h5 style='display:inline'>Don't spend longer than</h5>";
  entry += "<input id='" + key +"-hours' class='form-control' type='number' min='0' step='1' placeholder='Max Hours' style='width: 15%'>";
  entry += "<p style='display:inline'> Hours </p>"
  entry += "<input id='" + key +"-minutes' class='form-control' type='number' min='0' max='59' step='1' placeholder='Max Mins' style='display:inline;width: 15%'>";
  entry += "<p style='display:inline'> Minutes </p> <br><br>"
  outer_div.innerHTML = outer_div.innerHTML + entry;

}
