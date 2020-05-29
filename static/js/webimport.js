// import packages

var array_unique = function(a) {
	let s = new Set(a);
	let res = new Array(s);
	return res;
}

window.webimport = {
	baseurl: "/static/json/webimport/",
	loaded_mods: new Array(),
	waiting_to_load: new Array(),
	mod_name_map: new Map(),
	mod_id_map: new Array(),
	dep_graph: new Array(),
	mod_cnt: 0,

	load_json: function(url) {
		let data = $.get(url);
		let res = eval("(" + data + ")");
		return res;
	},

	require_new_mod: function(name) {
		this.waiting_to_load.push(load_conf(name));
	},
	
	load_conf: function(name) {
		return load_json(this.baseurl + name + ".json");
	},

	list_mods: function(name) {
		let mod_conf = this.load_conf(name);
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
		
		if (this.loaded_mods.indexOf(mod_conf.name) != -1) { 
			this.waiting_to_load.push(mod_conf);
			
			this.mod_name_map.set(mod_conf.name, ++this.mod_cnt);
			this.mod_id_map[this.mod_cnt] = mod_conf.name;
		}
		
		return true;
	},
	
	init_dependence_graph: function() {
		let res = new Array();
		
		for (let i = 0; i < this.waiting_to_load.length; ++i) {
			let deps = this.waiting_to_load[i].depandence;
			if (deps == undefined || deps.length == 0) continue;
			for (let j = 0; j < deps.length; ++j) {
				let x = deps[j];
				if (typeof(x) != "string") {
					console.warn("Type error when calculating Module " + this.waiting_to_load[i].name + " dependences");
					continue;
				}
				
				res[i].push(this.mod_name_map.get(x));
			}
		}
		
		return res;
	},
	
	load_script: function(mod_conf) {
		if (this.loaded_mods.indexOf(mod_conf.name) != -1) {
			console.warn("Module " + mod_conf.name + " already loaded.")
		}
		
		let tag = $("<script></script>");
		tag.attr("src", mod_conf.path);
		$("#load_static").append(tag);
		
		this.loaded_mods.push(mod_conf.name);
	},
	
	topu_sort: function() {
		this.waiting_to_load = array_unique(this.waiting_to_load);
		let G = this.init_dependence_graph();
		this.depandence_graph = G;
		
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
		
		this.waiting_to_load = res;
		return res;
	},
	
	init_webscripts: function() {
		this.loaded_mods.push("jquery");
		this.load_script(this.load_conf("queueJS"));
		
		let ori = this.waiting_to_load.concat();
		waiting_to_load = [];
		for (lei i = 0; i < ori.length; ++i) {
			if (!this.list_mods(ori[i].name)) {
				console.error(ori[i].name + "Failed.");
				continue;
			}
		}
		
		let ss = this.topu_sort();
		for (let i = 0; i < ss.length; ++i) {
			this.load_script(this.load_conf(this.mod_id_map[ss[i]]));
		}
	}
};