<script>
	import '../app.css';
</script>

<div class="text-[var(--color-primary-50)] antialiased">
	<slot />
</div>

<style>
	:global(body) {
		background-color: var(--color-primary-900);
	}
</style>
