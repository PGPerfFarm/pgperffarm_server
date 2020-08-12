<template>
	<v-app>
		<pg-toolbar></pg-toolbar>
	    <pg-navbar></pg-navbar>
	    <router-view></router-view>
	</v-app>
</template>

<script>
	import PgNavbar from './components/Navbar.vue'
    import PgToolbar from './components/Toolbar.vue'

	export default {
	  name: 'App',
	  components: {
	  	PgNavbar,
	  	PgToolbar,
	  }
	}

</script>