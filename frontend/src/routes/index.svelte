<script lang="ts">
	export const prerender = true;
	import Button, { Label } from "@smui/button";
	import List, { Item, Text } from "@smui/list";
	import { goto } from "$app/navigation";

	import { fade } from "svelte/transition";
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<section in:fade>
	<p>
		<a href="https://en.wikipedia.org/wiki/Codenames_(board_game)" target="_blank">Codenames</a> is a
		great board game to play with your friends - but what if you don't have any friends?
	</p>
	<p>
		Modern problems require modern solutions. Play with <strong>AI</strong>
	</p>
</section>
<Button variant="raised" on:click={() => goto("/game")}>
	<Label>It's gaming time</Label>
</Button>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: right;
		flex: 1;
		width: 60%;
		margin-top: 5em;
	}

	section > p {
		font-size: 2rem;
	}

	p + p {
		font-size: large;
		margin-bottom: 5rem;
	}

	a {
		font-size: 3rem;
	}
</style>
