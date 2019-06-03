// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// import router from './router'
/*
import PgPanel from './components/Panel.vue'
import PgLoginForm from './components/LoginForm.vue'
import PgNavbar from './components/Navbar.vue'
import PgFooter from './components/Footer.vue'
import PgContent from './components/Content.vue'
*/

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  // router,
  template: '<App/>',
  components: { App }
})

new Vue({
    el: '#login-name',
    data: {
    logged: 'You are not logged in!'
    }
  })
