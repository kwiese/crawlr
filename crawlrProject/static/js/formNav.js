var addressOk = false;
var timeOk = true;

$(document).ready(function () {
	$("#nextButton").click(function(e){
		e.preventDefault();
		if(addressOk && timeOk){
			$("#pageOne").hide(500);
			$("#pageTwo").show(500);
			$("#pageOneText").hide(500);
			$("#pageTwoText").show(500);
		}
		else{
			validateAddress();
			validateTime();
		}

	});

	$("#backButton").click(function(e){
		e.preventDefault();
		$("#pageTwo").hide(500);
		$("#pageOne").show(500);
		$("#pageTwoText").hide(500);
		$("#pageOneText").show(500);
	});
});

function validateAddress(){
  var address=document.getElementById("addr").value;
  
  if(address == ""){
    $('#addr_input').addClass('has-error');
    $('#addr_input').addClass('has-feedback');
    $('#addr_label').css({'color':'#a94442'});
    $('#addr_message').show();
    $('#addr_icon').show();
    addressOk = false;
  }
  else{
    $('#addr_input').removeClass('has-error');
    $('#addr_input').removeClass('has-feedback');
    $('#addr_label').css({'color':'black'});
    $('#addr_message').hide();
    $('#addr_icon').hide();
    addressOk = true;
  }
}

function validateTime(){
  var hour=document.getElementById("userHour").value;
  var minute=document.getElementById("userMinute").value;
  if((hour == 0 && minute == 0)||hour < 0||minute < 0){
    $('#time_available').addClass('has-error');
    $('#time_label').css({'color':'#a94442'});
    $('#userHour').css({'margin-bottom':'0'});
    $('#userMinute').css({'margin-bottom':'0'});
    $('#time_message').show();
    timeOk = false;
  }
  else{
    $('#time_available').removeClass('has-error');
    $('#time_label').css({'color':'black'});
    $('#time_message').hide();
    timeOk = true;
  }
}

function checkBudget(){
  var budget = document.getElementById("budget_select").value;
  if(budget == 0){
    //document.getElementById("budget").classList.add("has-warning");
    $('#budget').addClass('has-warning');
    $('#budget_label').css({'color':'#8a6d3b'});
    $('#budget_select').css({'margin-bottom':'0'});
    $('#budget_message').show();
  }
  else{
    $('#budget').removeClass('has-warning');
    $('#budget_label').css({'color':'black'});
    $('#budget_message').hide();
  }
}
