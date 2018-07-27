const fs = require("fs");
const path = require("path");

let hearthstoneKeys = [];
const hearthstoneDir = path.resolve(__dirname, "locale", "en", "hearthstone");
const filenames = fs.readdirSync(hearthstoneDir);
for (const filename of filenames) {
	const file = fs.readFileSync(path.resolve(hearthstoneDir, filename));
	const contents = JSON.parse(file);
	hearthstoneKeys = hearthstoneKeys.concat(Object.keys(contents));
}

module.exports = {
	options: {
		// use strings as keys
		nsSeparator: false,
		keySeparator: false,
		// settings
		defaultNs: "frontend",
		lngs: ["en"],
		resource: {
			loadPath: "{{lng}}/{{ns}}.json",
			savePath: "{{lng}}/{{ns}}.json",
		},
		func: false,
		trans: false,
		defaultValue: (language, namespace, key) => key,
	},
	transform(file, enc, done) {
		const parser = this.parser;
		const content = fs.readFileSync(file.path, enc);
		const ext = path.extname(file.path);

		parser.parseFuncFromString(
			content,
			{
				list: ["t"],
			},
			(key, options) => {
				if (hearthstoneKeys.indexOf(key) !== -1) {
					return;
				}
				parser.set(key, options);
			},
		);

		parser.parseTransFromString(
			content,
			{
				component: "Trans",
				i18nKey: false,
			},
			(key, options) => {
				parser.set(options.defaultValue, options);
			},
		);

		done();
	},
};
