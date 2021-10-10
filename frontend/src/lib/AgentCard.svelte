<script>
	import { page } from "$app/stores";
	import { io } from "socket.io-client";
	export let name;
	export let num;
	export let colour;

	let background;

	let gameId = $page.params.id;

	const socket = io("http://localhost:5000");
	console.log("in agent card");
	console.log(colour);
	console.log("^^^ colour");
	$: {
		switch (colour) {
			case "R":
				background = "red";
				break;
			case "B":
				background = "blue";
				break;
			case "O":
				background = "yellow";
				break;
			case "X":
				background = "purple";
				break;
		}
	}
	console.log(background);
	console.log("^^^ background");

	function makeMove(card) {
		console.log("made move");
		let data = { card: card, gameId: gameId };
		socket.emit("make_move", data);
		console.log(background);
	}
</script>

<div id="card-{num}" style="background-color: {background}" on:click={() => makeMove({ name })}>
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
