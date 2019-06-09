<template>
	<v-toolbar 
	flat 
	color="white">
		<v-toolbar-items >		      
			<v-btn 
				flat
				rgb(51, 103, 145)--text
		     >
		     	<router-link to="/home">
		     		<v-icon color="rgb(51, 103, 145)">home</v-icon>
		     		Home
		     	</router-link>
		     </v-btn>
		     <v-btn flat>
		     	<v-icon color="rgb(51, 103, 145)">dns</v-icon>
		     	 Machine
		     </v-btn>
		     <v-btn flat>
		     	<v-icon color="rgb(51, 103, 145)">list</v-icon>
		     	 Status</v-btn>
		     <v-menu open-on-hover bottom offset-y>
		      	<template v-slot:activator="{ on }">
			    	<v-btn flat v-on="on">
			    		<v-icon color="rgb(51, 103, 145)">feedback</v-icon>
			           Contact
			        </v-btn>
			      </template>

			      <v-list>
			        <v-list-tile href="https://github.com/PGPerfFarm/pgperffarm">
			        	<v-icon color="rgb(51, 103, 145)">code</v-icon>
			          <v-list-tile-title> GitHub</v-list-tile-title>
			        </v-list-tile>
			        	<v-list-tile>
			        		<v-icon color="rgb(51, 103, 145)">help</v-icon>
			          	<v-list-tile-title> Help</v-list-tile-title>
			        	</v-list-tile>
			        <v-list-tile>
			        	<v-icon color="rgb(51, 103, 145)">copyright</v-icon>
			          <v-list-tile-title> License</v-list-tile-title>
			        </v-list-tile>
			      </v-list>

			    </v-menu>
			   <v-btn flat><router-link to="/login">
			   	<v-icon color="rgb(51, 103, 145)">input</v-icon>
			   Login</router-link></v-btn>
    	</v-toolbar-items>
	</v-toolbar>
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