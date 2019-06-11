# root component
# outer HTML and router view

# run with yarn serve

# todo after website is complete
# add packages to packages.json
# fix tabs and spaces
# https?

# todo asap
# fix login card
# fix pp & license bottom border
# fix router
# add help link to homepage
# fixed homepage and menu bar
# machine - status - profile

<template>
  <login></login>
</template>

<script>
  import Login from './components/Login.vue'

  export default {
  name: 'App',
  components: {
    Login
  }
 }

</script>