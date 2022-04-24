<script lang="ts">
	import AgentCard from "../../lib/AgentCard.svelte";
	import { socket } from "../../socket.js";
	import { expId, state } from "../../stores.js";
	import { onMount } from "svelte";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import CircularProgress from "@smui/circular-progress";
	import Button, { Label } from "@smui/button";
	import { goto } from "$app/navigation";

	export let spymaster = false;
	export let ai = false;

	let open = false;
	let winner;
	let winningMsg;
	let word1 = "";
	let word2 = "";
	let word3 = "";
	let word4 = "";
	let clue = "test";
	let count = 0;
	// let count = 4;

	$: if (count === 4) {
		socket.emit("experiment-create-spymaster", $expId);
		console.log("creating spymaster");
	}

	let generating_clue = true;

	onMount(() => {
		socket.emit("experiment", $expId);
	});

	socket.on("send-experiment", function (data) {
		clue = data;
		generating_clue = false;
	});

	socket.on("before-experiment-join-spymaster", function (game) {
		$state = game;
		goto("/experiment/spymaster");
	});

	function sendAnswers() {
		// TODO: make sure that required are actually required
		let data = { expId: $expId, word1: word1, word2: word2, word3: word3, word4: word4 };
		socket.emit("send-answer", data);
		word1 = "";
		word2 = "";
		word3 = "";
		word4 = "";
		generating_clue = true;
		generating_clue = true;
		count++;
	}
</script>

<!-- <svelte:window on:load={handleLoad} /> -->
<div class="container">
	<div class="clue">
		<!-- Clue: {#if generating_clue}
			<CircularProgress
				class="my-four-colors"
				style="height: 32px; width: 32px;"
				indeterminate
				fourColor
			/>
		{:else}
			<strong>{clue}</strong>
		{/if} -->
		Clue: <strong>teeth</strong>
	</div>
	<div class="agentsGrid">
		{#if $state != {}}
			{#each Object.entries($state.board) as [name, col], _}
				<AgentCard {name} colour={false} spymaster={false} ai={false} toast={false} />
			{/each}
		{/if}
	</div>
	<div class="answers">
		<Textfield id="word1Input" required={true} bind:value={word1} label="Word 1">
			<HelperText slot="helper">Please enter your first guess</HelperText>
		</Textfield>
		<Textfield id="word2Input" required={true} bind:value={word2} label="Word 2">
			<HelperText slot="helper">Please enter your second guess</HelperText>
		</Textfield>
		<Textfield id="word3Input" required={false} bind:value={word3} label="Word 3">
			<HelperText slot="helper">Please enter your third guess</HelperText>
		</Textfield>
		<Textfield id="word4Input" required={false} bind:value={word4} label="Word 4">
			<HelperText slot="helper">Please enter your fourth guess</HelperText>
		</Textfield>
		{#if word1 !== "" && word2 !== ""}
			<br />
			<Button variant="raised" on:click={sendAnswers}>
				<Label>Submit</Label>
			</Button>
		{/if}
	</div>
</div>

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
