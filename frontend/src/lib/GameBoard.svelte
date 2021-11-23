<script lang="ts">
	import AgentCard from "./AgentCard.svelte";
	import { page } from "$app/stores";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import { socket } from "../socket.js";
	import Button, { Label } from "@smui/button";
	import { state, username, team } from "../stores";
	import LayoutGrid, { Cell, InnerGrid } from "@smui/layout-grid";
	import GameStats from "./GameStats.svelte";
	import { onMount, onDestroy } from "svelte";

	export let spymaster = false;
	export let ai = false;

	let open = false;
	let winner;
	let winningMsg;
	$: whoLost = $state.round % 2 != 0 ? "Red" : "Blue";

	socket.on("send-state", function (game) {
		$state = game;
	});

	$: if ($state.red_agents == 0) {
		winner = "Red";
		winningMsg = "Well done red team. Play again?";
		open = true;
		socket.emit("game-over", $state.gameId);
	}

	$: if ($state.blue_agents == 0) {
		winner = "Blue";
		winningMsg = "Well done blue team. Play again?";
		open = true;
		socket.emit("game-over", $state.gameId);
	}

	$: if ($state.assassinated) {
		winner = "Assassin";
		winningMsg = `${whoLost} team found the assassin so they lose! Play again?`;
		open = true;
		socket.emit("game-over", $state.gameId);
	}

	onMount(() => {
		let data = {
			gameId: $state.gameId,
			name: $username,
			team: $team,
			role: spymaster ? "spymaster" : "operative"
		};
		if (ai) {
			socket.emit("ai_user_join", data);
		} else {
			socket.emit("user_join", data);
		}
	});

	onDestroy(() => {
		let data = {
			gameId: $state.gameId
		};
		socket.emit("user_leave", data);
	});
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

<!-- <svelte:window on:load={handleLoad} /> -->
<div class="agentsGrid">
	{#if $state != {}}
		{#if spymaster}
			{#each Object.entries($state.solution) as [name, col], _}
				<AgentCard {name} colour={col} spymaster={true} {ai} />
			{/each}
		{:else}
			{#each Object.entries($state.board) as [name, col], _}
				<AgentCard {name} colour={col} spymaster={false} {ai} />
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

		width: 100%;
		min-width: 20%;
	}
</style>
