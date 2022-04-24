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
	import GameBoard from "$lib/GameBoard.svelte";
	import Card, { PrimaryAction } from "@smui/card";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";

	let open = false;
	let winner;
	let winningMsg;
	let clues = [];
	let words = [];
	let count = 0;
	let clueInd = 1; // start at one because we already have the first clue
	let gameInd = 0;
	let classString = "agentCard";
	// let count = 4;

	$: if (clueInd > 4 && gameInd === 5) {
		socket.emit("save-evaluation");
		console.log("saving");
		open = true;
	}

	$: if (clueInd === 4 && gameInd < 5) {
		gameInd++;
		let data = { ind: gameInd };
		socket.emit("evaluation-next-game", data);
	}

	onMount(() => {
		let data = { gameInd: gameInd, clueInd: clueInd };
		socket.emit("evaluation", data);
	});

	socket.on("send-evaluation", function (data) {
		clues = data.clues;
		words = data.words;
	});

	socket.on("evaluation-next-game", function (data) {
		clueInd = 1;
		$state = data.game;
		words = data.words;
		clues = data.clues;
	});

	function makeVote(name) {
		if (clueInd < 5) {
			// use index 5 to know we are going to the next game
			let data = { vote: name, clueInd: clueInd, gameInd: gameInd };
			socket.emit("make-vote", data);
			clueInd++;
		}
	}
</script>

<!-- <svelte:window on:load={handleLoad} /> -->
<div>
	<div class="clue">
		Words
		<strong>{words[0]}</strong>
		and
		<strong>{words[1]}</strong>
	</div>
	<!-- TODO: why are colours breaking on a new game??? -->
	<div class="agentsGrid">
		{#if $state != {}}
			{#each Object.entries($state.solution) as [name, col], _}
				<!-- {name}
				{col} -->
				<AgentCard {name} colour={col} spymaster={true} ai={false} toast={false} />
			{/each}
		{/if}
	</div>
</div>
<br />
<br />
<h2>Which was the <strong>better</strong> clue?</h2>
<div class="vote">
	<Card>
		<PrimaryAction on:click={() => makeVote(clues[0])} padded class={classString}>
			<span> {clues[0]}</span>
		</PrimaryAction>
	</Card>
	<Card>
		<PrimaryAction on:click={() => makeVote(clues[1])} padded class={classString}>
			<span> {clues[1]}</span>
		</PrimaryAction>
	</Card>
</div>

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
		margin-bottom: 2em;
		align-items: center;
	}

	.vote {
		display: flex;
		width: 50%;
		align-items: center;
		justify-content: space-around;
		margin-top: 2em;
	}
</style>
