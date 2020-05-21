// login support javasript
import {ask_captcha} from '/static/js/captcha.js';

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
			$("#message").text("Login failed: Network Error.");
			$("input[name=password]").val('');
		},
		success: function (data) {
			if (null != data && "" != data) {
				if (data.code == 20) { // success
					$("#message").text("Login succes: Hello, {name}".format({
						name: username
					}));
					setTimeout(function() {
						window.location.href = "/";
					}, 500);
				} else { // failed
					$("#message").text("Login failed: [Err{code}]{msg}".format({
						code: data.code,
						msg: data.msg
					}));
					$("input[name=password]").val('');
				}
			}
		}
	});

	return false;
}