$(document).ready(function(){
	$("#id_rate_type").change(function() {
		if ($("#id_rate_type").val() == "user") {
			$(".field-gateway").hide()
		}
		else {
			$(".field-gateway").show()
		}

    });
 });
