import Vue from 'vue'
import Router from 'vue-router'

import Home from './components/Home.vue'
import Help from './components/Help.vue'
import PrivacyPolicy from './components/PrivacyPolicy.vue'
import License from './components/License.vue'
import Profile from './components/Profile.vue'
import Benchmarks from './components/Benchmarks.vue'
import Machines from './components/Machines.vue'
import Machine from './components/Machine.vue'
import Run from './components/Run.vue'
import Trend from './components/Trend.vue'
import Result from './components/Result.vue'
import BenchmarkList from './components/BenchmarkList.vue'
import Plots from './components/Plots.vue'

Vue.use(Router)

const routes = [
	{path: '/', name: 'Home', component: Home},
	// {path: '*', redirect: '/'},
	{path: '/help', component: Help},
	{path: '/privacypolicy', component: PrivacyPolicy},
	{path: '/license', component: License},
	{path: '/profile/:username', component: Profile, props: true},
	{path: '/machines', component: Machines, props: true},
	{path: '/benchmarks', component: Benchmarks, props: true},
	{path: '/machine/:id', component: Machine, props: true},
	{path: '/run/:id', name: 'Run', component: Run, props: true},
	{path: '/trend/:id/:config/', component: Trend, props: true,
		children: [
		{path: '/trend/:id/:config/detail/:commit/:machine/:benchmark', name: 'Detail', component: BenchmarkList},
		{path: '', name: 'Plots', component: Plots}
		]
	},
	{path: '/result/:id', name: 'Result', component: Result, props: true},
]

export default new Router({
	mode: 'history',
  	routes,
})