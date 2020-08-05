<template>
	<v-app>
		<main>
	 		<v-content>
				<pg-panel></pg-panel>          
			</v-content>
		</main>
	</v-app>
</template>

<script>
	import PgPanel from './Panel.vue'

	export default {
		name: 'home',
		components: {
			PgPanel
		},
  	};

</script>
