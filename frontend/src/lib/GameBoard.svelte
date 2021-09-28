<script>
	import AgentCard from "./AgentCard.svelte";

	// export let agents;

	// dummy data
	let agents = [
		{ name: "resonant", colour: "blue" },
		{ name: "tangy", colour: "yellow" },
		{ name: "moldy", colour: "yellow" },
		{ name: "powerful", colour: "yellow" },
		{ name: "dad", colour: "blue" },
		{ name: "sweater", colour: "blue" },
		{ name: "experience", colour: "yellow" },
		{ name: "tart", colour: "blue" },
		{ name: "island", colour: "red" },
		{ name: "sneaky", colour: "yellow" },
		{ name: "church", colour: "yellow" },
		{ name: "modern", colour: "red" },
		{ name: "pipe", colour: "blue" },
		{ name: "hospital", colour: "red" },
		{ name: "examine", colour: "yellow" },
		{ name: "efficient", colour: "yellow" },
		{ name: "twist", colour: "blue" },
		{ name: "thank", colour: "blue" },
		{ name: "scrub", colour: "red" },
		{ name: "crook", colour: "yellow" },
		{ name: "clover", colour: "red" },
		{ name: "assorted", colour: "yellow" },
		{ name: "foregoing", colour: "red" },
		{ name: "embarrassed", colour: "red" },
		{ name: "glow", colour: "red" }
	];

	export let spymaster = false;
</script>

<div class="agentsGrid">
	{#each agents as agent, i}
		{#if spymaster}
			<AgentCard name={agent.name} colour={agent.colour} num={i} />
		{:else}
			<AgentCard name={agent.name} num={i} />
		{/if}
	{/each}
</div>

<style>
	.agentsGrid {
		width: 600px;
		display: grid;
		grid-gap: 75px;
		grid-template-columns: repeat(5, 100px);
		grid-template-rows: repeat(5, 100px);
		grid-auto-flow: column;
	}
</style>
