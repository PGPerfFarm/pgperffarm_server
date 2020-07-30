<template>
	<v-container fluid grid-list-md>
    	<v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Average TPS and latency in milliseconds: {{ alias }}
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
      				<v-btn class="login-button" >View OS settings</v-btn>
      				<v-btn class="login-button" >View Postgres settings</v-btn>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
     		</v-card>
    	<v-layout>
      		<v-flex d-flex xs12 sm6 md3>
            	<v-layout column>
	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-title>
		                  	Owner: {{ owner }} <br>
		                  	Email: {{ email }} <br>
	                    	Total runs: {{ number_runs }} <br>
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
		                  	Clients: <br>
		                  	Scale: <br>
		                  	Duration: <br>
		                  	Read-only: <br> <br>
		                  	<v-btn icon absolute left> <v-icon color="white">arrow_back_ios</v-icon> </v-btn> <v-btn icon absolute right> <v-icon color="white">arrow_forward_ios</v-icon> </v-btn> <br> <br>
                  	  	</v-card-text> 
	                </v-card>
            	</v-layout>
      		</v-flex>
      		<v-flex d-flex fluid>
          		<v-card flat class="profile-card-title">
                
            	<v-tabs
            		dark
            		height=70
                    align-with-title
                >
                    <v-tabs-slider color="white"></v-tabs-slider>
                    <v-tab v-for="item in branches" :key="item"> <span style="color: white"> {{ item }} </span> </v-tab>
                    
                	<v-tabs-items>
   
		                <v-tab-item>
		                    <v-card flat id="Head">	
		                    </v-card>
		                </v-tab-item>

		                <v-tab-item>
		                    <v-card flat id="13_stable">	
		                    </v-card>
		                </v-tab-item>

		                <v-tab-item>
		                    <v-card flat id="12_table">	
		                    </v-card>
		                </v-tab-item>

		                <v-tab-item>
		                    <v-card flat id="11_stable">	
		                    </v-card>
		                </v-tab-item>

		                <v-tab-item>
		                    <v-card flat id="10_stable">	
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
	import axios from 'axios'
	import Plotly from 'plotly.js-dist'

	// same machine, same benchmark configuration, same postgres settings, same os configuration, same git repository

	// machine, benchmark: user defined parameters
	// results/benchmark/machine

	export default {
		name: 'Trend',

		data: () => ({

			latencies: [[], [], [], [], []],
			tps: [[], [], [], [], []],
			commits: [[], [], [], [], []],
			runs: [0, 0, 0, 0, 0],
			branches: ['Head', '13 stable', '12 stable', '11 stable', '10 stable'],
			alias: '',
			owner: '',
			number_runs: '',
			compiler: '',
			os: '',
			email: '',
			
		}),

		methods: {

			getTrend() {

				var url = this.$store.state.endpoints.record + this.$route.params.id;
				console.log(url)

				axios.get(url)
        		.then((response) => {

        			var report = response.data.runs;

        			this.alias = response.data.alias;
        			this.owner = response.data.owner.username;
        			this.email = response.data.owner.email;

        			this.os = response.data.runs[0].os_version.dist.dist_name + ' ' + response.data.runs[0].os_version.release + ' ' + response.data.runs[0].os_version.codename;

        			this.compiler = response.data.runs[0].compiler.compiler;
        			this.number_runs = response.data.runs.length

        			var branches_raw = ['master', 'REL_13_STABLE', 'REL_12_STABLE', 'REL_11_STABLE', 'REL_10_STABLE'];

        			var max_length = 30;
        			if (max_length > report.length)
        				max_length = report.length;

        			for (let run = 0; run < max_length; run++) {

        				var latency = 0;
        				var tps = 0;

        				var benchmarks = 0;

        				for (let j = 0; j < 5; j++) {
        					if (branches_raw[j] == report[run].git_branch.name) {

        						//if this.commits[j].includes(report[run].git_commit) {

	        						this.commits[j].push(report[run].git_commit.substring(33, 40));

	        						for (let i in report[run].pgbench_result) {
		        						latency += report[run].pgbench_result[i].latency;
		        						tps += report[run].pgbench_result[i].tps;
		        						benchmarks++;
	        						}

	        						this.runs[j]++;

	        						this.latencies[j].push(latency / benchmarks);
	        						this.tps[j].push((tps / benchmarks) / 1000);
	        					}
        					//}

        				}
        			}

        			for (let j = 0; j < 5; j++) {
        				this.commits[j].reverse();
        				this.latencies[j].reverse();
        				this.tps[j].reverse();
        			}

        			var data = [[], [], [], [], []];

        			console.log(this.runs);

        			for (let j = 0; j < 5; j++) {

        				var latency_line = {
							x: this.runs[j],
							y: this.latencies[j],
							mode: 'lines+markers',
							text: this.commits[j],
							marker: {
								color: '#336791',
								size: 10
							},
							line: {
								color: '#336791',
								width: 2
							},
							name: 'Latency'

						};

						var tps_line = {
							x: this.runs[j],
							y: this.tps[j],
							yaxis: 'y2',
							mode: 'lines+markers+text',
							text: this.commits[j],
							textposition: 'top center',
							marker: {
								color: '#a6c5e0',
								size: 10
							},
							line: {
								color: '#a6c5e0',
								width: 2
							},
							name: 'TPS'

						};
        			
	        			data[j] = [latency_line, tps_line];
        			}

        			var title = 'Git repository: ' + response.data.runs[0].git_repo.url

        			var layout = {
        				title: {
        					text: title,
    						x: 0.05,
        				},
	        			xaxis: {
	        				title: 'Run'
	        			},
	        			yaxis: {
	       					title: 'Latency'
	       				},
	       				yaxis2: {
	       					title: 'TPS',
	       					showgrid: false,
	       					overlaying: 'y',
    						side: 'right'
	       				},
	       				legend: {
						    x: 1,
						    xanchor: 'right',
						    y: 1.25,
						    orientation: "h"
						},
	        		};

	        		console.log(data[0])

        			Plotly.newPlot(document.getElementById("Head"), data[0], layout, {responsive: true});
        			Plotly.newPlot(document.getElementById("13_stable"), data[1], layout, {responsive: true});
        			Plotly.newPlot(document.getElementById("12_table"), data[2], layout, {responsive: true});
        			Plotly.newPlot(document.getElementById("11_stable"), data[3], layout, {responsive: true});
        			Plotly.newPlot(document.getElementById("10_stable"), data[4], layout, {responsive: true});
			      
        		})
        		.catch((error) => {
          			console.log(error);
        		})

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