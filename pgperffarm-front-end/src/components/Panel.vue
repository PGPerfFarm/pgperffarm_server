<template>
  <v-layout justify-center column my-4>
    <v-flex>
    	<v-card flat class="pg-v-card">
        	<v-card-text class="pg-v-card-text-main">
			Manage your test results!
			</v-card-text>
      </v-card>
  </v-flex>
  <v-flex>
      <v-card flat class="pg-v-card">
	        <v-card-text class="pg-v-card-text">
				      The PostgreSQL Performance Farm project is a community project to collect performance data from tests, as code changes are made to PostgreSQL. Test results come as JSON or flat files, and the server-side interface is deployed using the Django framework. The web application is made using Vue.js.
			     </v-card-text>
      </v-card>
  </v-flex>
  <v-flex>
      <v-card flat class="pg-v-card">
	        <v-card-text class="pg-v-card-text">
				    This website enables registered users to upload, browse and download test results for all machines.
			   </v-card-text>
      </v-card>
    </v-flex>
    <v-flex>
      <v-card flat class="pg-v-card">
	        <v-card-text class="pg-v-card-text">
				    Visit the <router-link to="/help">Help</router-link> page for additional information!
			     </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
	export default {
		name: 'PgPanel'
	}
</script>


