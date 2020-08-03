<template>
	<v-container fluid grid-list-md>
    	<v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Average TPS and latency in milliseconds: {{ alias }}
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
      				<v-btn class="login-button" >View history</v-btn>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
     		</v-card>
    	<v-layout>
      		<v-flex d-flex xs12 sm6 md3>
            	<v-layout column>
	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-title>
		                  	Owner: {{ owner }} <br>
		                  	Email: {{ email }} <br> <br>
                  	  	</v-card-title> 
	                </v-card>
	                <v-card flat class="run-left-bottom" min-width=15>
	                	<v-card-text>
	                		<p>
								{{ os }} <br>
	                    	</p>
	                    		{{ compiler }}
	                	</v-card-text>
	                </v-card>
	                <v-card flat class="run-left-top" min-width=15>

	                	<v-card-text>
		                  	Clients: {{ clients }} <br>
		                  	Scale: {{ scale }} <br>
		                  	Duration: {{ duration }} <br>
		                  	Read-only: {{ read_only }} <br> <br>
		                  	<!--
		                  	<v-btn icon absolute left> <v-icon color="white">arrow_back_ios</v-icon> </v-btn> <v-btn icon absolute right> <v-icon color="white">arrow_forward_ios</v-icon> </v-btn> <br> <br>
		                  -->
                  	  	</v-card-text> 
	                </v-card>
            	</v-layout>
      		</v-flex>
      		<v-flex d-flex fluid>
          		<router-view></router-view>
      	</v-flex>
    </v-layout>
  </v-layout>
  </v-container>
	

</template>

<script>
	import axios from 'axios'

	// same machine, same benchmark configuration, same postgres settings, same os configuration, same git repository

	// machine, benchmark: user defined parameters
	// results/benchmark/machine

	export default {
		name: 'Trend',

		data: () => ({
			
			alias: '',
			owner: '',
			compiler: '',
			os: '',
			email: '',

			clients: '',
			duration: '',
			scale: '',
			read_only: '',
			
		}),

		methods: {

			getTrend() {

        			var main = this.$store.getters.pgbench_results;
        			
        			this.alias = main.alias;
        			this.owner = main.username;
        			this.email = main.email;

        			this.clients = main.clients;
        			this.duration = main.duration;
        			this.scale = main.scale;
        			this.read_only = main.read_only;

        			this.os = main.kernel_name + ' ' + main.dist_name + ' ' + main.machine_type;
        			this.compiler = main.compiler;
			     
			},

			downloadJSON() {
				const url = window.URL.createObjectURL(new Blob([JSON.stringify(this.report, null, 2)], {type: 'application/json'}));
			    const link = document.createElement('a');
			    link.href = url;
			    link.setAttribute('download', 'report.json');
			    document.body.appendChild(link);
			    link.click();
    		},

		},

		mounted() {
			this.getTrend();
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