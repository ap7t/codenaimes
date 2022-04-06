<script lang="ts">
	import { page } from "$app/stores";
	import { socket } from "../socket.js";
	import { team, state } from "../stores";
	import Snackbar, { Label, SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Icon from "@smui/textfield/icon";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import Button from "@smui/button";

	let re = /^\w+ \d ?$/;
	let prevClue = "";
	let clue = "";
	let guesses;
	let gameId = $page.params.id;
	let open = false;

	export let spymaster = false;

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
		// validate clue
		let match = re.exec(clue);
		if (match) {
			guesses = parseInt(clue.split(" ")[1]);
			let data = { clue: clue, guesses: guesses, gameId: gameId, team: $team };
			socket.emit("send-clue", data);
			prevClue = clue;
			clue = "";
		} else {
			open = true;
		}
	};
</script>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">Invalid Clue</Title>
	<Content id="simple-content"
		>Your clue must be in the form "word number": example 4<br />Please try again!
	</Content>
	<Actions>
		<Button>
			<Label>Okay</Label>
		</Button>
	</Actions>
</Dialog>

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
{#if spymaster}
	<Textfield variant="outlined" bind:value={clue} label="Clue" on:keydown={onInput}>
		<Icon class="material-icons" slot="leadingIcon">forward_to_inbox</Icon>
		<!-- <HelperText slot="helper">Send a clue in the form &lt;word number&gt;</HelperText> -->
	</Textfield>
{/if}
