<script>
	import { fade } from "svelte/transition";
	let gameId = "dev";
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<div in:fade>
	<h1>Create a new game</h1>
	<a href="/game/create">Play with humans</a>
	<br />
	<strike><a href="/game/create">Play with AI</a></strike> Coming soon &#128064;
	<hr />
	<h1>Join an existing game</h1>
	<input type="text" bind:value={gameId} placeholder="Enter existing gameId" />
	<br />
	<!-- TODO: check if the game actually exists first -->
	<a href="/game/{gameId}/join/"> Join Game</a>
</div>
