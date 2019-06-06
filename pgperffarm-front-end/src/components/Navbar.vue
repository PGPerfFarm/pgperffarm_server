<template>
	<div class='pg-navbar'>
		<v-toolbar>
			<v-toolbar-items class="blue-grey-darken-2">
		      <v-btn flat><router-link to="/home">Home</router-link></v-btn>
		      <v-btn flat>Machine</v-btn>
		      <v-btn flat>Status</v-btn>
		      <v-menu open-on-hover bottom offset-y>
		      	<template v-slot:activator="{ on }">
			    	<v-btn flat v-on="on">
			          Contact
			        </v-btn>
			      </template>

			      <v-list>
			        <v-list-tile href="https://github.com/PGPerfFarm/pgperffarm">
			          <v-list-tile-title>GitHub</v-list-tile-title>
			        </v-list-tile>
			        	<v-list-tile>
			          	<v-list-tile-title>Help</v-list-tile-title>
			        	</v-list-tile>
			        <v-list-tile>
			          <v-list-tile-title>License</v-list-tile-title>
			        </v-list-tile>
			      </v-list>

			    </v-menu>
			    <v-btn flat><router-link to="/login">Login</router-link></v-btn>
    		</v-toolbar-items>
		</v-toolbar>
	</div>
</template>

<script>
	import router from '../router'

	export default {
		name: 'PgNavbar',
		methods: {
            navigate() {
                router.push({ name: "Home" });
            }
        }
	}
</script>