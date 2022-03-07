<script lang="ts">
	import AgentCard from "../../lib/AgentCard.svelte";
	import { socket } from "../../socket.js";
	import { expId, state } from "../../stores.js";
	import { onMount } from "svelte";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import CircularProgress from "@smui/circular-progress";
	import Button, { Label } from "@smui/button";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import { goto } from "$app/navigation";
	import Snackbar, { SnackbarComponentDev } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";

	export let spymaster = false;
	export let ai = false;

	let open = false;
	let re = /^\w+$/;
	let clue = "";
	let word1 = "";
	let word2 = "";
	// let count = 0;
	let count = 3;
	let generating_clue = true;

	$: if (count === 4) {
		console.log("count is 4");
		socket.emit("save-experiment", $expId);
		open = true;
	}

	onMount(() => {
		socket.emit("experiment-spymaster", $expId);
	});

	socket.on("send-experiment-spymaster", function (data) {
		console.log(data);

		word1 = data.word1;
		word2 = data.word2;
		generating_clue = false;
	});

	function sendAnswers() {
		// TODO: make sure that required are actually required
		let match = re.exec(clue);
		if (match) {
			if (count < 4) {
				let data = { expId: $expId, clue: clue };
				socket.emit("send-answer-spymaster", data);
				count++;
				clue = "";
				generating_clue = true;
			}
		} else {
			oneWordSnackbar.open();
			return;
		}
	}

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		sendAnswers();
	};

	let oneWordSnackbar: SnackbarComponentDev;
</script>

<!-- <svelte:window on:load={handleLoad} /> -->
<div class="container">
	<div class="clue">
		Words: {#if generating_clue}
			<CircularProgress
				class="my-four-colors"
				style="height: 32px; width: 32px;"
				indeterminate
				fourColor
			/>
		{:else}
			<strong>{word1}</strong>
			and
			<strong>{word2}</strong>
		{/if}
	</div>
	<div class="agentsGrid">
		{#if $state != {}}
			{#each Object.entries($state.solution) as [name, col], _}
				<AgentCard {name} colour={col} spymaster={true} ai={false} toast={false} />
			{/each}
		{/if}
	</div>
	<div class="answers">
		<Textfield id="clueInput" required={true} bind:value={clue} label="Clue">
			<HelperText slot="helper">Please enter your clue</HelperText>
		</Textfield>
		{#if clue !== ""}
			<br />
			<Button variant="raised" on:click={sendAnswers} on:keydown={onInput}>
				<Label>Submit</Label>
			</Button>
		{/if}
	</div>
</div>

<Snackbar bind:this={oneWordSnackbar} timeoutMs={4000}>
	<Label>Your clue can only be one word!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">Thank you</Title>
	<Content id="simple-content"
		>Your responses have been saved, thank you for taking the time to do this experiment!</Content
	>
	<Actions>
		<Button on:click={() => goto("/")}>
			<Label>No problem!</Label>
		</Button>
	</Actions>
</Dialog>

<style>
	.agentsGrid {
		/* Activate grid layout */
		display: grid;

		/* Create 5 columns, each 1 "fractional unit" wide */
		grid-template-columns: repeat(5, 1fr);

		/* Create 5 rows, each 1 "fractional unit" high */
		grid-template-rows: repeat(5, 1fr);

		/* Add a 10px gap between columns and rows */
		grid-gap: 10px;

		width: 100%;
		min-width: 20%;
	}

	/* .answers { */
	/* align-content: center; */
	/* } */

	.container {
		width: 50%;
		display: flex;
		flex-direction: column;
		align-items: center;
		row-gap: 2em;
	}

	.clue {
		font-size: xx-large;
	}
</style>
