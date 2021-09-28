<script>
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import Clipboard from "svelte-clipboard";

	let gameLink;
	let gameId = $page.params.id;
	onMount(() => {
		gameLink = `${window.location.origin}/game/${gameId}/join`;
	});
	console.log(gameLink);
</script>

<Clipboard
	text={gameLink}
	let:copy
	on:copy={() => {
		console.log("Has Copied");
	}}
>
	<button on:click={copy}>Copy game link</button>
</Clipboard>

<style>
	button {
		width: 100px;
		height: 50px;
	}
</style>
