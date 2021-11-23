<script lang="ts">
	import { socket } from "../socket.js";
	import { page } from "$app/stores";
	import { fade } from "svelte/transition";
	import { beforeUpdate, afterUpdate } from "svelte";
	import Button, { Label } from "@smui/button";
	import { state, team } from "../stores";
	import Snackbar, { Actions, SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";

	let clue;
	// let clues = ["test 4", "test 4", "test 4", "test 4"];
	let clues = [];
	let div;
	let autoscroll;
	let prevClue = "";
	let lastGo = "red";

	let gameId = $page.params.id;
	$: whosTurn = $state.round % 2 == 0 ? "red" : "blue";
	$: canMove =
		($team === "Red" && $state.round % 2 == 0) || ($team === "Blue" && $state.round % 2 != 0);

	beforeUpdate(() => {
		autoscroll = div && div.offsetHeight + div.scrollTop > div.scrollHeight - 20;
	});

	afterUpdate(() => {
		if (autoscroll) div.scrollTo(0, div.scrollHeight);
	});

	socket.on("send-clue", function (clue) {
		clues = [...clues, clue];
		prevClue = clue.clue;
		lastGo = whosTurn;
		let objDiv = document.getElementById("clues");
		objDiv.scrollTop = objDiv.scrollHeight;
	});

	function requestClue() {
		console.log(prevClue, $state.current_clue);
		console.log(lastGo, whosTurn);
		if (prevClue === $state.current_clue && lastGo =	= whosTurn) {
			alreadyRequestedClueSnackbar.open();
			return;
		}
		console.log("reqeusting");
		let data = { gameId: gameId, team: whosTurn };
		socket.emit("request-clue", data);
	}
	let alreadyRequestedClueSnackbar: SnackbarComponentDev;
</script>

<div class="scrollHider">
	<h1>Clues</h1>
	<div>
		{#if canMove}
			<Button on:click={requestClue}>
				<Label>Request clue</Label>
			</Button>
		{/if}
	</div>
	<div id="clues" bind:this={div}>
		{#each clues as clue, i}
			<p in:fade class={clue.team.toLowerCase()}>{clue.clue}</p>
		{/each}
	</div>
</div>

<Snackbar bind:this={alreadyRequestedClueSnackbar} timeoutMs={4000}>
	<Label>A clue has already been requested this round!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<style>
	.scrollHider {
		width: 100%;
		height: 400px;
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
