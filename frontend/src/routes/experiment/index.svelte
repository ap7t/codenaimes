<script lang="ts">
	import { browser, dev } from "$app/env";
	import { fade } from "svelte/transition";
	import FormField from "@smui/form-field";
	import Checkbox from "@smui/checkbox";
	import Button, { Label } from "@smui/button";
	import { goto } from "$app/navigation";
	import { state, expId } from "../../stores";
	import { socket } from "../../socket";
	import { v4 as uuidv4 } from "uuid";
	import { v4 } from "@lukeed/uuid";

	let checked: boolean | null = null;
	let uuid = "";

	function join() {
		uuid = uuidv4();
		$expId = uuid;
		socket.emit("experiment-create", uuid);
	}

	socket.on("before-experiment-join", function (game) {
		$state = game;
		goto("/experiment/operative");
	});
</script>

<svelte:head>
	<title>Experiment</title>
</svelte:head>

<div class="content" in:fade>
	<h1>Experiment</h1>
	<p>
		<strong>TODO:</strong> add explanation about how this will work
	</p>
	<FormField>
		<!--
          Note: binding to `indeterminate` is probably a bad idea.
          The component will set `indeterminate`, but it should be
          always related to `checked`.
       
          `indeterminate` is required for the correct state, even
          if `checked` is null.
        -->
		<Checkbox bind:checked indeterminate={checked === null} input$required />
		<span slot="label"
			>I have read the description of how this experiment will work and understand what I must do</span
		>
	</FormField>
	<!-- {#if checked !== null} -->
	<div>
		<Button variant="raised" on:click={join}>
			<Label>Start experiment</Label>
		</Button>
	</div>
	<!-- {/if} -->
</div>

<style>
	.content {
		width: 100%;
		max-width: var(--column-width);
		margin: var(--column-margin-top) auto 0 auto;
	}
</style>
