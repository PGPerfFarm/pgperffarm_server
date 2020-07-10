import Vue from 'vue'
import Router from 'vue-router'

import Home from './components/Home.vue'
import Login from './components/Login.vue'
import Help from './components/Help.vue'
import PrivacyPolicy from './components/PrivacyPolicy.vue'
import License from './components/License.vue'
import Profile from './components/Profile.vue'
import Branches from './components/Branches.vue'
import Machines from './components/Machines.vue'
import MyMachines from './components/MyMachines.vue'
import Machine from './components/Machine.vue'
import Apply from './components/Apply.vue'
import Results from './components/Results.vue'
import Result from './components/Result.vue'

Vue.use(Router)

const routes = [
	{path: '/', name: 'Home', component: Home},
	// {path: '*', redirect: '/'},
	{path: '/login', component: Login},
	{path: '/help', component: Help},
	{path: '/privacypolicy', component: PrivacyPolicy},
	{path: '/license', component: License},
	{path: '/profile', component: Profile, props: true,
		children: [
        {path: '/addmachine', component: Apply},
        {path: '', component: MyMachines}
        ]
	},
	{path: '/machines', component: Machines, props: true},
	{path: '/branches', component: Branches, props: true},
	{path: '/machine/:alias', component: Machine, props: true},
	//{path: '/records/:id', name: 'Record', component: Results, props: true}
	{path: '/results', name: 'Results', component: Results, props: true},
	{path: '/result', name: 'Result', component: Result, props: true}
]

export default new Router({
	mode: 'history',
  	routes,
})