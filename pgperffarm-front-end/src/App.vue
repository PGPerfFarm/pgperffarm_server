# root component
# outer HTML and router view

<template>
  <div id='app'>
    <header>
      <span>Vue.js Postgres Performance Farm PWA </span>
    </header>

    <main>
      <!-- <img src="./assets/logo.png" alt="Vue.js PWA"> -->
      <pgpanel></pgpanel>

      <router-view></router-view>
    </main>

  </div>
</template>

<script>
import PgPanel from './components/Panel.vue'

export default {
  name: 'app',
  components: {
    PgPanel
  }
}
</script>

<!-- <style lang="css" src="./static/style.css">