# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# add packages to packages.json
# fix tabs and spaces
# https?

# todo wip
# fix navbar buttons
# fixed homepage and menu nav
# machine - status
# remove extra apps

<template>
	<v-app>
		<pg-toolbar></pg-toolbar>
	    <pg-navbar></pg-navbar>
	    <router-view></router-view>
	    <pg-footer></pg-footer>
	</v-app>
</template>

<script>
	import PgNavbar from './components/Navbar.vue'
    import PgFooter from './components/Footer.vue'
    import PgToolbar from './components/Toolbar.vue'
    // import Login from './components/Login.vue'

	export default {
	  name: 'App',
	  components: {
	  	PgNavbar,
	  	PgToolbar,
	  	PgFooter,
	  	//Login
	  }
	}

</script>