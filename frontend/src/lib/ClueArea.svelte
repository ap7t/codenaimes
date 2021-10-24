<script>
	import { socket } from "../socket.js";
	import { page } from "$app/stores";
	import { fade } from "svelte/transition";
	import { beforeUpdate, afterUpdate } from "svelte";

	let clue;
	let clues = [];
	let div;
	let autoscroll;

	let gameId = $page.params.id;

	beforeUpdate(() => {
		autoscroll = div && div.offsetHeight + div.scrollTop > div.scrollHeight - 20;
	});

	afterUpdate(() => {
		if (autoscroll) div.scrollTo(0, div.scrollHeight);
	});

	socket.on("send-clue", function (clue) {
		clues = [...clues, clue];
		let objDiv = document.getElementById("clues");
		objDiv.scrollTop = objDiv.scrollHeight;
		console.log(clues);
	});
</script>

<div class="scrollHider">
	<h1>Clues</h1>
	<div id="clues" bind:this={div}>
		{#each clues as clue, i}
			<p in:fade class={clue.team.toLowerCase()}>{clue.clue}</p>
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
