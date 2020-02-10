// login support javasript

var login = function(csrf_token) {
	var username = $("input[name=username]").val();
	var password = $("input[name=password]").val();
	var login_data = {
		"username": username,
		"password": password
	};

	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		headers: { "X-CSRFToken": csrf_token },
		url: "/api/application/user/login",
		dataType: "json",
		cache: false,
		data: JSON.stringify(login_data),
		error: function () {
			$("#message").text("login failed");
			$("input[name=password]").val('');
		},
		success: function (data) {
			if (null != data && "" != data) {
				if (data.code == 0) { // success
					$("#message").text("Login succes: " + data.msg);
					setTimeout(function() {
						window.location.href = "/";
					}, 500);
				} else { // failed
					$("#message").text("Login failed: " + data.msg);
					$("input[name=password]").val('');
				}
			}
		}
	});

	return false;
}