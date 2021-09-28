<script>
	export let name;
	export let num;
	export let colour;

	function showColour() {
		console.log(`card-${num}`);
		let card = document.getElementById(`card-${num}`);
		card.style.backgroundColor = colour;
	}
</script>

<div id="card-{num}" style="background-color: {colour}" on:click={showColour}>
	{name}
</div>

<style>
	div {
		text-transform: uppercase;
		margin: 1em;
		padding-top: 2em;
		border: 1px solid black;
		height: 100px;
		width: 100px;
		text-align: center;
	}
</style>
