// register javascript

mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;

var isEmail = function(str) {
	if (mailReg.test(str)) {
		return true;
	} else {
		return false;
	}
}

var register = function(csrf_token) {
	var username = $("input[name=username]").val();
	var password = $("input[name=password]").val();
	var password_confirmation = $("input[name=password_confirmation]").val();
	var email = $("input[name=email]").val();

	if (password != password_confirmation) {
		$("#message").text("password mismatch.");
		return;
	}

	if (username == "") {
		$("#message").text("username is required.");
		return;
	}

	if (password.length < 6) {
		$("#message").text("password is too short.");
		return;
	}

	if (!isEmail(email)) {
		$("#message").text("email is not correct.");
		return;
	}

	var register_data = {
		"username": username,
		"password": password,
		"email": email
	};

	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		headers: { "X-CSRFToken": csrf_token },
		url: "/api/application/user/register",
		dataType: "json",
		cache: false,
		data: JSON.stringify(register_data),
		error: function () {
			$("#message").text("register failed");
			$("input[name=password]").val('');
			$('input[name=password_confirmation]').val('');
		},
		success: function (data) {
			if (null != data && "" != data) {
				if (data.code == 0) { // success
					$("#message").text("Register Succesful. Please Login.");
					setTimeout(function() {
						window.location.href = "/";
					}, 1000);
				} else { // failed
					$("#message").text("Failed to register.");
					$("input[name=password]").val('');
					$('input[name=password_confirmation]').val('');
				}
			}
		}
	});
}