import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist'

Vue.use(Vuex)

const vuexPersist = new VuexPersist({
  key: 'my-app',
  storage: localStorage
})

//var baseUrl = 'http://140.211.168.111:8080/'
var baseUrl = 'http://127.0.0.1:8000/'

export default new Vuex.Store({
  	state: {
	    authUser: '',
	    isAuthenticated: false,
	    jwt: localStorage.getItem('token'),
	    email: '',
	    reports: '',
	    machines: '',
	    branches: '',
	    pgbench_results: [],

	    endpoints: {
		    obtainJWT: baseUrl + 'login_token/',
		    machines: baseUrl + 'machines/',
		    status: baseUrl + 'records-by-branch/',
		    machine: baseUrl + 'machine-records-by-branch/',
		    my_machine: baseUrl + 'my-machines/',
		    record: baseUrl + 'last_runs/',
		    run: baseUrl + 'run/',
		    users: baseUrl + 'users/',
		    benchmarks: baseUrl + 'benchmarks_machines/',
		    results: baseUrl + 'pgbench_results_complete/',
		    trends: baseUrl + 'pgbench_trends/',
		    trends_benchmarks: baseUrl + 'pgbench_results_commit/',
	    }
  	},

  	mutations: {

	    setAuthUser(state, {
	      authUser,
	      isAuthenticated,
	      email}) {
	      Vue.set(state, 'authUser', authUser)
	      Vue.set(state, 'isAuthenticated', isAuthenticated)
	      Vue.set(state, 'email', email)
	    },

	    updateToken(state, newToken) {
	      localStorage.setItem('token', newToken);
	      state.jwt = newToken;
	    },

	    removeToken(state) {
	      localStorage.removeItem('token');
	      state.jwt = null;
	      state.isAuthenticated = false;
	    },

	    setProfile(state, info) {
	    	localStorage.setItem('reports', info.reports);
	    	localStorage.setItem('machines', info.machines);
	    	localStorage.setItem('branches', info.branches);
	    	localStorage.setItem('email', info.email);
	    	state.reports = info.reports;
	    	state.machines = info.machines;
	    	state.branches = info.branches;
	    	//state.email = info.email;
	    },

	    setPgBenchResults(state, obj) {
	    	localStorage.setItem('pgbench_results', obj);
	    	state.pgbench_results = obj;
	    }

	},

	getters: {
    	username: state => state.authUser,
    	token: state => state.jwt,
    	authenticated: state => state.isAuthenticated,
    	email: state => state.email,
    	reports: state => state.reports,
    	branches: state => state.branches,
    	machines: state => state.machines,
    	pgbench_results: state => state.pgbench_results,
  	},

  	actions: {
  		fetchAccessToken({commit}) {
      		commit('updateAccessToken', localStorage.getItem('token'));
    	}
  	},

  	plugins: [vuexPersist.plugin]
})

