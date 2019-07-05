# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# fix tabs and spaces
# https?
# fix cors headers same origin
# responsiveness on mobile
# avatars?

# todo wip
# fix navbar buttons hover
# fixed homepage and menu nav
# too much recursion error
# fix scrolling
# profile buttons center
# cards binding profile
# fixing profile table style
# fix table pagination and sorting
# add n. branches to profile
# status in the last 30 days
# add machine link to profile and status
# add report link to single machine page

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