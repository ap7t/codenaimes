<script lang="ts">
	import { state, guesses } from "../stores";
	import { page } from "$app/stores";
	import GameBoard from "./GameBoard.svelte";
	import LinkGame from "./LinkGame.svelte";
	import { Icon } from "@smui/button";

	$: whosTurn = $state.round % 2 == 0 ? "red" : "blue";
</script>

<!-- guesses left: {guessesLeft} -->
<div class="container">
	<div class="agentsRemaining">
		<Icon class="material-icons">sports_score</Icon>
		<span class="red">{$state.red_agents}</span> - <span class="blue">{$state.blue_agents}</span>
	</div>
	<div class="container">
		{whosTurn}
		{#if whosTurn == "red"}
			<span class="red">ROUND {$state.round}</span>
		{:else}
			<span class="blue">ROUND {$state.round}</span>
		{/if}
		<!-- {#if $state.guesses > 0} -->
		{#if $state.guesses > 0}
			<Icon class="material-icons">person_search</Icon>
			{$state.guesses} guesses left
		{/if}
	</div>
	<div><LinkGame /></div>
</div>

<style>
	* {
		font-size: x-large;
	}

	.container {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	.red {
		color: rgb(199, 45, 45);
	}

	.blue {
		color: #2767ff;
	}
</style>
