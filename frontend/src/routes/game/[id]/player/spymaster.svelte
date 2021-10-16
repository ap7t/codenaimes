<script>
	import ClueInput from "$lib/ClueInput.svelte";
	import GameBoard from "$lib/GameBoard.svelte";
	import LinkGame from "$lib/LinkGame.svelte";
	import { team } from "../../../../stores";
	import { socket } from "../../../../socket";
	import { page } from "$app/stores";

	let gameId = $page.params.id;
	console.log("joined game");
	// socket.emit("join", gameId);
</script>

<h1>You joined as a spymaster</h1>
<h1>Team: {$team}</h1>
<!-- can probably do this better as operative and spymaster screens will have the same layout for the top -->
<ClueInput />
<GameBoard spymaster="true" />
