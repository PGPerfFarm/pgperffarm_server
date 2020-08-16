<template>

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
							<v-card flat id="Head" class="branch" :key="1">	
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat id="13_stable" class="branch" :key="2">	
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat id="12_stable" class="branch" :key="3">	
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat id="11_stable" class="branch" :key="4">	
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat id="10_stable" class="branch" :key="5">	
							</v-card>
						</v-tab-item>

					</v-tabs-items>
				</v-tabs>

			</v-card>
</template>

<script>
	import Plotly from 'plotly.js-dist'

	// same machine, same benchmark configuration, same postgres settings, same os configuration, same git repository

	// machine, benchmark: user defined parameters
	// results/benchmark/machine

	export default {
		name: 'Plots',

		data: () => ({

			avg_latencies: [[], [], [], [], []],
			avg_tps: [[], [], [], [], []],
			std_latencies: [[], [], [], [], []],
			std_tps: [[], [], [], [], []],
			commits: [[], [], [], [], []],

			branches: ['Head', '13 stable', '12 stable', '11 stable', '10 stable'],
			
		}),

		methods: {

			getPlots() {

				var url = this.$store.state.endpoints.trends + this.$route.params.id + '/' + this.$route.params.config;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							var main = response.results[0];
							this.$store.commit('setPgBenchResults', main);

							var machine_id = response.results[0].machine_id;
							var config_id = response.results[0].pgbench_benchmark_id;

							var branches_raw = ['master', 'REL_13_STABLE', 'REL_12_STABLE', 'REL_11_STABLE', 'REL_10_STABLE'];
							var max_length = 20;

							for (let run = 0; run < response.results.length; run++) {

								for (let i = 0; i < 5; i++) {

									if (branches_raw[i] == response.results[run].name) {

										if (this.commits[i].length < max_length) {

											this.avg_latencies[i].push(response.results[run].avglat);
											this.std_latencies[i].push(response.results[run].stdlat);
											this.avg_tps[i].push(response.results[run].avgtps);
											this.std_tps[i].push(response.results[run].stdtps);
											this.commits[i].push(response.results[run].git_commit.substring(30, 40));

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
									x: this.commits[j],
									y: this.avg_latencies[j],
									mode: 'lines+markers',
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
									x: this.commits[j],
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
									x: this.commits[j],
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
									x: this.commits[j],
									y: this.std_tps[j],
									yaxis: 'y2',
									mode: 'lines+markers',
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
									title: 'Commit'
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


							Plotly.newPlot(document.getElementById("Head"), data[0], layout, {responsive: true});
							Plotly.newPlot(document.getElementById("13_stable"), data[1], layout, {responsive: true});
							Plotly.newPlot(document.getElementById("12_stable"), data[2], layout, {responsive: true});
							Plotly.newPlot(document.getElementById("11_stable"), data[3], layout, {responsive: true});
							Plotly.newPlot(document.getElementById("10_stable"), data[4], layout, {responsive: true});

							var router = this.$router;

							document.getElementById("Head").on('plotly_click', function(data) {

								var commit = '';
							
								for (let i = 0; i < data.points.length; i++) {
									commit = data.points[i].text;
								}

								var detail = config_id + '/detail/' + commit + '/' + machine_id + '/' + config_id;
								router.push(detail);
								
							});

							document.getElementById("13_stable").on('plotly_click', function(data) {

								var commit = '';
							
								for (let i = 0; i < data.points.length; i++) {
									commit = data.points[i].text;
								}

								var detail = config_id + '/detail/' + commit + '/' + machine_id + '/' + config_id;
								router.push(detail);
								
							});

							document.getElementById("12_stable").on('plotly_click', function(data) {

								var commit = '';
							
								for (let i = 0; i < data.points.length; i++) {
									commit = data.points[i].text;
								}

								var detail = config_id + '/detail/' + commit + '/' + machine_id + '/' + config_id;
								router.push(detail);
								
							});

							document.getElementById("11_stable").on('plotly_click', function(data) {

								var commit = '';
							
								for (let i = 0; i < data.points.length; i++) {
									commit = data.points[i].text;
								}

								var detail = config_id + '/detail/' + commit + '/' + machine_id + '/' + config_id;
								router.push(detail);
								
							});

							document.getElementById("10_stable").on('plotly_click', function(data) {

								var commit = '';
							
								for (let i = 0; i < data.points.length; i++) {
									commit = data.points[i].text;
								}

								var detail = config_id + '/detail/' + commit + '/' + machine_id + '/' + config_id;
								router.push(detail);
								
							});
						}
						else {
							console.log(httpRequest.status);
						}
					}
				}
			},

		},

		mounted() {
			this.getPlots();
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