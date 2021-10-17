<script lang="ts">
	export const prerender = true;
	import AgentCard from "$lib/AgentCard.svelte";

	import { fade, fly } from "svelte/transition";
	let test = "test";
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<section in:fade>
	<p>Coden<b>ai</b>mes</p>
	<p>It's Codenames, but with AI</p>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 1;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
