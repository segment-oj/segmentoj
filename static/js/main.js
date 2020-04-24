String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }
 
    var data = arguments;
    if (arguments.length == 1 && typeof(args) == "object") {
        data = args;
    }
	
    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replace("{" + key + "}", value);
        }
	}
    return result;
}

var random = function(min, max) {
	return Math.floor(Math.random() * (max - min)) + min;
}