<template>
	<v-container fluid grid-list-md>
    <v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Benchmark result page: {{this.$route.params.id}}
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
        	<v-layout row>
        	<v-flex>
        	<v-card flat>
		        <v-card-text class="machine-main-text">
		          Farmer: <u> <router-link :to="{path: '/machine/'+ id }"> {{ alias }} </router-link> </u> <br>
		          Run: <u> <router-link :to="{path: '/run/'+ run }"> {{ run }} </router-link> </u> 
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          Branch: {{ branch }} <br>
		          Commit: <u> <a> {{ commit.substring(63, 70) }} </a> </u>
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          OS: {{ os }} <br>
		          Kernel: {{ kernel }}
		        </v-card-text>
		    </v-card>
		</v-flex>
         </v-layout>
     
     </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top" min-width=15>
	                  <v-card-title>
                    	Benchmark configuration: {{config}}  <br>
                  	  </v-card-title> 
	                </v-card>
	                <v-card flat class="profile-left-bottom" min-width=15>
	                	<v-card-text class="profile-left-text">
	                		<v-icon color="rgb(51, 103, 145)">account_tree</v-icon> Clients: {{ clients }} <br>
		                  	<v-icon color="rgb(51, 103, 145)">linear_scale</v-icon> Scale: {{ scale }} <br>
		                  	<v-icon color="rgb(51, 103, 145)">timelapse</v-icon> Duration: {{ duration }} <br>
		                  	<v-icon color="rgb(51, 103, 145)">edit</v-icon> {{ read_only }} <br> <br>
	                	</v-card-text>
	                </v-card>
	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-text class="run-left-text">
	                	  Iteration: {{ iteration }} <br>
		                  TPS: {{ tps }} <br>
	                      Latency: {{ latency }} <br>
	                      Mode: {{ mode }} <br> 
	                      Init: {{ init }} <br> 
	                      Start: {{ start }} <br> 
	                      End: {{ end }} <br> <br>
                  	  	</v-card-text> 
	                </v-card>
            	</v-layout>
      </v-flex>
      <v-flex fluid>
          	<v-card flat class="profile-card-title">
                
            	<template class="tabs">
					<v-tabs
					  v-model="tab"
					  class="tabs"
					>
						<v-tabs-slider color="white"></v-tabs-slider>
	                    <v-tab> Statement latencies </v-tab>
	                    <v-tab> Log </v-tab>

                    </v-tabs>
				</template>
                   
                	<v-tabs-items v-model="tab" class="tabs-div">

	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Statement latencies for each line. </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Line </b> </th>
										    		<th class="mounts-h"> <b> Latency </b> </th>
										    		<th class="mounts-h"> <b> Statement </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in results" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.line}} </td>
													<td class="mounts-d"> {{item.latency}} </td>
													<td class="mounts-d"> {{item.statement}} </td>
												    
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Log produced with aggregate intervals of 1 second. </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Start </b> </th>
										    		<th class="mounts-h"> <b> Transactions </b> </th>
										    		<th class="mounts-h"> <b> Sum latency </b> </th>
										    		<th class="mounts-h"> <b> Sum latency 2</b> </th>
										    		<th class="mounts-h"> <b> Min latency </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in log" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.interval_start}} </td>
													<td class="mounts-d"> {{item.num_transactions}} </td>
													<td class="mounts-d"> {{item.sum_latency}} </td>
													<td class="mounts-d"> {{item.sum_latency_2}} </td>
													<td class="mounts-d"> {{item.min_latency}} </td>
													<td class="mounts-d"> {{item.max_latency}} </td>
												    
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
		                
                	</v-tabs-items>
              	</v-tabs>
          	</v-card>
      	</v-flex>
    </v-layout>
  </v-layout>
  </v-container>
	

</template>

<script>

	export default {
		name: 'Result',

		data: () => ({

			tab: null,

			alias: '',
			id: '',
	        os: '',
	        branch: '',
	        commit: '',
	        kernel: '',
	        run: '',

			tps: '',
			latency: '',
			mode: '',
			init: '',
			start: '',
			end: '',
			config: '',
			iteration: '',
			clients: '',
			scale: '',
			duration: '',
			read_only: '',
			results: {},
			log: {},

			result: '',

		}),

		methods: {

			getResult() {

				var id = this.$route.params.id;
				var url = this.$store.state.endpoints.results + id;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							this.result = response;

		        			this.clients = response.benchmark_config.clients;
		        			this.scale = response.benchmark_config.scale;
		        			this.duration = response.benchmark_config.duration;

		        			if (response.benchmark_config.read_only == true) {
								this.read_only = "Read-only test";
							}

							else {
								this.read_only = "Read-write test";
							}

		        			this.config = response.benchmark_config.pgbench_benchmark_id;

		        			this.tps = response.tps;
		        			this.latency = response.latency;
		        			this.init = response.init;
		        			this.start = new Date(response.start * 1000).toLocaleTimeString();
		        			this.end = new Date(response.end * 1000).toLocaleTimeString();
		        			this.mode = response.mode;
		        			this.iteration = response.iteration;

		        			this.alias = response.run.machine.alias;
		        			this.id = response.run.machine.machine_id;
		        			this.os = response.run.os_version.dist.dist_name + ' ' + response.run.os_version.release;
		        			this.branch = response.run.git_branch.name;
		        			this.kernel = response.run.os_kernel.kernel.kernel_name + ' ' + response.run.os_kernel.kernel_release;
		        			this.run = response.run.run_id;
		        			this.commit = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + response.run.git_commit;

		        			for (let i = 0; i < response.pgbench_run_statement.length; i++) {
		        				var result = {
		        					"line": response.pgbench_run_statement[i].line_id,
		        					"latency": response.pgbench_run_statement[i].latency,
		        					"statement": response.pgbench_run_statement[i].statements.statement
		        				};

		        				this.results[response.pgbench_run_statement[i].line_id] = result;
		        			}

		        			for (let i = 0; i < response.pgbench_log.length; i++) {
		        				var single_result = {
		        					"interval_start": new Date(response.pgbench_log[i].interval_start).toLocaleTimeString(),
		        					"num_transactions": response.pgbench_log[i].num_transactions,
		        					"sum_latency": response.pgbench_log[i].sum_latency,
		        					"sum_latency_2": response.pgbench_log[i].sum_latency_2,
		        					"min_latency": response.pgbench_log[i].min_latency,
		        					"max_latency": response.pgbench_log[i].max_latency,
		        				};

		        				this.log[response.pgbench_log[i].pgbench_log_id] = single_result;
		        			}
		        		}
		        		else {
							console.log(httpRequest.status);
						}
					}
				}
			},

			downloadJSON() {
				const url = window.URL.createObjectURL(new Blob([JSON.stringify(this.result, null, 2)], {type: 'application/json'}));
			    const link = document.createElement('a');
			    link.href = url;
			    link.setAttribute('download', 'result.json');
			    document.body.appendChild(link);
			    link.click();
    		},

		},

		mounted() {
			this.getResult();
		},

		computed: {
      		binding () {
        		const binding = {};

        		if (this.$vuetify.breakpoint.smAndDown) 
        			binding.column = true;

        	return binding
      }
    }
	}


</script>