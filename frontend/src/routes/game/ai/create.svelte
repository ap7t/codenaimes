<script lang="ts">
	import CircularProgress from "@smui/circular-progress";
	import { fade } from "svelte/transition";
	import Button, { Label } from "@smui/button";
	import { socket } from "../../../socket.js";
	import { goto } from "$app/navigation";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";

	let gameId = "dev";
	let open = false;
	let visible = false;

	function createGame() {
		socket.emit("ai_create_game", gameId);
		visible = true;
	}

	socket.on("ai_cant_create", function () {
		open = true;
	});

	socket.on("ai_create_game", function () {
		console.log("got told a game was made");
		goto(`/game/ai/${gameId}/join`);
	});
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">Game Already Exists</Title>
	<Content id="simple-content"
		>Looks like someone is already using that Game ID, please use a different one</Content
	>
	<Actions>
		<Button>
			<Label>Will do</Label>
		</Button>
	</Actions>
</Dialog>

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

{#if visible}
	<div style="display: flex; justify-content: center">
		<h1>Please wait while we create the AI spymaster</h1>
		<small>May take up to 2 minutes</small>
		<CircularProgress
			class="my-four-colors"
			style="height: 32px; width: 32px;"
			indeterminate
			fourColor
		/>
	</div>
{/if}

<style>
	div {
		margin-top: 50px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
	}
</style>
