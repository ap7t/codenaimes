<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import Button, { Label, Icon } from "@smui/button";
	import Snackbar, { SnackbarComponentDev, Actions } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";

	export let ai = false;
	let gameLink;
	let gameId = $page.params.id;
	let text = "Copy";
	onMount(() => {
		if (ai) {
			gameLink = `${window.location.origin}/game/ai/${gameId}/join`;
		} else {
			gameLink = `${window.location.origin}/game/${gameId}/join`;
		}
	});

	function sleep(ms) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}

	async function copyLink() {
		let dummy = document.createElement("textarea");
		document.body.appendChild(dummy);
		dummy.value = gameLink;
		dummy.select();
		document.execCommand("copy");
		document.body.removeChild(dummy);
		text = "Copied";
		await sleep(2000);
		text = "Copy";
	}
</script>

<Button on:click={copyLink} variant="outlined">
	<Icon class="material-icons">content_copy</Icon>
	<Label>{text} game link</Label>
</Button>
