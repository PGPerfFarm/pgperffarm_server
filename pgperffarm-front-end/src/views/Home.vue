<template>
  <v-app>
    <!--
    <router-link v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
    <router-view @authenticated="setAuthenticated" />
	-->
    <main>
      <v-content>
      	<pg-toolbar></pg-toolbar>
        <pg-navbar></pg-navbar>
        <pg-panel></pg-panel>          <pg-footer></pg-footer>
      </v-content>
    </main>
  </v-app>
</template>

<script>
import PgPanel from '../components/Panel.vue'
import PgNavbar from '../components/Navbar.vue'
import PgFooter from '../components/Footer.vue'
import PgToolbar from '../components/Toolbar.vue'
export default {
  name: 'home',
  components: {
    PgPanel,
    PgNavbar,
    PgFooter,
    PgToolbar
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
