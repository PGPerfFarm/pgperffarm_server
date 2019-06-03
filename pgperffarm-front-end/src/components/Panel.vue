<template>
	<div id='pg-panel'>
		<Panel headline="Postgres Performance Farm">
			<p> abc {{test}} </p>
		</Panel>
	</div>
</template>

<script>
	export default {
		name: 'pg-panel',
		data () {
			return {
				test: 'aaa'
			}
		}
	}
</script>