<script>
	import { io } from "socket.io-client";
	import { fly } from "svelte/transition";
	import { page } from "$app/stores";

	let message;
	let messages = [];
	let gameLink;
	let gameId = $page.params.id;

	const socket = io("http://localhost:5000");

	socket.on("connect", function () {
		// TODO: maybe keep a record of the messages and show when joined but thats a future improvement
		socket.emit("join", gameId);
	});

	socket.on("message", function (message) {
		console.log("received message");
		console.log(messages);
		messages = [...messages, message];
	});

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		let data = { message: message, gameId: gameId };
		socket.emit("message", data);
		// messages = [...messages, message];
		message = "";
	};

	function debug() {
		console.log("pressed debug");
		messages = [...messages, "debug"];
		console.log(messages);
	}
</script>

<div>
	<ul id="messages">
		{#each messages as message}
			<li in:fly={{ x: -200, duration: 1000 }}>{message}</li>
		{/each}
	</ul>
	<input type="text" placeholder="Your message" bind:value={message} on:keydown={onInput} />
	<button on:click|preventDefault={debug} />
</div>

<style>
	li {
		list-style-type: none;
	}

	ul {
		height: 400px;
		width: 200px;
		border: 1px black solid;
	}

	input {
		width: 200px;
	}

	@media (min-width: 480px) {
		h1 {
			font-size: 4em;
		}
	}
</style>
