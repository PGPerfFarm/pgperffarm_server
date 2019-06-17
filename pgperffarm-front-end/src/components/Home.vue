<template>
  <v-app>
    <!--
    <router-link v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
    <router-view @authenticated="setAuthenticated" />
	-->
    <main>
      <v-content>
        <pg-panel></pg-panel>          
      </v-content>
    </main>
  </v-app>
</template>

<script>
  import PgPanel from './Panel.vue'

  export default {
    name: 'home',
    components: {
      PgPanel
    },
    data() {
      return {
        authenticated: false,
        mockAccount: {
          username: "nraboy",
          password: "password"
        }
      }
    },
    mounted() {
      if(!this.authenticated) {
        this.$router.replace({ name: "login" });
      }
    },
    methods: {
      setAuthenticated(status) {
        this.authenticated = status;
      },
      logout() {
        this.authenticated = false;
      }
    }
  }
</script>
