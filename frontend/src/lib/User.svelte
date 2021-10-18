<script lang="ts">
	import { Icon } from "@smui/button";

	export let username;
	export let role;
	export let team;
</script>

{#if role == "spymaster"}
	<div>
		<Icon class="material-icons {team.toLowerCase()}" slot="leadingIcon">person_search</Icon>
		<span class={team.toLowerCase()}>{username}</span>
	</div>
{:else}
	<div>
		<Icon class="material-icons {team.toLowerCase()}" slot="leadingIcon">support_agent</Icon>
		<span class={team.toLowerCase()}>{username}</span>
	</div>
{/if}

<style>
	div {
		display: inline-flex;
		align-items: center;
	}
</style>
