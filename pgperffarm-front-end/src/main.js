// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import router from './router'
import Axios from 'axios'
// import VueAxios from 'vue-axios'
import Vuetify from 'vuetify'
import App from './App'

Vue.config.productionTip = false

Vue.use(Vuetify)

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
  render: h => h(App),
  router,
  components: { App }
}).$mount('#app')
