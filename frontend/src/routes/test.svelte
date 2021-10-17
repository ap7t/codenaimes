<script lang="ts">
	let clues = [
		"messagebackground-color: #121212;background-color: #121212;background-color: #121212; 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9",
		"message 9"
	];
</script>

<div class="scrollHider">
	<h1>Chat</h1>
	<div class="messages">
		{#each clues as clue, i}
			<p>
				<span class={i % 2 == 0 ? "red" : "blue"}>username</span> <span class="time">16:20</span>
				<br />
				{clue}
			</p>
		{/each}
	</div>
</div>

<style>
	.scrollHider {
		width: 30%;
		height: 400px;
		display: flex;
		flex-direction: column;
		align-items: center;
		overflow: hidden;
	}

	.messages {
		width: 100%;
		height: 100%;
		overflow-y: scroll;
		padding-right: 17px; /* Increase/decrease this value for cross-browser compatibility */
		box-sizing: content-box; /* So the width will be 100% + 17px */
		margin-left: auto;
		display: flex;
		flex-direction: column;
		align-items: left;
		background-color: #121212;
	}

	p {
		padding: 5px;
		margin: 10px 0;
		text-transform: uppercase;
		/* width: auto; */
	}
	span {
		font-weight: 900;
	}

	.red {
		color: rgb(199, 45, 45);
	}

	.blue {
		color: #2767ff;
	}

	.time {
		color: rgb(155 149 147);
		font-size: 0.75rem;
	}
</style>
