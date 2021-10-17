<script>
	import { socket } from "../socket.js";
	import { page } from "$app/stores";
	import { fade } from "svelte/transition";

	let clue;
	let clues = [];

	let gameId = $page.params.id;

	// socket.on("connect", function () {
	// 	socket.emit("join", gameId);
	// });

	socket.on("send-clue", function (clue) {
		clues = [...clues, clue];
		let objDiv = document.getElementById("clues");
		objDiv.scrollTop = objDiv.scrollHeight;
	});
</script>

<div class="scrollHider">
	<h1>Clues</h1>
	<div id="clues">
		{#each clues as clue, i}
			<p class={i % 2 == 0 ? "red" : "blue"}>{clue}</p>
		{/each}
	</div>
</div>

<style>
	.scrollHider {
		width: 100%;
		height: 200px;
		display: flex;
		flex-direction: column;
		align-items: center;
		overflow: hidden;
	}

	#clues {
		width: 100%;
		height: 100%;
		overflow-y: scroll;
		padding-right: 17px; /* Increase/decrease this value for cross-browser compatibility */
		box-sizing: content-box; /* So the width will be 100% + 17px */
		margin-left: auto;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	p {
		border: 2px solid #dedede;
		background-color: #f1f1f1;
		border-radius: 5px;
		padding: 10px;
		margin: 10px 0;
		text-transform: uppercase;
		/* width: auto; */
	}

	.red {
		color: rgb(199, 45, 45);
	}

	.blue {
		color: #2767ff;
	}
</style>
