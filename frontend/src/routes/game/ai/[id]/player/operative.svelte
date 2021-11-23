<script>
	import PlayArea from "$lib/PlayArea.svelte";
	import GameStats from "$lib/GameStats.svelte";
</script>

<PlayArea ai={true}/>
<style>
	.general {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
