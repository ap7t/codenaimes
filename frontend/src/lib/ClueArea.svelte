<script>
	import { io } from "socket.io-client";
	import { page } from "$app/stores";
	import { fade } from "svelte/transition";

	let clue;
	let clues = [];

	let gameId = $page.params.id;

	const socket = io("http://localhost:5000");

	socket.on("connect", function () {
		socket.emit("join", gameId);
	});

	socket.on("send-clue", function (clue) {
		clues = [...clues, clue];
		console.log(clues);
	});
</script>

<div class="border-2">
	<h4>Clues from Spymaster</h4>
	<ul id="clues" class="border-2 border-black-700">
		{#each clues as clue}
			<li in:fade class="list-none">{clue}</li>
		{/each}
	</ul>
</div>
