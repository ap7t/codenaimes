<script>
	import { socket } from "../socket.js";
	import { page } from "$app/stores";
	import { fade } from "svelte/transition";

	let clue;
	let clues = [];

	let gameId = $page.params.id;

	socket.on("connect", function () {
		socket.emit("join", gameId);
	});

	socket.on("send-clue", function (clue) {
		clues = [...clues, clue];
		console.log(clues);
	});
</script>

<div class="border-2">
	<div>
		<h4>Clues from Spymaster</h4>
	</div>
	<ul id="clues" class="border-2 border-black-700">
		{#each clues as clue}
			<li in:fade class="list-none">{clue}</li>
		{/each}
	</ul>
</div>
