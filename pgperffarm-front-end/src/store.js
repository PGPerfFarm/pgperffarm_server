import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var baseUrl = 'http://140.211.168.111:8080/'
//var baseUrl = 'http://127.0.0.1:8000/'

export default new Vuex.Store({
  	state: {
	 
	    endpoints: {
		    obtainJWT: baseUrl + 'login_token/',
		    machines: baseUrl + 'machines/',
		    machine: baseUrl + 'history/',
		    my_machine: baseUrl + 'my-machines/',
		    record: baseUrl + 'last_runs/',
		    run: baseUrl + 'run/',
		    user: baseUrl + 'machine_user/',
		    benchmarks: baseUrl + 'benchmarks_machines/',
		    results: baseUrl + 'pgbench_results_complete/',
		    trends: baseUrl + 'pgbench_trends/',
		    trends_benchmarks: baseUrl + 'pgbench_results_commit/',
		    login: baseUrl + 'community_login/',
		    postgres: baseUrl + 'postgres/',
		    home: baseUrl + 'overview/',
	    }
  	},
})

