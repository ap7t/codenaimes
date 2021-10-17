<script lang="ts">
	import AgentCard from "./AgentCard.svelte";
	import { page } from "$app/stores";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import { socket } from "../socket.js";
	import Button, { Label } from "@smui/button";
	import { state } from "../stores";
	import LayoutGrid, { Cell, InnerGrid } from "@smui/layout-grid";
	import GameStats from "./GameStats.svelte";

	export let spymaster = false;

	let open = false;
	let winner;
	let winningMsg;
	$: whoLost = $state.round % 2 != 0 ? "Red" : "Blue";

	// let data;
	// let redCount;
	// let blueCount;
	// let agents = [];
	// let solution = [];
	// let gameId = $page.params.id;
	// let assassinated = false;
	// let clicked;
	// let guessesLeft;

	// state.subscribe((stateData) => {
	// 	if (Object.keys(stateData).length === 0) {
	// 		return;
	// 	}
	// 	data = stateData;
	// 	// console.log(data);
	// 	// console.log("-- agents --");
	// 	// console.log(data.board);
	// 	agents = Object.entries(data.board);
	// 	solution = Object.entries(data.solution);
	// 	// console.log(agents);
	// 	redCount = data.red_agents;
	// 	blueCount = data.blue_agents;
	// 	assassinated = data.assassinated;
	// 	guessesLeft = data.guesses;
	// });

	socket.on("send-state", function (game) {
		console.log("just got new state");
		// console.log(game.current_clue);
		console.log(game);
		$state = game;
	});

	$: if ($state.red_agents == 0) {
		winner = "Red";
		winningMsg = "Well done red team. Play again?";
		open = true;
	}

	$: if ($state.blue_agents == 0) {
		winner = "Blue";
		winningMsg = "Well done blue team. Play again?";
		open = true;
	}

	$: if ($state.assassinated) {
		winner = "Assassin";
		winningMsg = `${whoLost} team found the assassin so they lose! Play again?`;
		open = true;
	}
	console.log("state inside gameboard->", $state);
</script>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">{winner} Won</Title>
	<Content id="simple-content">{winningMsg}</Content>
	<Actions>
		<Button on:click={() => (clicked = "No")}>
			<Label>No</Label>
		</Button>
		<Button on:click={() => (clicked = "Yes")}>
			<Label>Yes</Label>
		</Button>
	</Actions>
</Dialog>

<GameStats />
<div class="agentsGrid">
	{#if $state != {}}
		{#if spymaster}
			{#each Object.entries($state.solution) as [name, col], i}
				<AgentCard {name} colour={col} num={i} spymaster={true} />
			{/each}
		{:else}
			{#each Object.entries($state.board) as [name, col], i}
				<AgentCard {name} colour={col} num={i} spymaster={false} />
			{/each}
		{/if}
	{/if}
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
	}
</style>
