// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// token: 6810f83b3fdf48c80d7fea8087180e3dc95e9ebd 

import Vue from 'vue'
import router from './router'
import Axios from 'axios'
import store  from  './store'

import Vuetify from 'vuetify'
import App from './App'
import VueSession from 'vue-session'
//import VueAuthenticate from 'vue-authenticate'
//import VueResource from 'vue-resource'

// Vue.prototype.$axios = axios;
Vue.config.productionTip = false

// setting up Vuetify
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify)
import './stylus/main.styl' 

Vue.use(VueSession)

// adding Axios to Vue instance
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token')
if (token) {
    Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
  components: { App }
}).$mount('#app')
