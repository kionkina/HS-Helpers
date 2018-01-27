
$(document).ready(function(){
console.log($('form').serialize());
    $("button").click(function(e){
	    e.preventDefault();
	    e.stopPropagation();
	    $.ajax({
		    type: "POST",
			url: "/ajax_helper",
			data: $('form').serialize(),
			success: function(response) {
			    console.log(response);
			    alert(response);
			$("#div1").html(response);
		    },
			error: function(error) {
			console.log(error);

		    }
		})
		})
	})


