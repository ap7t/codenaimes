<script lang="ts">
	import Drawer, { AppContent, Content, Header, Title, Subtitle } from "@smui/drawer";
	import Button, { Label, Icon } from "@smui/button";
	import List, { Item, Text } from "@smui/list";
	import { goto } from "$app/navigation";

	let open = false;
	let active = "Gray Kittens";

	function setActive(value: string) {
		active = value;
	}
</script>

<nav>
	<label class="logo" on:click={() => goto("/")}>coden<strong>ai</strong>mes</label>
	<ul>
		<li>
			<Button on:click={() => goto("/")}>
				<Icon class="material-icons">home</Icon>
				<Label>Home</Label>
			</Button>
		</li>
		<li>
			<Button on:click={() => goto("/game")}>
				<Icon class="material-icons">sports_esports</Icon>
				<Label>Play</Label>
			</Button>
		</li>
		<li>
			<Button on:click={() => goto("/about")}>
				<Icon class="material-icons">info</Icon>
				<Label>About</Label>
			</Button>
		</li>
	</ul>
</nav>

<style>
	* {
		font-family: "Roboto";
	}
	nav {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		height: 60px;
		max-width: 100%;
	}
	label.logo {
		font-size: 35px;
		font-weight: bold;
		line-height: 60px;
		margin-left: 40px;
	}
	nav ul {
		/* float: right; */
		display: flex;
		flex-direction: row;
		margin-right: 50px;
	}
	nav ul li {
		display: inline-block;
		line-height: 60px;
		margin: 0px 20px;
	}
</style>
