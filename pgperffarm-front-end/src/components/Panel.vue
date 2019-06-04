<template>
	<div class='pg-panel'>

		<p class='pg-par'> {{text1}} </p>
		<p class='pg-par'> {{text2}} </p>

	</div>
</template>

<script>
	export default {
		name: 'PgPanel',
		data () {
			return {
				text1: 'The PostgreSQL Performance Farm project is a community project to collect performance data from tests, as code changes are made to PostgreSQL. Test results come as JSON or flat files, and the server-side interface is deployed using the Django framework. The web application is a Vue.js PWA.',
                 text2: 'This website enables registered users to upload, browse and download test results for all machines.'
			}
		}
	}
</script>


