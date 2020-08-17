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
							<v-card flat>	
								<div id="Head"> </div>
								<v-card-text>
		                    		<table class="mounts-center">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Average latency </b> </th>
										    		<th class="mounts-h"> <b> STD latency </b> </th>
										    		<th class="mounts-h"> <b> Average TPS </b> </th>
										    		<th class="mounts-h"> <b> STD TPS </b> </th>
										    		<th class="mounts-h"> <b> Min latency </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										    		<th class="mounts-h"> <b> Min TPS </b> </th>
										    		<th class="mounts-h"> <b> Max TPS </b> </th>
										    		<th class="mounts-h"> <b> Commit </b> </th>
										  </tr>
										  		<tr v-for="i in master_length" :key="i" class="mounts-r">
													<td class="mounts-d"> {{ avg_latencies[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_latencies[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ avg_tps[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_tps[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_latencies[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_latencies[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_tps[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_tps[0][i].toFixed(2) }} </td>
												    <td class="mounts-d"> <a :href=commits_raw[0][i] target="_blank"> <u>{{ commits[0][i] }} </u></a> </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat>	
								<div id="13_stable"> </div>
								<v-card-text>
		                    		<table class="mounts-center">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Average latency </b> </th>
										    		<th class="mounts-h"> <b> STD latency </b> </th>
										    		<th class="mounts-h"> <b> Average TPS </b> </th>
										    		<th class="mounts-h"> <b> STD TPS </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										    		<th class="mounts-h"> <b> Min TPS </b> </th>
										    		<th class="mounts-h"> <b> Max TPS </b> </th>
										    		<th class="mounts-h"> <b> Commit </b> </th>
										  </tr>
										  		<tr v-for="i in rel_13_length" :key="i" class="mounts-r">
													<td class="mounts-d"> {{ avg_latencies[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_latencies[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ avg_tps[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_tps[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_latencies[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_latencies[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_tps[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_tps[1][i].toFixed(2) }} </td>
												    <td class="mounts-d"> <a :href=commits_raw[1][i] target="_blank"> <u>{{ commits[1][i] }} </u></a> </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat>	
								<div id="12_stable"> </div>
								<v-card-text>
		                    		<table class="mounts-center">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Average latency </b> </th>
										    		<th class="mounts-h"> <b> STD latency </b> </th>
										    		<th class="mounts-h"> <b> Average TPS </b> </th>
										    		<th class="mounts-h"> <b> STD TPS </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										    		<th class="mounts-h"> <b> Min TPS </b> </th>
										    		<th class="mounts-h"> <b> Max TPS </b> </th>
										    		<th class="mounts-h"> <b> Commit </b> </th>
										  </tr>
										  		<tr v-for="i in rel_12_length" :key="i" class="mounts-r">
													<td class="mounts-d"> {{ avg_latencies[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_latencies[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ avg_tps[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_tps[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_latencies[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_latencies[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_tps[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_tps[2][i].toFixed(2) }} </td>
												    <td class="mounts-d"> <a :href=commits_raw[2][i] target="_blank"> <u>{{ commits[2][i] }} </u></a> </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat>	
								<div id="11_stable"> </div>
								<v-card-text>
		                    		<table class="mounts-center">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Average latency </b> </th>
										    		<th class="mounts-h"> <b> STD latency </b> </th>
										    		<th class="mounts-h"> <b> Average TPS </b> </th>
										    		<th class="mounts-h"> <b> STD TPS </b> </th>
										    		<th class="mounts-h"> <b> Min latency </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										    		<th class="mounts-h"> <b> Min TPS </b> </th>
										    		<th class="mounts-h"> <b> Max TPS </b> </th>
										    		<th class="mounts-h"> <b> Commit </b> </th>
										  </tr>
										  		<tr v-for="i in rel_11_length" :key="i" class="mounts-r">
													<td class="mounts-d"> {{ avg_latencies[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_latencies[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ avg_tps[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_tps[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_latencies[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_latencies[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_tps[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_tps[3][i].toFixed(2) }} </td>
												    <td class="mounts-d"> <a :href=commits_raw[3][i] target="_blank"> <u>{{ commits[3][i] }} </u></a> </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>
							</v-card>
						</v-tab-item>

						<v-tab-item>
							<v-card flat>	
								<div id="10_stable"> </div>
								<v-card-text>
		                    		<table class="mounts-center">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Average latency </b> </th>
										    		<th class="mounts-h"> <b> STD latency </b> </th>
										    		<th class="mounts-h"> <b> Average TPS </b> </th>
										    		<th class="mounts-h"> <b> STD TPS </b> </th>
										    		<th class="mounts-h"> <b> Max latency </b> </th>
										    		<th class="mounts-h"> <b> Min TPS </b> </th>
										    		<th class="mounts-h"> <b> Max TPS </b> </th>
										    		<th class="mounts-h"> <b> Commit </b> </th>
										  </tr>
										  		<tr v-for="i in rel_10_length" :key="i" class="mounts-r">
													<td class="mounts-d"> {{ avg_latencies[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_latencies[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ avg_tps[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ std_tps[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_latencies[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_latencies[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ min_tps[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> {{ max_tps[4][i].toFixed(2) }} </td>
												    <td class="mounts-d"> <a :href=commits_raw[4][i] target="_blank"> <u>{{ commits[4][i] }} </u></a> </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>
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
			min_latencies: [[], [], [], [], []],
			max_latencies: [[], [], [], [], []],
			min_tps: [[], [], [], [], []],
			max_tps: [[], [], [], [], []],
			commits: [[], [], [], [], []],
			commits_raw: [[], [], [], [], []],
			master_length: 0,
			rel_13_length: 0,
			rel_12_length: 0,
			rel_11_length: 0,
			rel_10_length: 0,

			branches: ['Head', '13 stable', '12 stable', '11 stable', '10 stable'],

			csv_data: '',
			
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

											if (response.results[run].stdlat == null) {
												this.std_latencies[i].push(0);
											}
											else {
												this.std_latencies[i].push(response.results[run].stdlat);
											}

											if (response.results[run].stdtps == null) {
												this.std_tps[i].push(0);
											}
											else {
												this.std_tps[i].push(response.results[run].stdtps);
											}

											this.avg_tps[i].push(response.results[run].avgtps);
											this.min_tps[i].push(response.results[run].mintps);
											this.max_tps[i].push(response.results[run].maxtps);
											this.min_latencies[i].push(response.results[run].minlat);
											this.max_latencies[i].push(response.results[run].maxlat);
											this.commits[i].push(response.results[run].git_commit.substring(30, 40)).toString();
											this.commits_raw[i].push('https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + response.results[run].git_commit);

										}
									}
								}
							}

							this.master_length = this.commits[0].length - 1;
							this.rel_13_length = this.commits[1].length - 1;
							this.rel_12_length = this.commits[1].length - 1;
							this.rel_11_length = this.commits[1].length - 1;
							this.rel_10_length = this.commits[1].length - 1;

							for (let j = 0; j < 5; j++) {
								this.commits[j].reverse();
								this.avg_latencies[j].reverse();
								this.avg_tps[j].reverse();
								this.std_latencies[j].reverse();
								this.std_tps[j].reverse();
								this.commits_raw.reverse();
							}

							var data = [[], [], [], [], []];

							for (let j = 0; j < 5; j++) {

								var avg_latency_line = {
									x: this.commits[j],
									y: this.avg_latencies[j],
									error_y: {
								    	type: 'data',
    									symmetric: false, 
								    	array: this.max_latencies[j],
								    	arrayminus: this.min_latencies[j],
								    	visible: true
								    },
									mode: 'lines+markers',
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
									x: this.commits[j],
									y: this.avg_tps[j],
									error_y: {
								    	type: 'data',
    									symmetric: false, 
								    	array: this.max_tps[j],
								    	arrayminus: this.min_tps[j],
								    	visible: true
								    },
									yaxis: 'y2',
									mode: 'lines+markers',
									text: this.commits[j],
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
							
								data[j] = [avg_latency_line, avg_tps_line];
							}

							var layout = {

								xaxis: {
									title: 'Commit',
									type: 'category'
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

			downloadCSV() {

				var data = [];
				var header = ['Branch', 'Commit', 'Avg latency', 'Avg TPS', 'Std latency', 'Std TPS', 'Max latency', 'Max TPS', 'Min latency', 'Min TPS'];
				data.push(header);

				for (let j = 0; j < 5; j++) {
					for (let i = 0; i < this.commits[j].length; i++) {
						var row = [this.branches[j], this.commits_raw[j][i], this.avg_latencies[j][i], this.avg_tps[j][i], this.std_latencies[j][i], this.std_tps[j][i], this.max_latencies[j][i], this.min_latencies[j][i], this.max_tps[j][i], this.min_tps[j][i]];
						data.push(row);
					}
				}

				let csvContent = "data:text/csv;charset=utf-8," + data.map(e => e.join(",")).join("\n");
				var encodedUri = encodeURI(csvContent);
				var link = document.createElement("a");
				link.setAttribute("href", encodedUri);
				link.setAttribute("download", "trend_data.csv");
				document.body.appendChild(link); // Required for FF

				link.click(); // This will download the data file named "my_data.csv".
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