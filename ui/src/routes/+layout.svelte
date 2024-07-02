<script>
	import '../app.css';
</script>

<div class="text-primary-50 antialiased">
	<slot />
</div>

<style>
	:global(body) {
		@apply bg-primary-900;
	}
</style>
