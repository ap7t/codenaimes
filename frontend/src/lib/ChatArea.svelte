<script lang="ts">
	import { socket } from "../socket.js";
	import { fly } from "svelte/transition";
	import { page } from "$app/stores";
	import { username, team } from "../stores";
	import Textfield from "@smui/textfield";
	import Icon from "@smui/textfield/icon";

	let gameLink;
	let gameId = $page.params.id;
	let message = "";
	let messages = [];

	socket.on("message", function (data) {
		console.log("received message");
		messages = [...messages, data];
		let objDiv = document.getElementById("messages");
		objDiv.scrollTop = objDiv.scrollHeight;
	});

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		let data = { username: $username, team: $team, message: message, gameId: gameId };
		socket.emit("message", data);
		message = "";
	};
</script>

<div>
	<div class="scrollHider">
		<h1>Chat</h1>
		<div class="messages">
			{#each messages as message, i}
				<p>
					<span class={message.team.toLowerCase()}>{message.username}</span>
					<span class="time">{message.timestamp}</span>
					<br />
					{message.message}
				</p>
			{/each}
		</div>
	</div>
</div>
<Textfield variant="outlined" bind:value={message} label="Message" on:keydown={onInput}>
	<Icon class="material-icons" slot="leadingIcon">chat</Icon>
</Textfield>

<style>
	.scrollHider {
		width: 100%;
		height: 400px;
		display: flex;
		flex-direction: column;
		align-items: center;
		overflow: hidden;
	}

	.messages {
		width: 100%;
		height: 100%;
		overflow-y: scroll;
		padding-right: 17px; /* Increase/decrease this value for cross-browser compatibility */
		box-sizing: content-box; /* So the width will be 100% + 17px */
		margin-left: auto;
		display: flex;
		flex-direction: column;
		align-items: left;
		background-color: #121212;
	}

	p {
		padding: 5px;
		margin: 10px 0;
		text-transform: uppercase;
		/* width: auto; */
	}
	span {
		font-weight: 900;
	}

	.red {
		color: red;
	}

	.blue {
		color: #2767ff;
	}

	.time {
		color: rgb(155 149 147);
		font-size: 0.75rem;
	}
</style>
