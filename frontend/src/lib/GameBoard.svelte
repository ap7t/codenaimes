<script lang="ts">
	import AgentCard from "./AgentCard.svelte";
	import { page } from "$app/stores";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import { socket } from "../socket.js";
	import Button, { Label } from "@smui/button";
	import { state, guesses } from "../stores";
	import { onMount } from "svelte";

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

	// socket.on("join_game", function (game) {
	// 	state.set(game);
	// 	// console.log("should have got game");
	// 	agents = Object.entries(game.board);
	// 	solution = Object.entries(game.solution);
	// 	redCount = game.red_agents;
	// 	blueCount = game.blue_agents;
	// 	// console.log("=== agents from create game ===");
	// 	// console.log(agents);
	// });
	state.subscribe((stateData) => {
		if (Object.keys(stateData).length === 0) {
			return;
		}
		data = stateData;
		// console.log(data);
		// console.log("-- agents --");
		// console.log(data.board);
		agents = Object.entries(data.board);
		solution = Object.entries(data.solution);
		// console.log(agents);
		redCount = data.red_agents;
		blueCount = data.blue_agents;
		assassinated = data.assassinated;
		guessesLeft = data.guesses;
	});

	// socket.on("send-state", function (game) {
	// 	console.log("should have got new state");
	// 	// console.log(game);
	// 	$state = game;
	// 	const newAgents = Object.entries(game.board);
	// 	agents = [...agents, ["testing", "G"]];
	// 	agents = newAgents;
	// 	redCount = state.red_agents;
	// 	blueCount = state.blue_agents;
	// 	// console.log(agents);

	// 	// console.log(agents);
	// });
	socket.on("send-state", function (game) {
		// console.log("should have got new state");
		console.log("just got new game");
		console.log(game.current_clue);
		console.log(game);
		state.set(game);
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

	// guesses.subscribe((val) => {
	// 	guesses.set = val;
	// });
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
Do we even have a game state lol? {$state}
<br />
Game round {$state.round}
<br />
{$state.round % 2 == 0 ? "Red" : "Blue"} team's turn
<br />
guesses left: {guessesLeft}
<div>
	Red agents left: {redCount}
	<br />
	Blue agents left: {blueCount}
	<br />
	Assassinated {assassinated}
	<br />
	{#if guessesLeft > 0}
		Guesses remaining: {guessesLeft}
	{/if}
</div>
<div class="agentsGrid">
	{#if spymaster}
		{#each solution as sol, i}
			<AgentCard name={sol[0]} colour={sol[1]} num={i} spymaster={true} />
		{/each}
	{:else}
		{#each agents as agent, i}
			<AgentCard name={agent[0]} colour={agent[1]} num={i} spymaster={false} />
		{/each}
	{/if}

	<!-- {state.board} -->
</div>

<style>
	.agentsGrid {
		width: 600px;
		display: grid;
		grid-gap: 75px;
		grid-template-columns: repeat(5, 100px);
		grid-template-rows: repeat(5, 100px);
		grid-auto-flow: column;
	}
</style>
