// import packages

window.webimport = {};
window.webimport.conf_path = "/static/json/webimport/load.json";
window.webimport.loaded_mods = new Array();
window.webimport.waiting_to_load = new Array();
window.webimport.mod_name_map = new Map();
window.webimport.mod_id_map = new Array();
window.webimport.dep_graph = new Array();
window.webimport.mod_cnt = 0;

// e referres to methods obj, f referrers to wantted export objs
var webexport = function(e, f) {
	for (var i = 0; i < f.length; ++i) {
		if (window[f[i]] != undefined) {
			console.error("Identifier " + f[i] + " already in use when loading.");
			continue;
		}
		
		if (e[f[i]] == undefined) {
			console.error("Identifier " + f[i] + " not defined when exporting.");
			continue;
		}
		
		window[f[i]] = e[f[i]];
	}
}

var array_unique = function(a) {
	let s = new Set(a);
	let res = new Array(s);
	return res;
}

window.webimport.methods = {
	load_json: function(url) {
		let data = $.get(url);
		let res = eval("(" + data + ")");
		return res;
	},

	require_new_mod: function(name) {
		window.webimport.waiting_to_load.push(name);
	},

	list_mods: function(name) {
		let mod_conf = load_json(window.webimport.baseurl + name + ".json");
		if (mod_conf.name != name) {
			console.error("Module " + name + " name dissmatch.");
			return false;
		}
		
		for (let i = 0; i < name.depandence.length; i++) {
			if (this.list_mods(name.dependence[i])) {
				console.error("Module " + name + " dependence load failed.");
				return false;
			}
		}
		
		if (window.webimport.loaded_mods.indexOf(mod_conf.name) != -1) { 
			window.webimport.waiting_to_load.push(mod_conf);
			
			window.webimport.mod_name_map.set(mod_conf.name, ++window.webimport.mod_cnt);
			window.webimport.mod_id_map[window.webimport.mod_cnt] = mod_conf.name;
		}
		
		return true;
	},
	
	init_dependence_graph: function() {
		let res = new Array();
		
		for (let i = 0; i < window.webimport.waiting_to_load.length; ++i) {
			let deps = window.webimport.waiting_to_load[i].depandence;
			if (deps == undefined || deps.length == 0) continue;
			for (let j = 0; j < deps.length; ++j) {
				let x = deps[j];
				if (typeof(x) != "string") {
					console.warn("Type error when calculating Module " + window.webimport.waiting_to_load[i].name + " dependences");
					continue;
				}
				
				res[i].push(window.webimport.mod_name_map.get(x));
			}
		}
		
		return res;
	},
	
	load_script: function(mod_conf) {
		if (window.webimport.loaded_mods.indexOf(mod_conf.name) != -1) {
			console.warn("Module " + mod_conf.name + " already loaded.")
		}
		
		let tag = $("<script></script>");
		tag.attr("src", mod_conf.path);
		$("#load_static").append(tag);
		
		window.webimport.loaded_mods.push(mod_conf.name);
	},
	
	topu_sort: function() {
		window.webimport.waiting_to_load = array_unique(window.webimport.waiting_to_load);
		let G = this.init_dependence_graph();
		window.webimport.depandence_graph = G;
		
		let in_cnt = new Array();
		for (let i = 0; i < G.length; ++i) {
			if (G[i] == undefined) continue;
			for (let j = 0; j < G[i].length; ++j) {
				++in_cnt[G[i][j]];
			}
		}
		
		let res = new Array();
		let q = new Queue();
		for (let i = 0; i < G.length; ++i) {
			if (G[i] == undefined) continue;
			if (in_cnt[i] === 0) q.push(i);
		}
		
		while (!q.empty()) {
			let x = q.front();
			res.push(x);
			q.pop();
			
			for (let i = 0; i < G[x].length; ++i) {
				int y = G[x][i];
				--in_cnt[y];
				if (in_cnt[y] === 0) q.push(y);
			}
		}
		
		window.webimport.waiting_to_load = res;
		return res;
	},
};

webexport(window.webimport.methods, ["require_new_mod", "load_modules"]);