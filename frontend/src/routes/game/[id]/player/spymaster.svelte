<script>
	import GameBoard from "$lib/GameBoard.svelte";
	import LinkGame from "$lib/LinkGame.svelte";
</script>

<h1>You joined as a spymaster</h1>
<!-- can probably do this better as operative and spymaster screens will have the same layout for the top -->
<LinkGame />
<GameBoard spymaster="true" />
