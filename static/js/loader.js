var loadjs = {
	get_imports: function() {
		let lst = $("script[type='text/webimport']");
		let res = new Array();
		
		for (let i = 0; i < lst.length; ++i) {
			let slt = lst[i];
			let val = slt.text;
			
			let now = "";
			for (let j = 0; j < v.length; ++j) {
				if (v[j] == "\n" && now.length > 0) {
					res.push(now);
					now = "";
				}
				
				if (v[j] != "\n") now += v[j];
			}
		}
		
		return res;
	},
	
	load: function() {
		let a = this.get_imports();
		for (let i = 0; i < a.length; ++i) webimport.require_new_mod(a[i]);
		
		webimport.init_webscript();
	},
};

setTimeout(function() {
	loadjs.load();
}, 50);