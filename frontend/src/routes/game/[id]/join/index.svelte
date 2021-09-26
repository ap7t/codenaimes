<script>
	import { page } from "$app/stores";

	import { fade } from "svelte/transition";

	let gameId = $page.params.id;
</script>

<div in:fade>
	<h1>What will you join this game as</h1>
	<p>
		<a href="../{gameId}/player/spymaster">Spymaster</a>
		<br />
		<a href="../{gameId}/player/operative">Operative</a>
	</p>
</div>
