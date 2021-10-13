<script>
	import ClueInput from "$lib/ClueInput.svelte";
	import GameBoard from "$lib/GameBoard.svelte";
	import LinkGame from "$lib/LinkGame.svelte";
	import { team } from "../../../../stores";
</script>

<h1>You joined as a spymaster</h1>
<h1>Team: {$team}</h1>
<!-- can probably do this better as operative and spymaster screens will have the same layout for the top -->
<LinkGame />
<ClueInput />
<GameBoard spymaster="true" />
