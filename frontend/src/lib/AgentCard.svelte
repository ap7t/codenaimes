<script lang="ts">
	import { page } from "$app/stores";
	import { socket } from "../socket.js";
	import { team, state } from "../stores.js";
	import Snackbar, { Actions, SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";
	import Card, { Content, PrimaryAction, ActionButtons, ActionIcons } from "@smui/card";
	import Button, { Label } from "@smui/button";

	export let colour;
	export let spymaster;
	export let name;
	let msg;

	let classString = "agentCard";

	let gameId = $page.params.id;

	$: {
		switch (colour) {
			case "R":
				classString += " redAgent";
				break;
			case "B":
				classString += " blueAgent";
				break;
			case "O":
				classString += " civilian";
				break;
			case "X":
				classString += " assassin";
				break;
		}
	}

	let notYourTurnSnackbar: SnackbarComponentDev;
	let noClueSnackbar: SnackbarComponentDev;
	let yourSpymasterSnackbar: SnackbarComponentDev;
	let wrongCardSnackbar: SnackbarComponentDev;
	$: canMove =
		($team === "Red" && $state.round % 2 == 0) || ($team === "Blue" && $state.round % 2 != 0);
	function makeMove(card) {
		if (!canMove) {
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
			let data = { card: card, gameId: gameId, correct: false };
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
			let data = { card: card, gameId: gameId, correct: false };
			socket.emit("make_move", data);
		} else {
			let data = { card: card, gameId: gameId, correct: true };
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

<Card>
	<PrimaryAction
		on:click={() => makeMove({ name })}
		padded
		class={spymaster && $state.board[name] ? classString + " found" : classString}
	>
		{name}
	</PrimaryAction>
</Card>
