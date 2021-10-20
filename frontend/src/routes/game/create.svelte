<script>
	import { fade } from "svelte/transition";
	import Button, { Label } from "@smui/button";
	import { socket } from "../../socket.js";
	import { goto } from "$app/navigation";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";

	let gameId = "dev";

	function createGame() {
		socket.emit("create_game", gameId);
		goto(`/game/${gameId}/join`);
	}
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<div in:fade>
	<h3>Create a Game ID</h3>
	<Textfield id="gameId" variant="outlined" required={true} bind:value={gameId} label="Game ID">
		<HelperText slot="helper"
			>Enter a word that will be used as the Game ID so your friends can join</HelperText
		>
	</Textfield>

	<Button on:click={createGame}>
		<Label>Create game</Label>
	</Button>
</div>

<style>
	div {
		margin-top: 50px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
	}
</style>
