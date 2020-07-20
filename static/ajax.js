/* Article FructCode.com */
$( document ).ready(function() {
    $("#submit_btn").click(
		function(){
			sendAjaxForm('result_form', 'ajax_form', '/create');
			return false;
		}
	);
    $( "#new_one_btn" ).click(function() {
      $('#ajax_form').show();
      $('#result_form').hide();
      $('#enterLink').val('')
    });

});

function sendAjaxForm(result_form, ajax_form, url) {
    $.ajax({
    url:     url,
    type:     "POST",
    dataType: "html",
    data: $("#"+ajax_form).serialize(),
    success: function(response) { //Данные отправлены успешно
        result = $.parseJSON(response);
        if (result.error) {
            alert("Error: " + result.error)
        } else {
            $('#ajax_form').hide();
            $('#result_form').show();
            $('#result_input').val(window.location.href + result.id);
        }
    },
    error: function(response) { // Данные не отправлены
        alert("Error")
    }
    });


}
