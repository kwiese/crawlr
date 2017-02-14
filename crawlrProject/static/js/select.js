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
  entry += "<select class='form-control' name='k-" + num_chosen.toString() + "'>";
  for (var key in chosen){
    if (chosen[key] == false){
      entry += "<option value='" + key + "'>" + key + "</option>";
    }
  }
  entry += "</select>";
  if (num_chosen < 3){
    alert("In if!")
    entry += "<button type='primary' name='add-" + num_chosen.toString() + "-options' onClick='displayOptions()'> Add another! </button>";
  }
  entry += "</div>";
  num_chosen += 1;
  document.getElementById("keyword-selection").innerHTML = document.getElementById("keyword-selection").innerHTML + entry;
}

function displayOptions(){
  var outer_div = document.getElementById("keyword-"+num_chosen.toString());
  var sel = document.getElementById("k-" + num_chosen.toString());
  var key = sel.options[sel.selectedIndex].value;
  var entry = "<h5 style='display:inline'>Don't spend longer than</h5><br>";
  entry += "<select name='" + key + "class='form-control' style='display:inline; width:10%; margin: 5px'>";
  entry += ""

}
