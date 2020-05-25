// register javascript

mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;

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

	var ckey = $("input[name=ckey]").val();
	var cans = $("input[name=canswer]").val();

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
				if (data.code == 20) { // success
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