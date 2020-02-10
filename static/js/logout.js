// logout javascript

var logout = function(csrf_token) {
	$.ajax({
		type: 'POST',
		contentType: 'application/json; charset=utf-8',
		headers: {
			"X-CSRFToken": csrf_token
		}, 
		url: '/api/application/user/logout',
		cache: false,
		error: function() {
			$('#msg').text('Logout Failed.');
		},
		success: function(data) {
			if (data.code == 0) {
				$('#msg').text('Logout Success.');
				window.location.href = '/';
			} else {
				$('#msg').text('Logout Failed.');
			}
		}
	})
}