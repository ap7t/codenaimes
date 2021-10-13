<script lang="ts">
	import { socket } from "../socket.js";
	let data;
	console.log(socket);
	socket.on("connection", function () {
		data = "penis";
	});

	function fn() {
		console.log("sending socket thing");
		socket.emit("penis", "from client");
		console.log("should have sent");
	}
</script>

<div>
	test
	{data}
</div>
<button on:click={fn}> press me </button>
