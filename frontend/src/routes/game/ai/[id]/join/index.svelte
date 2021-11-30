<script lang="ts">
	import Card, { PrimaryAction, Actions, ActionButtons, ActionIcons } from "@smui/card";
	import Button, { Label } from "@smui/button";
	import Dialog, { Title, Content } from "@smui/dialog";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Radio from "@smui/radio";
	import FormField from "@smui/form-field";
	import { goto } from "$app/navigation";
	import { state, username, team } from "../../../../../stores";
	import { page } from "$app/stores";
	import { socket } from "../../../../../socket";
	import IconButton from "@smui/icon-button";
	import User from "$lib/User.svelte";

	let gameId = $page.params.id;

	let name = "";
	let redblue = "Red";
	let role = "Operative";
	let open = false;

	$: $username = name;
	$: $team = redblue;

	function handleSubmit() {
		if (name === "") {
			open = true;
		} else {
			socket.emit("ai_join", gameId);
		}
	}

	const onInput = (event) => {
		if (event.key !== "Enter") return;
		handleSubmit();
	};

	socket.on("before-join", function (game) {
		$state = game;
		goto(`/game/ai/${gameId}/player/${role.toLowerCase()}`);
	});
</script>

<Dialog bind:open aria-labelledby="simple-title" aria-describedby="simple-content">
	<!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
	<Title id="simple-title">Name Required</Title>
	<Content id="simple-content">You must enter a name before joining the game!</Content>
	<Actions>
		<Button on:click={() => (open = false)}>
			<Label>Oops</Label>
		</Button>
	</Actions>
</Dialog>
<div>
	<div>
		<h2>1. Identify yourself</h2>
		<Textfield id="nameInput" required={true} bind:value={name} on:keydown={onInput} label="Name">
			<HelperText slot="helper">Enter a name so you can be recognised by your team</HelperText>
		</Textfield>
	</div>
	<div class="radio-demo">
		<h2>2. Choose your team</h2>
		{#each ["Red", "Blue"] as option}
			<FormField>
				<Radio bind:group={redblue} value={option} touch />
				<span class={option == "Red" ? "red" : "blue"} slot="label">{option}</span>
			</FormField>
		{/each}
	</div>
	<div>
		<h2>3. Play</h2>
		<div>
			<User username={$username} team={redblue.toLowerCase()} role={role.toLowerCase()} />
			<Button variant="raised" class="red" on:click={handleSubmit}>
				<Label>Join as {role}</Label>
			</Button>
		</div>
	</div>
</div>

<style>
	h2 + div {
		display: flex;
		justify-content: space-evenly;
		flex-direction: row-reverse;
	}
</style>
