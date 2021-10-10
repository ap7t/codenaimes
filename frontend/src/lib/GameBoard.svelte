<script lang="ts">
	import AgentCard from "./AgentCard.svelte";
	import { page } from "$app/stores";
	import { io } from "socket.io-client";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import Button, { Label } from "@smui/button";
	import { state } from "../stores";
	export let spymaster = false;

	let data;
	let redCount;
	let blueCount;
	let agents = [];
	let gameId = $page.params.id;
	let open = false;
	let assassinated = false;
	let clicked;
	let winner;
	let winningMsg;
	let i = 0;

	const socket = io("http://localhost:5000");
	socket.on("connect", function () {
		// TODO: maybe keep a record of the messages and show when joined but thats a future improvement
		// console.log("connected");
		socket.emit("join", gameId);
		socket.emit("create_game", gameId);
	});

	socket.on("create_game", function (game) {
		state.set(game);
		console.log("should have got game");
		agents = Object.entries(game.board);
		redCount = game.red_agents;
		blueCount = game.blue_agents;
		console.log("=== agents from create game ===");
		console.log(agents);
	});
	state.subscribe((stateData) => {
		if (Object.keys(stateData).length === 0) {
			return;
		}
		data = stateData;
		console.log("inside subscribe time: ", i);
		i++;
		console.log(data);
		console.log("-- agents --");
		console.log(data.board);
		agents = Object.entries(data.board);
		console.log(agents);
		redCount = data.red_agents;
		blueCount = data.blue_agents;
		assassinated = data.assassinated;
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
		console.log("should have got new state");
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
WHY IS THIS MISSING
<div>
	Red agents left: {redCount}
	<br />
	Blue agents left: {blueCount}
	<br />
	Assassinated {assassinated}
</div>
<div class="agentsGrid">
	<p>AGENTS: {agents}</p>
	{#each agents as agent, i}
		{#if spymaster}
			<AgentCard name={agent[0]} colour={agent[1]} num={i} />
		{:else}
			<AgentCard name={agent[0]} colour={agent[1]} num={i} />
		{/if}
	{/each}

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
