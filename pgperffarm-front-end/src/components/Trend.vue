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
		                  	Clients: {{ clients }} <br>
		                  	Scale: {{ scale }} <br>
		                  	Duration: {{ duration }} <br>
		                  	Read-only: {{ read_only }} <br> <br>
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

			avg_latencies: [[], [], [], [], []],
			avg_tps: [[], [], [], [], []],
			std_latencies: [[], [], [], [], []],
			std_tps: [[], [], [], [], []],
			commits: [[], [], [], [], []],

			branches: ['Head', '13 stable', '12 stable', '11 stable', '10 stable'],
			alias: '',
			owner: '',
			number_runs: '',
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

				var url = this.$store.state.endpoints.trends + this.$route.params.id + '/10';
				console.log(url);
				
				axios.get(url)
        		.then((response) => {

        			console.log(response);

        			var main = response.data.results[0];

        			this.alias = main.alias;
        			this.owner = main.username;
        			this.email = main.email;

        			this.clients = main.clients;
        			this.duration = main.duration;
        			this.scale = main.scale;
        			this.read_only = main.read_only;

        			this.os = "todo";

        			this.compiler = "todo";
        			this.number_runs = response.data.count;

        			var branches_raw = ['master', 'REL_13_STABLE', 'REL_12_STABLE', 'REL_11_STABLE', 'REL_10_STABLE'];
        			var max_length = 20;

        			for (let run = 0; run < response.data.results.length; run++) {

        				for (let i = 0; i < 5; i++) {

        					if (branches_raw[i] == response.data.results[run].name) {

        						if (this.commits[i].length < max_length) {

	        						this.avg_latencies[i].push(response.data.results[run].avglat);
	        						this.std_latencies[i].push(response.data.results[run].stdlat);
	        						this.avg_tps[i].push(response.data.results[run].avgtps);
	        						this.std_tps[i].push(response.data.results[run].stdtps);
	        						this.commits[i].push(response.data.results[run].git_commit.substring(33, 40));

        						}
        					}
        				}
        			}

        			for (let j = 0; j < 5; j++) {
        				this.commits[j].reverse();
        				this.avg_latencies[j].reverse();
        				this.avg_tps[j].reverse();
        				this.std_latencies[j].reverse();
        				this.std_tps[j].reverse();
        			}

        			var data = [[], [], [], [], []];

        			for (let j = 0; j < 5; j++) {

        				var avg_latency_line = {
							x: this.commits[j].length,
							y: this.avg_latencies[j],
							mode: 'lines+markers+text',
							text: this.commits[j],
							marker: {
								color: '#12BA9E',
								size: 10
							},
							line: {
								color: '#12BA9E',
								width: 2
							},
							name: 'Average latency'

						};

						var avg_tps_line = {
							x: this.commits[j].length,
							y: this.avg_tps[j],
							yaxis: 'y2',
							mode: 'lines+markers',
							textposition: 'top center',
							marker: {
								color: '#89A6FB',
								size: 10
							},
							line: {
								color: '#89A6FB',
								width: 2
							},
							name: 'Average TPS'

						};

						var std_latency_line = {
							x: this.commits[j].length,
							y: this.std_latencies[j],
							mode: 'lines+markers',
							marker: {
								color: '#A3D9FF',
								size: 10
							},
							line: {
								color: '#A3D9FF',
								width: 2
							},
							name: 'Standard deviation latency'

						};

						var std_tps_line = {
							x: this.commits[j].length,
							y: this.std_tps[j],
							yaxis: 'y2',
							mode: 'lines+markers',
							text: this.commits[j],
							textposition: 'top center',
							marker: {
								color: '#96E6B3',
								size: 10
							},
							line: {
								color: '#96E6B3',
								width: 2
							},
							name: 'Standard deviation TPS'

						};
        			
	        			data[j] = [avg_latency_line, avg_tps_line, std_latency_line, std_tps_line];
        			}

        			var layout = {
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