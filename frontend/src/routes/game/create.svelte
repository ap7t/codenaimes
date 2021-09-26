<script>
	import { fade } from "svelte/transition";
	let gameId = "dev";
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<div in:fade>
	<h1>Create a game</h1>
	<input type="text" bind:value={gameId} placeholder="Create a game ID" />
	<br />
	<br />
	<a href="/game/{gameId}/join">Create</a>
</div>
