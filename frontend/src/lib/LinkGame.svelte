<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import Button, { Label, Icon } from "@smui/button";
	import Snackbar, { SnackbarComponentDev, Actions } from "@smui/snackbar";
	import IconButton from "@smui/icon-button";

	let gameLink;
	let gameId = $page.params.id;
	onMount(() => {
		gameLink = `${window.location.origin}/game/${gameId}/join`;
	});
	console.log(gameLink);

	function copyLink() {
		console.log("copied to clipboard");
		linkCopied.open();
	}
	let linkCopied: SnackbarComponentDev;
</script>

<Snackbar bind:this={linkCopied} timeoutMs={4000}>
	<Label>Link copied to clipboard!</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>
<Button on:click={copyLink} variant="outlined">
	<Icon class="material-icons">content_copy</Icon>
	<Label>Copy game link</Label>
</Button>
