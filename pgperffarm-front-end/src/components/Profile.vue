<template>
	<v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex d-flex xs12 sm6 md3>
            <v-layout column>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title><v-icon color="rgb(51, 103, 145)">person</v-icon>Your information</v-card-title>
	                </v-card>
	                <v-card flat class="profile-left-bottom">
	                	<v-card-text>
                      <v-icon color="rgb(51, 103, 145)">archive</v-icon> &nbsp; Total reports: {{ $store.getters.reports }} <br>
	                		<v-icon color="rgb(51, 103, 145)">computer</v-icon> &nbsp; N. machine(s): {{ $store.getters.machines }} <br>
	                		<v-icon color="rgb(51, 103, 145)">format_list_bulleted</v-icon> &nbsp; Branch(es) of latest reports: {{ $store.getters.branches }}<br>
	                		<v-icon color="rgb(51, 103, 145)">email</v-icon> &nbsp; 
                      <a :href="`mailto:${$store.getters.email}`"> {{ $store.getters.email }} </a> <br>
	                	</v-card-text>
	                </v-card>
            	</v-layout>
              </v-flex>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top"
	                >
	                  <v-card-title><v-icon color="rgb(51, 103, 145)">bookmark</v-icon>Shortcuts</v-card-title>
                  </v-card>
                  <v-card flat class="profile-left-bottom">
                    <v-card-actions>
                    <v-btn block flat class="profile-button">
                  <router-link to="/addmachine">
                    <v-icon color="rgb(51, 103, 145)">add</v-icon>
                    Add a new machine
                  </router-link>
                  </v-btn>
                    </v-card-actions>
                    <v-card-actions>
                    <v-btn block flat class="profile-button">
                  <router-link to="/profile">
                    <v-icon color="rgb(51, 103, 145)">view_stream</v-icon>
                    My machines
                  </router-link>
                  </v-btn>
                    </v-card-actions>
                    <v-card-actions>
                    <v-btn block flat class="profile-button" v-on:click="logout()">
                      <v-icon color="rgb(51, 103, 145)">arrow_back</v-icon>
                      &nbsp; Logout
                    </v-btn>
                </v-card-actions>
	             </v-card>
	            </v-layout>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex d-flex fluid>
        <v-layout column>
          <v-card flat class="profile-card-title">
            <v-card-title class="profile-card-title-text">Welcome back, {{ $store.getters.username }}!</v-card-title>
          </v-card>
          <router-view></router-view>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'Profile',

  methods: {
    logout() {
        this.$store.commit('removeToken', this.$store.state);
        this.$router.push("/");
    }
  },

  mounted() {
    if (!this.$store.getters.authenticated)
      this.$router.push("/");
  }
}

</script>