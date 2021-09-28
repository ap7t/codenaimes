<script>
	import { page } from "$app/stores";
	import { io } from "socket.io-client";

	let clue;
	let gameId = $page.params.id;

	const socket = io("http://localhost:5000");

	const onInput = (event) => {
		console.log("func called");
		if (event.key !== "Enter") return;
		let data = { clue: clue, gameId: gameId };
		socket.emit("send-clue", data);
		clue = "";
	};
</script>

<div class="mx-4">
	<input
		class="round-lg"
		type="text"
		placeholder="Send clues"
		bind:value={clue}
		on:keydown={onInput}
	/>
</div>
