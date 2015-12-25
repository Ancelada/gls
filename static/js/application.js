$(document).ready(function(){
	var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	$.ajax({
		type:"POST",
		url:"/getkoors/",
		data:{'csrfmiddlewaretoken': csrf_token},
		success: function(data, textStatus, jqXHR){
			$('#result').html(data);
		},
		dataType: 'html',
	})
});