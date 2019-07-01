<template>
	<v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex d-flex xs12 sm6 md3>
            <v-layout column>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>Your information</v-card-title>
	                </v-card>
	                <v-card flat class="profile-left-bottom">
	                	<v-card-text>
                      Total reports: <br>
	                		N. machine(s): <br>
	                		N. branch(es) involved: <br>
	                		mail@mail.com
	                	</v-card-text>
	                </v-card>
            	</v-layout>
              </v-flex>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top"
	                >
	                  <v-card-title>Shortcuts</v-card-title>
                  </v-card>
                  <v-card flat class="profile-left-bottom">
                    <v-card-actions>
                    <v-btn block flat class="profile-button">
                  <router-link to="/addmachine">
                   Add a new machine
                  </router-link>
                  </v-btn>
                    </v-card-actions>
                    <v-card-actions>
                    <v-btn block flat class="profile-button">
                  <router-link to="/profile">
                   My machines
                  </router-link>
                  </v-btn>
                    </v-card-actions>
                    <v-card-actions>
                    <v-btn block flat class="profile-button" v-on:click="logout()">Logout</v-btn>
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