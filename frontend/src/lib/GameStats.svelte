<script lang="ts">
	import { team, state } from "../stores";
	import { page } from "$app/stores";
	import GameBoard from "./GameBoard.svelte";
	import LinkGame from "./LinkGame.svelte";
	import { socket } from "../socket.js";
	import Button, { Label, Icon } from "@smui/button";

	$: whosTurn = $state.round % 2 == 0 ? "red" : "blue";

	$: canMove =
		($team === "Red" && $state.round % 2 == 0) || ($team === "Blue" && $state.round % 2 != 0);

	export let spymaster = false;
</script>

<!-- guesses left: {guessesLeft} -->
<div class="container">
	<div class="round">
		{#if whosTurn == "red"}
			<span class="red">ROUND {$state.round + 1}</span>
		{:else}
			<span class="blue">ROUND {$state.round + 1}</span>
		{/if}
	</div>
	<div class="middleBar">
		<div>
			<Icon class="material-icons">sports_score</Icon>
			<span class="red">{$state.red_agents}</span> -
			<span class="blue">{$state.blue_agents}</span>
		</div>

		<LinkGame />
	</div>
	<div class="guesses">
		{#if $state.guesses > 0}
			<Icon class="material-icons">contact_support</Icon>
			{$state.guesses} guesses left
		{/if}
	</div>
	<div class="endRound">
		{#if $state.guesses > 0 && canMove && !spymaster}
			<Button
				class={whosTurn}
				variant="outlined"
				on:click={() => socket.emit("end_round", $state.gameId)}
			>
				<Icon class="material-icons">block</Icon>
				<Label>End round</Label>
			</Button>
		{/if}
	</div>
</div>

<style>
	* {
		font-size: x-large;
	}

	.container {
		display: flex;
		flex-direction: column;
		width: 100%;
	}

	.middleBar {
		height: 100%;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	.guesses {
		display: flex;
		flex-direction: row;
		justify-content: left;
	}

	.round {
		display: flex;
		justify-content: center;
		width: 100%;
	}

	.red {
		color: rgb(199, 45, 45);
	}

	.blue {
		color: #2767ff;
	}

	.endRound {
		margin-top: 0.5rem;
	}
</style>
