import preprocess from "svelte-preprocess";
/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte'
	},

    vite: {
		resolve: {
			alias: {
				"socket.io-client": "socket.io-client/dist/socket.io.js"
			}
		}
	},

    preprocess: [preprocess({
        postcss: true
    })]
};

export default config;
