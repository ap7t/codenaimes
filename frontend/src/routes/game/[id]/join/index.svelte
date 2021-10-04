<script lang="ts">
	import Card, { Content, PrimaryAction, Actions, ActionButtons, ActionIcons } from "@smui/card";
	import Button, { Label } from "@smui/button";

	import { page } from "$app/stores";
	let gameId = $page.params.id;

	let clicked = 0;
</script>

<div class="card-display">
	<div class="card-container">
		<Card>
			<Content><h2>Spymaster</h2></Content>
			<Content>Description of what a spymaster does</Content>
			<Actions fullBleed>
				<Button on:click={() => (window.location = `/game/${gameId}/player/spymaster`)}>
					<Label>Join as Spymaster</Label>
					<i class="material-icons" aria-hidden="true">arrow_forward</i>
				</Button>
			</Actions>
		</Card>
	</div>

	<div class="card-container">
		<Card>
			<Content><h2>Operative</h2></Content>
			<Content>Description of what a operative does</Content>
			<Actions fullBleed>
				<Button on:click={() => (window.location = `/game/${gameId}/player/operative`)}>
					<Label>Join as Operative</Label>
					<i class="material-icons" aria-hidden="true">arrow_forward</i>
				</Button>
			</Actions>
		</Card>
	</div>
</div>

<style>
	* :global(.card-media-16x9) {
		background-image: url(https://place-hold.it/320x180?text=16x9&fontsize=23);
	}

	* :global(.card-media-square) {
		background-image: url(https://place-hold.it/320x320?text=square&fontsize=23);
	}

	div {
		padding-top: 10px;
	}
</style>
