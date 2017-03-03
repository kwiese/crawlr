$(document).ready(function () {	
	$("#nextButton").click(function(e){
		e.preventDefault();
		$("#pageOne").hide(500);
		$("#pageTwo").show(500);
		$("#pageOneText").hide(500);
		$("#pageTwoText").show(500);

	});

	$("#backButton").click(function(e){
		e.preventDefault();
		$("#pageTwo").hide(500);
		$("#pageOne").show(500);
		$("#pageTwoText").hide(500);
		$("#pageOneText").show(500);
	});
});