<script lang="ts">
	import Card, { PrimaryAction, Actions, ActionButtons, ActionIcons } from "@smui/card";
	import Button, { Label } from "@smui/button";
	import Dialog, { Title, Content, Actions } from "@smui/dialog";
	import Textfield from "@smui/textfield";
	import HelperText from "@smui/textfield/helper-text/index";
	import Radio from "@smui/radio";
	import FormField from "@smui/form-field";
	import { goto } from "$app/navigation";
	import { state, username, team } from "../../../../stores";
	import { page } from "$app/stores";
	import { socket } from "../../../../socket";
	let gameId = $page.params.id;

	let name = "dev";
	let redblue = "Red";
	let open = false;
	let pt;

	$: $username = name;
	$: $team = redblue;

	function handleSubmit(playerType) {
		pt = playerType;
		if (name === "") {
			open = true;
		} else {
			socket.emit("join", gameId);
		}
	}

	socket.on("before-join", function (game) {
		console.log("got the game state before joining");
		$state = game;
		goto(`/game/${gameId}/player/${pt}`);
		console.log($state);
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
		<Textfield id="nameInput" variant="outlined" required={true} bind:value={name} label="Name">
			<HelperText slot="helper">Enter a name so you can be recognised by your team</HelperText>
		</Textfield>
	</div>
	<div class="radio-demo">
		<h3>Choose your team</h3>
		{#each ["Red", "Blue"] as option}
			<FormField>
				<Radio bind:group={redblue} value={option} touch />
				<span slot="label">{option}</span>
			</FormField>
		{/each}
	</div>
</div>

<div class="card-display">
	<Card>
		<!-- <Content><h2>Spymaster</h2></Content>
			<Content>Description of what a spymaster does</Content> -->
		<Actions fullBleed>
			<Button on:click={() => handleSubmit("spymaster")}>
				<Label>Join as Spymaster</Label>
				<i class="material-icons" aria-hidden="true">arrow_forward</i>
			</Button>
		</Actions>
	</Card>

	<Card>
		<!-- <Content><h2>Operative</h2></Content>
			<Content>Description of what a operative does</Content> -->
		<Actions fullBleed>
			<Button on:click={() => handleSubmit("operative")}>
				<Label>Join as Operative</Label>
				<i class="material-icons" aria-hidden="true">arrow_forward</i>
			</Button>
		</Actions>
	</Card>
</div>

<style>
	div * {
		padding: 20px;
	}
</style>
