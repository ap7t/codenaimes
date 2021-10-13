<script lang="ts">
	import { page } from "$app/stores";
	import { socket } from "../socket.js";
	import { team, state, guesses } from "../stores.js";
	import Snackbar, { Actions, Label, SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";

	export let name;
	export let num;
	export let colour;
	export let spymaster;
	let msg;

	let background;

	let gameId = $page.params.id;

	$: {
		switch (colour) {
			case "R":
				background = "red";
				break;
			case "B":
				background = "blue";
				break;
			case "O":
				background = "#FFD333";
				break;
			case "X":
				background = "purple";
				break;
		}
	}

	let notYourTurnSnackbar: SnackbarComponentDev;
	let noClueSnackbar: SnackbarComponentDev;
	let yourSpymasterSnackbar: SnackbarComponentDev;
	let wrongCardSnackbar: SnackbarComponentDev;

	console.log($state.solution);
	console.log($state.solution.glow);

	function makeMove(card) {
		let canMove =
			($team === "Red" && $state.round % 2 == 0) || ($team === "Blue" && $state.round % 2 != 0);
		if (!canMove) {
			// red starts and take one at a time for now
			console.log("its not your move");
			notYourTurnSnackbar.open();
		} else if (spymaster) {
			yourSpymasterSnackbar.open();
		} else if ($state.guesses === 0) {
			noClueSnackbar.open();
		} else if ($state.round % 2 == 0 && $state.solution[name] != "R") {
			switch ($state.solution[name]) {
				case "B":
					msg = "Oof, that's a blue agent, moving onto the next round";
					break;
				case "O":
					msg = "Oof, that's a civilian, moving onto the next round";
					break;
			}
			wrongCardSnackbar.open();
			let data = { card: null, gameId: gameId };
			socket.emit("make_move", data);
		} else if ($state.round % 2 != 0 && $state.solution[name] != "B") {
			switch ($state.solution[name]) {
				case "R":
					msg = "Oof, that's a red agent, moving onto the next round";
					break;
				case "O":
					msg = "Oof, that's a civilian, moving onto the next round";
					break;
			}
			wrongCardSnackbar.open();
			let data = { card: null, gameId: gameId };
			socket.emit("make_move", data);
		} else {
			console.log("making move");
			let data = { card: card, gameId: gameId };
			socket.emit("make_move", data);
		}
	}
</script>

<Snackbar bind:this={notYourTurnSnackbar} timeoutMs={4000}>
	<Label>Hold your horses, it's not your turn!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Snackbar bind:this={noClueSnackbar} timeoutMs={4000}>
	<Label>Don't get ahead of yourself, the spymaster hasn't sent their clue yet!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Snackbar bind:this={yourSpymasterSnackbar} timeoutMs={4000}>
	<Label>Your the spymaster, you can't guess!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Snackbar bind:this={wrongCardSnackbar} timeoutMs={4000}>
	<Label>{msg}</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<div id="card-{num}" style="background-color: {background}" on:click={() => makeMove({ name })}>
	{name}
	{$state.solution[name]}
</div>

<style>
	div {
		text-transform: uppercase;
		margin: 1em;
		padding-top: 2em;
		border: 1px solid black;
		height: 100px;
		width: 100px;
		text-align: center;
	}
</style>
