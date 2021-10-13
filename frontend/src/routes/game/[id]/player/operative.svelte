<script>
	import ChatArea from "$lib/ChatArea.svelte";
	import ClueArea from "$lib/ClueArea.svelte";
	import GameBoard from "$lib/GameBoard.svelte";
	import LinkGame from "$lib/LinkGame.svelte";
	import { team, username } from "../../../../stores.js";
</script>

<h1>You joined as a operative</h1>
<h1>Player: {$username}</h1>
<h1>Team: {$team}</h1>
<LinkGame />
<ClueArea />
<ChatArea />
<GameBoard />
