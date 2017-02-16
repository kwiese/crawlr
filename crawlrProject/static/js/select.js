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
var div_inserted = [false, false, false, false];

function addKeywordSelect(){
  var sel0 = document.getElementById("k-0");
  var sel1 = document.getElementById("k-1");
  var sel2 = document.getElementById("k-2");
  var val = "";
  var already_chosen = [null,null,null];
  if(sel0 != null){
    val = sel0.options[sel0.selectedIndex].value;
    if(val != "NONE-NONE"){
      already_chosen[0] = val
    }
  }
  if(sel1 != null){
    val = sel1.options[sel1.selectedIndex].value;
    if(val != "NONE-NONE"){
      already_chosen[1] = val
    }
  }
  if(sel2 != null){
    val = sel2.options[sel2.selectedIndex].value;
    if(val != "NONE-NONE"){
      already_chosen[2] = val
    }
  }

  var entry = "<div class='form-group' id='keyword-" + num_chosen.toString() +"'>";
  entry += "<select class='form-control' id='k-" + num_chosen.toString() + "' name='k-" + num_chosen.toString() + "'onchange='displayOptions(this.id);'>";
  entry += "<option value='NONE-NONE'>Select...</option>";
  for (var key in chosen){
    if (!chosen[key]){
      entry += "<option id='" + key + "-" + num_chosen.toString() + "' value='" + key + "-" + num_chosen.toString() + "'>" + key + "</option>";
    }
  }
  entry += "</select> <br>";
  entry += "</div>";
  entry += "<div class='form-group' id='keyword-options-" + num_chosen.toString() +"'></div>";
  document.getElementById("keyword-selection-" + num_chosen.toString()).innerHTML = document.getElementById("keyword-selection-" + num_chosen.toString()).innerHTML + entry;

  already_chosen.forEach(function(opt) {
    if(opt != null){
      if (opt.split("-")[1] != num_chosen.toString()){
        document.getElementById(opt.split("-")[0] + "-" + num_chosen.toString()).disabled = true;
      }
    }
  });
  if(num_chosen == 2){
    document.getElementById("keyword-add").disabled = true;
  }

}


function displayOptions(id){
  id = parseInt(id.split("-")[1]);
  var outer_div = document.getElementById("keyword-options-" + id);
  var sel = document.getElementById("k-" + id);

  if(!div_inserted[id]){
    var entry = "";

    entry += "<div class='container-fluid' style='background: rgba(55,104,183,0.6); color: #fff;'>";

    entry += "<div class='col-md-6'>";
    entry += "<h4>Time Limit</h4>";
    entry += "<div class='form-group row'>";
    entry += "<label class='col-md-2' for='" + id +"-hours'>Hours:</label>";
    entry += "<div class='col-md-4'>";
    entry += "<input name='" + id + "-hours' id='" + id +"-hours' class='form-control' type='number' min='0' step='1' placeholder='Hours'>";
    entry += "</div>";
    entry += "<label class='col-md-2' for='" + id +"-minutes'>Minutes:</label>";
    entry += "<div class='col-md-4'>";
    entry += "<input name='" + id + "-minutes' id='" + id +"-minutes' class='form-control' type='number' min='0' max='59' step='1' placeholder='Mins'>";
    entry += "</div>";
    entry += "</div>";
    entry += "</div>";

    entry += "<div class='col-md-6'>";
    entry += "<h4>Interest Multiplier</h4>";
    entry += "<div class='form-group row'>";
    entry += "<label class='col-md-2' for='" + id +"-interest'>Interest:</label>";
    entry += "<div class='col-md-4'>";
    entry += "<input name='" + id + "-interest' id='" + id +"-interest' class='form-control' type='number' min='0' step='1' placeholder='Multiplier'>";
    entry += "</div>";
    entry += "</div>";
    entry += "</div>";

    entry += "<div class='col-md-12'>";
    entry += "<h4>Number to Visit</h4>";
    entry += "<div class='form-group row'>";
    entry += "<label class='col-md-2' for='" + id +"-equality'>I want to visit:</label>";
    entry += "<div class='col-md-4'>";
    entry += "<select name='" + id + "-equality' class='form-control'> <option value='NONE' selected>Unlimited</option> <option value='EQ'> Exactly </option> <option value='LTE'> Less than </option> <option value='GTE'> More than </option> </select>";
    entry += "</div>";
    entry += "<div class='col-md-4'>"
    entry += "<input name='" + id + "-strictness' id='" + id +"-strictness' class='form-control' type='number' min='0' step='1' placeholder='Places'>";
    entry += "</div>";
    entry += "<label class='col-md-2' for='" + id +"-strictness'>places.</label>";
    entry += "</div>";
    entry += "</div>";

    entry += "</div>";

    outer_div.innerHTML = outer_div.innerHTML + entry;
    div_inserted[num_chosen] = true;
  }
}
