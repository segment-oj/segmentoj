// useful tools

var isEmail = function(str) {
	var mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
	if (mailReg.test(str)) {
		return true;
	} else {
		return false;
	}
};