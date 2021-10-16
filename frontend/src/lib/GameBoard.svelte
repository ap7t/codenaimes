<script lang="ts">
	import AgentCard from "./AgentCard.svelte";
	import { page } from "$app/stores";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import { socket } from "../socket.js";
	import Button, { Label } from "@smui/button";
	import { state, guesses } from "../stores";
	import LayoutGrid, { Cell, InnerGrid } from "@smui/layout-grid";
	import GameStats from "./GameStats.svelte";

	export let spymaster = false;

	let data;
	let redCount;
	let blueCount;
	let agents = [];
	let solution = [];
	let gameId = $page.params.id;
	let open = false;
	let assassinated = false;
	let clicked;
	let winner;
	let winningMsg;
	let guessesLeft;

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
		console.log("just got new game");
		// console.log(game.current_clue);
		console.log(game);
		$state = game;
	});

	$: if (redCount == 0) {
		winner = "Red";
		winningMsg = "Well done red team. Play again?";
		open = true;
	}

	$: if (blueCount == 0) {
		winner = "Blue";
		winningMsg = "Well done blue team. Play again?";
		open = true;
	}

	$: if (assassinated) {
		winner = "Assassin";
		winningMsg = "TODO: whatever team picked this lost";
		open = true;
	}
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
{$state == {}}
{$state}
<div class="agentsGrid">
	{#if spymaster && $state != {}}
		{#each $state.solution as sol, i}
			<AgentCard name={sol[0]} colour={sol[1]} num={i} spymaster={true} />
		{/each}
	{:else}
		{#each $state.board as agent, i}
			<AgentCard name={agent[0]} colour={agent[1]} num={i} spymaster={false} />
		{/each}
	{/if}

	<!-- {state.board} -->
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
