// the support for captcha things
import {new_layer} from '/static/js/layer.js';

var captcha_init = function() {
	var ckey = random(1, 100000);
	$("input[name=ckey]").val(ckey);
	$("#captcha-pic").attr("src", "/captcha/get/{key}".format({key: ckey}));
};

var captcha_refresh = function() {
	var ckey = $("input[name=ckey]").val();
	$(this).attr('src', '/captcha/get/{key}?c={t}'.format({
		key: ckey,
		t: Math.random()
	}));
}

var ask_captcha = function(f) {
	var w = new_layer();
	var form = $("<form action=\"#\" method=\"post\" \"></form>");
	var ckinput = $("<input type=\"hidden\" name=\"ckey\" />");
	var cainput = $("<input type=\"text\" name=\"canswer\" />");
	var cimg = $("<img id=\"captcha-pic\" />");
	var submit = $("<input type=\"submit\" value=\"submit\">");
	form.append(ckinput);
	form.append(cainput);
	form.append(cimg);
	form.append(submit);
	w.append(form);
	
	captcha_init();
	cimg.onclick(captcha_refresh);
	
	form.onsubmit(f);
}

export {
	captcha_init,
	captcha_refresh,
	ask_captcha
}