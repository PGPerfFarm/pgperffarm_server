// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import './assets/main.css'

import Vue from 'vue'
import router from './router'
import store  from  './store'
import App from './App'

Vue.config.productionTip = false

// setting up Vuetify
import vuetify from './plugins/vuetify';

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
    vuetify,
    components: { App }
}).$mount('#app')