# root component
# outer HTML and router view

# run with yarn serve

# add axios to packages.json
# fix tabs and spaces
# change font
# https
# github link in new tab

# next todo: adding login

<template>
  <home></home>
</template>

<script>
  import Home from './views/Home.vue'

  export default {
  name: 'app',
  components: {
    Home
  }
}

</script>