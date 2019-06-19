// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// token: 6810f83b3fdf48c80d7fea8087180e3dc95e9ebd 

import Vue from 'vue'
import router from './router'
import axios from 'axios'

import Vuetify from 'vuetify'
import App from './App'
import VueSession from 'vue-session'

// Vue.prototype.$axios = axios;
Vue.config.productionTip = false

// setting up Vuetify
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify)
import './stylus/main.styl' 

Vue.use(VueSession)
Vue.use(axios)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
  components: { App }
}).$mount('#app')
