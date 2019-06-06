// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import './plugins/vuetify'
import './plugins/vuetify'
import './plugins/vuetify'
import './plugins/vuetify'
import VueRouter from 'vue-router'
// import axios from 'axios'
// import VueAxios from 'vue-axios'

import App from './App'
import './stylus/main.styl'
import router from './router'

// require('./assets/css/style.css')

Vue.config.productionTip = false
// Vue.use(axios)
Vue.use(VueRouter)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  components: { App }
}).$mount('#app')
