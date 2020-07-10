<template>
	<v-container fluid grid-list-md>
    	<v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Report page: machine alias
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
     		</v-card>
    	<v-layout>
      		<v-flex d-flex xs12 sm6 md3>
            	<v-layout column>
	                <v-card flat class="profile-left-top" min-width=15>
	                	<v-card-title>
		                  	Owner:  <br>
	                    	Runs:  <br>
                  	  	</v-card-title> 
	                </v-card>
	                <v-card flat class="profile-left-bottom" min-width=15>
	                	<v-card-text>
	                    	<v-icon color="rgb(51, 103, 145)">computer</v-icon> OS:  <br>
	                    	<v-icon color="rgb(51, 103, 145)">border_all</v-icon> Processor:  <br>
	                    	<v-icon color="rgb(51, 103, 145)">email</v-icon> Email:  <br> <br>
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
                    <v-tab v-for="item in branches":key="item"> <span style="color: white"> {{ item }} </span> </v-tab>
                    
                	<v-tabs-items>
   
		                <v-tab-item v-for="(item, index) in branches" v-bind:key="item">
		                    <v-card flat id="plot">
		                    	

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

	export default {
		name: 'Results',

		data: () => ({

			latencies: [],
			commits: [],
			runs: [],
			branches: ['Head', '10 stable', '9.6 stable', '9.5 stable'],
		}),

		methods: {

			getResult() {

				var url = this.$store.state.endpoints.record;

				axios.get(url)
        		.then((response) => {

        			var report = response.data.results;
        			//this.report = report;

        			var n = 1;

        			for (let run in report) {
        				var latency = 0;
        				this.commits.push(report[run].git_commit.substring(33, 40))
        				for (let i in report[run].pgbench_result) {
	        				latency += report[run].pgbench_result[i].latency;
	        				n++;
        				}

        				this.latencies.push(latency / n);

        			}

        			this.runs = Array.from(Array(this.latencies.length).keys())

        			var data = {
						x: this.runs,
						y: this.latencies,
						mode: 'lines+markers+text',
						text: this.commits,
						textposition: top,
						marker: {
							color: 'rgb(128, 0, 128)',
							size: 10
						},
						line: {
							color: 'rgb(128, 0, 128)',
							width: 2
						}

					};
        			
        			var layout = {
        				title: 'Average latency between PgBench executions',
        				xaxis: {
        					title: 'Run'
        				},
        				yaxis: {
        					title: 'Latency'
        				}
        			};


					Plotly.newPlot(document.getElementById('plot'), [data], layout);

			      
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