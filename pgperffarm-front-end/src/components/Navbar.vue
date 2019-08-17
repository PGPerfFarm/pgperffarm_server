<template>
	<v-toolbar 
	class="main-navbar"
	flat
	>
		<v-toolbar-items>		      
			<v-btn flat class="v-btn-navbar" href="/">
		     	<v-icon color="rgb(51, 103, 145)">home</v-icon>
		     	&nbsp; Home
		    </v-btn>

		    <v-btn flat class="v-btn-navbar" href="/machines">
		     	<v-icon color="rgb(51, 103, 145)">dns</v-icon>
		     	 &nbsp; Machines
		      </v-btn>

		    <v-btn flat class="v-btn-navbar" href="/status">
		    	<v-icon color="rgb(51, 103, 145)">list</v-icon>
		     	 &nbsp; Status
		     </v-btn>

		     <v-menu open-on-hover bottom offset-y>
		      	<template v-slot:activator="{ on }">
			    	<v-btn flat v-on="on" class="v-btn-navbar">
			    		<v-icon color="rgb(51, 103, 145)">feedback</v-icon>
			           &nbsp; About
			        </v-btn>
			      </template>

			      <v-list>
			        <v-list-tile href="https://github.com/PGPerfFarm/pgperffarm" class="v-btn-navbar" target="_blank">
			        	<v-icon color="rgb(51, 103, 145)">code</v-icon>
			          <v-list-tile-title>&nbsp; GitHub</v-list-tile-title>
			        </v-list-tile>

			        <v-list-tile class="v-btn-navbar" href="/help">
			        	<v-icon color="rgb(51, 103, 145)">help</v-icon>
			          	<v-list-tile-title>&nbsp; Help</v-list-tile-title>
			        </v-list-tile>

			        <v-list-tile class="v-btn-navbar" href="/privacypolicy">
			        	<v-icon color="rgb(51, 103, 145)">security</v-icon>
			          	<v-list-tile-title>&nbsp; Privacy Policy</v-list-tile-title>
			        </v-list-tile>

			        <v-list-tile class="v-btn-navbar" href="/license">
			        	<v-icon color="rgb(51, 103, 145)">copyright</v-icon>
			          	<v-list-tile-title>&nbsp; License</v-list-tile-title>
			        </v-list-tile>
			      </v-list>
			    </v-menu>
			</v-toolbar-items>
			<v-spacer></v-spacer>

			<v-toolbar-items v-if="!$store.getters.authenticated">
				   <v-btn flat class="v-btn-navbar" href="/login">
				   		<v-icon color="rgb(51, 103, 145)">input</v-icon>
				   		&nbsp; Login
					</v-btn>
	    	</v-toolbar-items>

	    	<v-toolbar-items v-else>
	    		<v-btn flat class="v-btn-navbar" href="/profile">
				   	<v-icon color="rgb(51, 103, 145)">person</v-icon>
				   		&nbsp; {{ $store.getters.username }} 
				</v-btn>

				<v-btn flat class="v-btn-navbar" v-on:click="logout()">
					<v-icon color="rgb(51, 103, 145)">highlight_off</v-icon>
					   	&nbsp; Logout
				</v-btn>
	    	</v-toolbar-items>
	</v-toolbar>
</template>

<script>
	// import router from '../router'

	export default {
		name: 'PgNavbar',

		methods: {
		    logout() {
		    	this.$store.commit('removeToken', this.$store.state);
		    	this.$router.push("/");
		    }
		}
	}

</script>