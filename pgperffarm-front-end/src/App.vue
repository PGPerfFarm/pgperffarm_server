# root component
# outer HTML and router view

# favicon not working
# css padding is random
# fix tabs and spaces
# fix hovering navbar
# fix dynamic header

# next todo: adding login

<template>
  <div id='app'>
    <header>
        <a href='https://www.postgresql.org/'>
          <img src='./assets/images/transparent-logo.png' height='50' width='50'>
        </a>
        <span id='header-span'>Postgres Performance Farm</span>
    </header>

    <main>
      <!-- <img src="./assets/logo.png" alt="Vue.js PWA"> -->
      <pg-navbar></pg-navbar>
      <pg-panel></pg-panel>
      <pg-footer></pg-footer>

      <router-view></router-view>
    </main>

  </div>
</template>

<script>
import PgPanel from './components/Panel.vue'
import PgNavbar from './components/Navbar.vue'
import PgFooter from './components/Footer.vue'

export default {
  name: 'app',
  components: {
    PgPanel,
    PgNavbar,
    PgFooter
  }
}
</script>

<!-- <style lang="css" src="./static/style.css">