<template>
	<v-app>
		<pg-toolbar></pg-toolbar>
	    <pg-navbar></pg-navbar>
	    <router-view></router-view>
	</v-app>
</template>

<script>

	export default {
	  name: 'App',
	  components: {
	  	PgNavbar: () => import("./components/Navbar.vue"),
	  	PgToolbar: () => import("./components/Toolbar.vue"),
	  	Home: () => import("./components/Home.vue"),
	  }
	}

</script>