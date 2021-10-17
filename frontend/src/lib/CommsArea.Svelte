<script>
	import ClueInput from "$lib/ClueInput.svelte";
	import ClueArea from "$lib/ClueArea.svelte";
	import ChatArea from "$lib/ChatArea.svelte";

	export let spymaster = false;
</script>

<div class="container">
	<div class="clues">
		<ClueArea />
		{#if spymaster}
			<ClueInput />
		{/if}
	</div>
	<div class="chat">
		<ChatArea />
	</div>
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		/* align-items: center; */
	}

	.clues {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
