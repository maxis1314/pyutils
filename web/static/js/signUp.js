$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
                var json_parsed = $.parseJSON(response);
				console.log(json_parsed.error);
                if(json_parsed.error == 0){
                    window.location='/showSignIn';
                }
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
