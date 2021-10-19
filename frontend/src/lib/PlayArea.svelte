<script>
	import ClueInput from "$lib/ClueInput.svelte";
	import ClueArea from "$lib/ClueArea.svelte";
	import ChatArea from "$lib/ChatArea.svelte";
	import GameBoard from "$lib/GameBoard.svelte";

	export let spymaster = false;
	import GameStats from "./GameStats.svelte";
</script>

<div class="container">
	<div class="side">
		<ClueArea />
		<!-- {#if spymaster} -->
		<ClueInput {spymaster} />
		<!-- {/if} -->
	</div>
	<div class="game">
		<GameStats />
		<GameBoard {spymaster} />
	</div>
	<div class="side">
		<ChatArea {spymaster} />
	</div>
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
		justify-content: space-evenly;
		width: 100%;
		/* align-items: center; */
	}

	.side {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-width: 10%;
	}

	.game {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
	}
</style>
