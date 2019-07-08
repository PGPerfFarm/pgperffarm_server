# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# fix tabs and spaces
# https?
# fix cors headers same origin
# responsiveness on mobile
# avatars?
# status in the last 30 days?

# todo wip
# fixed homepage and menu nav
# too much recursion error
# fix scrolling (everywhere)
# profile buttons center
# fix table pagination and sorting
# fix pre text
# loading and no data
 
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