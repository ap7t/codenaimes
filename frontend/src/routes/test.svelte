<script lang="ts">
	import { state } from "../stores";
	let data;
	let unsubscribe = state.subscribe((stateData) => {
		data = stateData;
		console.log(data);
	});
</script>

<div>
	<h1>Game state:</h1>
	{data}
</div>
