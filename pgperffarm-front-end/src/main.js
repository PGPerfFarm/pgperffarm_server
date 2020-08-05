// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// token: 6810f83b3fdf48c80d7fea8087180e3dc95e9ebd 

import './assets/main.css'

import Vue from 'vue'
import router from './router'
import store  from  './store'

import Vuetify from 'vuetify'
import App from './App'

Vue.config.productionTip = false

// setting up Vuetify
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
  components: { App }
}).$mount('#app')
