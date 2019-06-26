# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# fix tabs and spaces
# https?
# responsiveness on mobile

# todo wip
# fix navbar buttons hover
# fixed homepage and menu nav
# add farmer
# machine page
# results page
# fetching mail?
# too much recursion error
# fix scrolling
# profile buttons center
# cards binding profile
# fixing profile table style

# just keep 9.5 and after

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