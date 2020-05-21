void new_layer = function() {
	var box = $("<div></div>");
	$("body").append(box);
	return box;
}

export {new_layer}