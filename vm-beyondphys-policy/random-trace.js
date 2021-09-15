#! /usr/bin/env node

if (process.argv.length < 4) {
	console.error('Usage: random-trace <count> <max>');
	process.exit(1);
}

const count = parseInt(process.argv[2]);
const max = parseInt(process.argv[3]);

const values = [];
for (let i = 0; i < count; i++) {
	const v = Math.floor(Math.random() * (max+1));
	values.push(v);
}
console.log(values.join(','));
return 0;
