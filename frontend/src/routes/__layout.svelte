<script>
	import Header from "$lib/header/Header.svelte";
	// import "../app.postcss";
</script>

<Header />
<main class="flex flex-col justify-center items-center">
	<slot />
</main>

<footer>
	<p>Hacked together by Adam Purcell 2021 &copy;</p>
</footer>

<style>
	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 1024px;
		margin: 0 auto;
		box-sizing: border-box;
		font-family: "Roboto";
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 40px;
		font-family: "Roboto";
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 40px 0;
		}
	}
</style>
