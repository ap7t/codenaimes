<script lang="ts">
	import { socket } from "../socket.js";
	import { fly } from "svelte/transition";
	import { page } from "$app/stores";
	import { username, team } from "../stores";
	import Textfield from "@smui/textfield";
	import Icon from "@smui/textfield/icon";
	import { beforeUpdate, afterUpdate } from "svelte";
	import User from "$lib/User.svelte";

	export let spymaster;

	let gameLink;
	let gameId = $page.params.id;
	let message = "";
	let messages = [];
	let div;
	let autoscroll;
	let role = spymaster ? "spymaster" : "operative";

	beforeUpdate(() => {
		autoscroll = div && div.offsetHeight + div.scrollTop > div.scrollHeight - 20;
	});

	afterUpdate(() => {
		if (autoscroll) div.scrollTo(0, div.scrollHeight);
	});

	socket.on("message", function (data) {
		messages = [...messages, data];
		let objDiv = document.getElementById("scrollHider");
		objDiv.scrollTop = objDiv.scrollHeight;
	});

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		let data = {
			username: $username,
			team: $team,
			message: message,
			gameId: gameId,
			spymaster: spymaster,
			role: role
		};
		socket.emit("message", data);
		message = "";
	};
</script>

<div class="scrollHider">
	<h1>Chat</h1>
	<div class="messages" bind:this={div}>
		{#each messages as message, i}
			<p>
				<User username={message.username} team={message.team} role={message.role} />
				<span class="time">{message.timestamp}</span>
				<br />
				{message.message}
			</p>
		{/each}
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
		min-width: 10%;
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
	}
	span {
		font-weight: 900;
	}

	.time {
		color: rgb(155 149 147);
		font-size: 0.75rem;
	}
</style>
