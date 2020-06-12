// register javascript

var register = function(csrf_token) {
	
}

var isEmail = function(str) {
	if (mailReg.test(str)) {
		return true;
	} else {
		return false;
	}
};

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

	if (email != '' && email != undefined && !isEmail(email)) {
		$("#message").text("email is not correct.");
		return;
	}

	var register_data = {
		"username": username,
		"password": password,
		"email": email,

		"captcha-key": ckey,
		"captcha-ans": cans
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
			$("#message").text("Register Failed: Network Error.");
			$("input[name=password]").val('');
			$('input[name=password_confirmation]').val('');
			$('#captcha-pic').click();
		},
		success: function (data) {
			if (null != data && "" != data) {
<<<<<<< HEAD
				if (data.code == 20) { // success
=======
				if (data.code == 20) { 
					/*
					Reg success.
					See https://github.com/segment-oj/segmentoj/wiki/API%E6%8E%A5%E5%8F%A3%E8%AE%BF%E9%97%AE%E6%96%B9%E5%BC%8F#code%E5%90%AB%E4%B9%89 for ret code details.
					*/
					
>>>>>>> dev
					$("#message").text("Register Succesful. Please Login.");
					setTimeout(function() {
						window.location.href = "/";
					}, 1000);
				} else { // failed
					var msg = "Failed to register: [Err{code}]{msg}".format({
						code: data.code,
						msg: data.msg
					});
					$("#message").text(msg);
					$("input[name=password]").val('');
					$('input[name=password_confirmation]').val('');
					$('#captcha-pic').click();
				}
			}
		}
	});
};

var captcha_init = function() {
	var ckey = random(1, 100000);
	$("input[name=ckey]").val(ckey);
	$("#captcha-pic").attr("src", "/captcha/get/{key}".format({key: ckey}));
};

$(document).ready(function(){
	$("#captcha-pic").click(function() {
		var ckey = $("input[name=ckey]").val();
		$(this).attr('src', '/captcha/get/{key}?c={t}'.format({
			key: ckey,
			t: Math.random()
		}));
	});

	captcha_init();
});