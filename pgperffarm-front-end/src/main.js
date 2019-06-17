// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// token: 6810f83b3fdf48c80d7fea8087180e3dc95e9ebd 

import Vue from 'vue'
import router from './router'
import Axios from 'axios'
// import VueAxios from 'vue-axios'
import Vuetify from 'vuetify'
import App from './App'
import VueSession from 'vue-session'

Vue.config.productionTip = false

// setting up Vuetify
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify)
import './stylus/main.styl' 

Vue.use(VueSession)

// calling axios via $http
// setting token to handle requests
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

// Vue.use(Axios)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
  components: { App }
}).$mount('#app')
