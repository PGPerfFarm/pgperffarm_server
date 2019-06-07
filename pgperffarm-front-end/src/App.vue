# root component
# outer HTML and router view

# run with yarn serve

# add packages to packages.json
# fix tabs and spaces
# change font
# https
# github link in new tab

# next todo: adding login

<template>
  <login></login>
</template>

<script>
  // import Home from './components/Home.vue'
  import Login from './components/Login.vue'

  export default {
  name: 'app',
  components: {
    Login
  }
}

</script>