# Webimport folder

Here we keep our js **dependency** config

## How to modify

every json look like this:

`<MODULE NAME>.json`
```js
{
	"name": "<MODULE NAME>",
	"path": "<PATH TO THE MODULE>",
	"dependence": ["<DEPENDENCE MODULE A>", "<DEPENDENCE MODULE B>"], // optional
	"description": "<DESCRIPTION OF THE MODULE>" // optional
}
```

A example(`jquery.json`):

```js
{
	"name": "jquery",
	"path": "/static/js/jquery.min.js",
	"description": "jquery v3.5.1 compressed production"
}
```