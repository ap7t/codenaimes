<script>
	import { fade } from "svelte/transition";
	let gameId = "dev";
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<div in:fade class="w-full max-w-xs">
	<div class="mb-4">
		<label class="block text-gray-700 text-sm font-bold mb-2" for="gameId"> Game ID </label>
		<input
			class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
			id="username"
			type="text"
			placeholder="Game ID"
			bind:value={gameId}
		/>
	</div>
	<div class="flex items-center justify-between">
		<a
			href="/game/{gameId}/join"
			class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline hover:no-underline"
			type="button"
		>
			Create Game
		</a>
	</div>
</div>
