<script lang="ts">
	import { page } from "$app/stores";
	import { socket } from "../socket.js";
	import { team, state } from "../stores";
	import Snackbar, { Actions, Label, SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Icon from "@smui/textfield/icon";

	let prevClue = ""; 
	let clue = "dev 4";
	let guesses;
	let gameId = $page.params.id;

	let notYourTurnSnackbar: SnackbarComponentDev;
	let alreadySentClueSnackbar: SnackbarComponentDev;

	$: canMove =
		($team === "Red" && $state.round % 2 == 0) || ($team === "Blue" && $state.round % 2 != 0);

	const onInput = (event) => {
		if (event.key !== "Enter") {
			return;
		} else if (!canMove) {
			notYourTurnSnackbar.open();
			return;
		} else if (prevClue === $state.current_clue) {
			alreadySentClueSnackbar.open();
			return;
		}
		guesses = parseInt(clue.split(" ")[1]);
		let data = { clue: clue, guesses: guesses, gameId: gameId };
		socket.emit("send-clue", data);
		prevClue = clue;
		clue = "";
	};
</script>

<Snackbar bind:this={alreadySentClueSnackbar} timeoutMs={4000}>
	<Label>You already sent your clue for this round!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Snackbar bind:this={notYourTurnSnackbar} timeoutMs={4000}>
	<Label>Hold your horses, it's not your turn!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Textfield variant="outlined" bind:value={clue} label="Clue" on:keydown={onInput}>
	<Icon class="material-icons" slot="leadingIcon">forward_to_inbox</Icon>
	<!-- <HelperText slot="helper">Send a clue in the form &lt;word number&gt;</HelperText> -->
</Textfield>
