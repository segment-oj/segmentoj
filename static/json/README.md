# Json Folder

Here we keep front-end config files using json.
You can request files `/static/json/xxx.json`

**Example:**

```js
var get_conf = function() {
	var conf;
	var raw = $.get("/static/json/xxx.json");
	conf = eval("({data})".format({data: raw}));
	return conf;
}
```