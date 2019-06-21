<template>
	<v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex d-flex xs12 sm6 md3>
        <v-layout row wrap>
          <v-flex d-flex>
            <v-layout row wrap>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card
	                  color="grey"
	                  dark
	                >
	                  <v-card-title>Your information</v-card-title>
	                  <v-card-text>Total reports: </v-card-text>
	                </v-card>
	                <v-card>
	                	<v-card-text>
	                		N machine(s) <br>
	                		N branch(es) involved <br>
	                		mail@mail.com
	                	</v-card-text>
	                </v-card>
            	</v-layout>
              </v-flex>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card
	                  color="grey"
	                  dark
	                >
	                  <v-card-title>Shortcuts</v-card-title>
	                  <v-card-text>Add a new machine </v-card-text>
	                </v-card>
	                <v-card>
	                	<v-card-text>
	                		Logout
	                	</v-card-text>
	                </v-card>
	            </v-layout>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex d-flex fluid>
        <v-card color="white">
          <v-card-title primary class="title">Welcome back, username</v-card-title>
          <v-card-text>table</v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'Profile',

  data() {
  	return {
  		user: ''
  	}
  },

  methods: {

  }
}

</script>