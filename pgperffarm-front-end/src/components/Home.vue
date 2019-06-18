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
  import router from '../router'

  export default {
    name: 'home',
    components: {
      PgPanel
    },

    data() {
    },

    mounted() {
    this.checkLoggedIn();
    },

    methods: {
      checkLoggedIn() {
        this.$session.start();
        if (!this.$session.has("token")) {
          router.push("/auth");
        }
      }
    }
  };

</script>
