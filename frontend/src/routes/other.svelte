<script>
	import { state } from "../stores";
	import { socket } from "../socket.js";

	let gameId = "dev";
	socket.on("connect", function () {
		// TODO: maybe keep a record of the messages and show when joined but thats a future improvement
		// console.log("connected");
		socket.emit("join", gameId);
		socket.emit("create_game", gameId);
	});

	socket.on("create_game", function (game) {
		// console.log("should have got game");
		$state = game;
	});
	function makeMove(card) {
		let data = { card: card, gameId: gameId };
		console.log(data);
		socket.emit("make_move", data);
		console.log("made move");
	}
</script>

<button on:click={() => makeMove("tangy")}> tangy </button>
<button on:click={() => makeMove("dad")}> dad </button>
<button on:click={() => makeMove("sweater")}> sweater </button>
