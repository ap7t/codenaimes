<script>
	import { state } from "../stores";
	import { socket } from "../socket.js";

	let gameId = "dev";
	socket.on("connect", function () {
		socket.emit("join", gameId);
		socket.emit("create_game", gameId);
	});

	socket.on("create_game", function (game) {
		$state = game;
	});
	function makeMove(card) {
		let data = { card: card, gameId: gameId };
		socket.emit("make_move", data);
	}
</script>

<button on:click={() => makeMove("tangy")}> tangy </button>
<button on:click={() => makeMove("dad")}> dad </button>
<button on:click={() => makeMove("sweater")}> sweater </button>
