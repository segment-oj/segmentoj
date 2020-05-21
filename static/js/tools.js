// useful tools

mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;

var isEmail = function(str) {
	if (mailReg.test(str)) {
		return true;
	} else {
		return false;
	}
};

export {isEmail};