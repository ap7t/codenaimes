<script>
	import { page } from "$app/stores";

	import { fade } from "svelte/transition";

	let gameId = $page.params.id;
</script>

<!-- 
<div in:fade>
	<h1>What will you join this game as</h1>
	<p>
		<a href="../{gameId}/player/spymaster">Spymaster</a>
		<br />
		<a href="../{gameId}/player/operative">Operative</a>
	</p>
</div> -->

<h1>What will you join as?</h1>
<div class="p-10 flex flex-row">
	<!-- Spymaster card -->
	<a class="hover:no-underline" href="../{gameId}/player/spymaster">
		<div class="max-w-sm rounded overflow-hidden shadow-lg mx-6">
			<div class="px-6 py-4">
				<div class="font-bold text-xl mb-2 flex justify-between items-center">
					Spymaster
					<img class="w-auto h-10 w-10" src="/spymaster.png" alt="Spymaster" />
				</div>
				<p class="text-gray-700 text-base">
					Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla!
					Maiores et perferendis eaque, exercitationem praesentium nihil.
					<br />
					<br />
					TODO: give details about what spymaster does
				</p>
			</div>
		</div>
	</a>

	<!-- Operative card -->
	<a class="hover:no-underline" href="../{gameId}/player/spymaster">
		<div class="max-w-sm rounded overflow-hidden shadow-lg">
			<div class="px-6 py-4">
				<div class="font-bold text-xl mb-2 flex justify-between items-center">
					Operative
					<img class="w-auto h-10 w-10" src="/operative.png" alt="Operative" />
				</div>
				<p class="text-gray-700 text-base">
					Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla!
					Maiores et perferendis eaque, exercitationem praesentium nihil.
					<br />
					<br />
					TODO: give details about what operative does
				</p>
			</div>
		</div>
	</a>
</div>
