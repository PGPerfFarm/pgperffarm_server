# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# fix tabs and spaces
# https?
# responsiveness on mobile
# status in the last 30 days?

# todo wip
# fixed homepage and menu nav
# too much recursion error
# fix scrolling (everywhere)
# profile buttons center
# fix pre text
 
# note: rest api works with python3.7

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
	  	//Login
	  }
	}

</script>