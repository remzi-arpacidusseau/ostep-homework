#! /usr/bin/env node

const values = [];
for (let i = 0; i < 10; i++) {
	// Value around which to cluster.
	const mean = Math.floor(Math.random() * i) + 1;
	// Number of values in this cluster, between 1 and 5 inclusive.
	const randCluster = Math.floor(Math.random() * 5) + 1;
	for (let j = 0; j < randCluster; j++) {
		// Random offset: -1, 0, or 1;
		const offset =  Math.floor(Math.random() * 3) - 1;
		values.push(mean + offset);
	}
}
console.log(values.join(','));
return 0;
