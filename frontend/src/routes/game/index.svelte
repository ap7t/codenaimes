<script lang="ts">
	import { fade } from "svelte/transition";
	import Button, { Label } from "@smui/button";
	import { goto } from "$app/navigation";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";

	let gameId = "dev";
	let open = false;
	let ai = true;
	let title;
	let content;
	let label;

	$: if (open && !ai) {
		title = "Game ID Required";
		content = "You need to provide the Game ID before joining!";
		label = "Oops, my bad";
	} else {
		title = "404 Not Found";
		content = "This feature has not been added yet";
		label = "I await with bated breath";
	}

	function handleJoin(aiGame) {
		if (gameId) {
			if (aiGame) {
				goto(`/game/ai/${gameId}/join`);
			} else {
				goto(`/game/${gameId}/join`);
			}
		} else {
			open = true;
			ai = false;
		}
	}

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		handleJoin(false);
	};
</script>

<svelte:head>
	<title>Start</title>
</svelte:head>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">{title}</Title>
	<Content id="simple-content">{content}</Content>
	<Actions>
		<Button>
			<Label>{label}</Label>
		</Button>
	</Actions>
</Dialog>

<div class="container" in:fade>
	<div class="create">
		<h1>Create a game</h1>
		<div>
			<Button on:click={() => goto("/game/create")}>
				<Label>Play with humans</Label>
			</Button>
			<br />
			<Button on:click={() => goto("/game/ai/create")}>
				<Label>Play with AI</Label>
			</Button>
		</div>
	</div>
	<div class="join">
		<h1>Join an existing game</h1>
		<Textfield
			id="gameId"
			variant="outlined"
			required={true}
			bind:value={gameId}
			on:keydown={onInput}
			label="Game ID"
		>
			<HelperText slot="helper">Enter the Game ID to join the game</HelperText>
		</Textfield>
		<Button variant="raised" on:click={() => handleJoin(false)}>
			<Label>Join game</Label>
		</Button>
		<br />
		<Button variant="raised" on:click={() => handleJoin(true)}>
			<Label>Join gaime</Label>
		</Button>
	</div>
</div>

<style>
	.container {
		margin-top: 50px;
		width: 50%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		/* flex-wrap: wrap; */
	}

	div > div {
		margin-top: 50px;
		width: 50%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	div + div {
		border-top: solid 1px #55ff00;
	}

	h1 + div {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 5%;
	}
</style>
