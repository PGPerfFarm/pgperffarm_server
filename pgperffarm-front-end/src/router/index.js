import Vue from 'vue'
import Router from 'vue-router'

const Home = () => import('@/components/Home')
const PrivacyPolicy = () => import('@/components/PrivacyPolicy')
const License = () => import('@/components/License')
const Profile = () => import('@/components/Profile')
const Benchmarks = () => import('@/components/Benchmarks')
const Machines = () => import('@/components/Machines')
const Machine = () => import('@/components/Machine')
const Run = () => import('@/components/Run')
const Trend = () => import('@/components/Trend')
const Result = () => import('@/components/Result')
const BenchmarkList = () => import('@/components/BenchmarkList')
const Plots = () => import('@/components/Plots')
const Postgres = () => import('@/components/Postgres')

Vue.use(Router)

const routes = [
	{path: '/', name: 'Home', component: Home},
	// {path: '*', redirect: '/'},
	{path: '/privacypolicy', component: PrivacyPolicy},
	{path: '/license', component: License},
	{path: '/profile/', component: Profile, props: true},
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
	{path: '/postgres/:id', name: 'Postgres', component: Postgres, props: true},
]

export default new Router({
	mode: 'history',
  	routes,
})