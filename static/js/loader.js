var loadjs = {
	get_imports: function() {
		let lst = $("script[type='text/webimport']");
		let res = new Array();
		
		for (let i = 0; i < lst.length; ++i) {
			let slt = lst[i];
			let val = slt.text;
			
			let now = "";
			for (let j = 0; j < val.length; ++j) {
				if (val[j] == "\n" && now.length > 0) {
					res.push(now);
					now = "";
				}
				
				if (val[j] != "\n") now += val[j];
			}
		}
		
		return res;
	},
	
	load: function() {
		let a = this.get_imports();
		for (let i = 0; i < a.length; ++i) webimport.require_new_mod(a[i]);
		
		webimport.init_webscripts();
	},
};

setTimeout(function() {
	loadjs.load();
}, 50);