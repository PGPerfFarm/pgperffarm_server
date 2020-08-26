<template>
	<v-card flat>
	<v-toolbar 
	text
	>
		<v-toolbar-items>		      
			<v-btn text class="v-btn-navbar" href="/">
		     	<v-icon color="rgb(51, 103, 145)">home</v-icon> &nbsp; Home
		    </v-btn>

		    <v-btn text class="v-btn-navbar" href="/machines">
		     	<v-icon color="rgb(51, 103, 145)">dns</v-icon> &nbsp; Machines
		      </v-btn>

		    <v-btn text class="v-btn-navbar" href="/benchmarks">
		    	<v-icon color="rgb(51, 103, 145)">list</v-icon> &nbsp; Benchmarks
		     </v-btn>

		     <v-menu open-on-hover bottom offset-y>
		      	<template v-slot:activator="{ on }">
			    	<v-btn text v-on="on" class="v-btn-navbar">
			    		<v-icon color="rgb(51, 103, 145)">feedback</v-icon> &nbsp; About
			        </v-btn>
			      </template>

			      <v-list>
			        <v-list-item href="https://github.com/PGPerfFarm/pgperffarm" class="v-btn-navbar" target="_blank">
			        	<v-icon color="rgb(51, 103, 145)">code</v-icon>
			          <v-list-item-title class="v-tile-navbar"> &nbsp; GitHub</v-list-item-title>
			        </v-list-item>

			        <v-list-item class="v-btn-navbar" href="/privacypolicy">
			        	<v-icon color="rgb(51, 103, 145)">security</v-icon> &nbsp;
			          	<v-list-item-title class="v-tile-navbar"> &nbsp; Privacy Policy</v-list-item-title>
			        </v-list-item>

			        <v-list-item class="v-btn-navbar" href="/license">
			        	<v-icon color="rgb(51, 103, 145)">copyright</v-icon>
			          	<v-list-item-title class="v-tile-navbar"> &nbsp; License</v-list-item-title>
			        </v-list-item>
			      </v-list>
			    </v-menu>
			</v-toolbar-items>
			<v-spacer></v-spacer>

			<v-toolbar-items v-if="cookie == null">
				   <v-btn text class="v-btn-navbar" :href="$store.state.endpoints.login">
				   		<v-icon color="rgb(51, 103, 145)">input</v-icon> &nbsp; Login
					</v-btn>
	    	</v-toolbar-items>

	    	<v-toolbar-items v-else>
	    		<v-btn text class="v-btn-navbar" href="/profile">
				   	<v-icon color="rgb(51, 103, 145)">person</v-icon>
				   		&nbsp; {{ $store.state.username }} 
				</v-btn>

				<v-btn text class="v-btn-navbar" v-on:click="logout()">
					<v-icon color="rgb(51, 103, 145)">highlight_off</v-icon>
					   	&nbsp; Logout
				</v-btn>
	    	</v-toolbar-items>
	</v-toolbar>
</v-card>
</template>

<script>

	export default {
		name: 'PgNavbar',

		data: () => ({
			cookie: null,
		}),

		methods: {

			getCookie() {
				var name = 'csrftoken';
				const value = `; ${document.cookie}`;
				const parts = value.split(`; ${name}=`);
				if (parts.length === 2) return parts.pop().split(';').shift();
			},

		    logout() {

		    	var url = this.$store.state.endpoints.logout;
				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.withCredentials = true;
				httpRequest.setRequestHeader("Content-Type", "application/json");
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {

							this.$store.commit('removeUsername');
		    				this.$router.push("/");
							
						}
					}
					else {
							console.log(httpRequest.status);
					}
				}
		    	
		    }
		}
	}

</script>