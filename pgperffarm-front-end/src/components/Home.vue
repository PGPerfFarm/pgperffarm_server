<template>
	<v-container fluid grid-list-md>
		<v-layout column align-center>
	  		<v-card flat class="pg-v-card">
				<v-card-title class="pg-v-card-text-main">
					Welcome to the Postgres Performance Farm!
				</v-card-title>
				<v-card-text class="pg-v-card-text">
		 			The Postgres Performance Farm is a project aiming to collect results of performance tests through source code updates, highlighting trends and changes.
				</v-card-text>
	  		</v-card>
	  		<v-container fluid>
				<v-layout>
	 				<v-flex md7>
						<v-layout column>
							<v-card flat class="home-card-left" min-width=15>
								<v-card-text class="home-card-text">
									{{ machines }} machines belonging to {{ users }} users <br>
									of which {{ last_month }} reported in the last month
								</v-card-text> 
							</v-card>
					
							<v-card flat class="home-card-left" min-width=15>
								<v-card-text class="home-card-text">
									{{ branches }} reporting branches <br>
									from {{ repos }} different Postgres repositories
								</v-card-text> 
							</v-card>
					
							<v-card flat class="home-card-left" min-width=15>
								<v-card-text class="home-card-text">
									{{ configs }} different PgBench configurations <br>
									{{ os }} different operating systems
								</v-card-text> 
							</v-card>
						</v-layout>
	 				</v-flex>

	  				<v-flex md7>
						<v-layout column>
							<v-card flat class="home-card-right" min-width=15>
								<v-card-text class="home-card-text">
									{{ runs }} total runs <br>
									{{ benchmarks }} total benchmarks
								</v-card-text> 
							</v-card>
					
							<v-card flat class="home-card-right" min-width=15>
								<v-card-text class="home-card-text">
									Last run: <u> <a :href="'/run/'+ last_run"> {{ last_run }}</a> </u> on {{ last_run_time }} <br>
									Reported by machine {{ last_run_machine }}
								</v-card-text> 
							</v-card>
					
							<v-card flat class="home-card-right" min-width=15>
								<v-card-text class="home-card-text">
									<u> <router-link :to="{path: '/trend/' + benchmark_machine + '/' + benchmark}"> Last run trends </router-link> </u> <br>
									Scale {{ scale }}, duration {{ duration }}, clients {{ clients }}, {{ read_only }}
								</v-card-text> 
							</v-card>
						</v-layout>
	  				</v-flex>
	  
				</v-layout>
			</v-container>
		</v-layout>
	</v-container>
</template>

<script>

	export default {
		name: 'Home',

		data: () => ({
			
			runs: '',
			benchmarks: '',
			last_run: '',
			last_run_machine: '',
			last_run_time: '',
			os: '',
			machines: '',
			users: '',
			last_run_machine_id: '',
			last_month: '',
			configs: '',
			branches: '',
			repos: '',

			benchmark: '',
			scale: '',
			clients: '',
			duration: '',
			read_only: '',
			benchmark_machine: '',
				
		}),

		methods: {

			getHome() {

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", this.$store.state.endpoints.home);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							this.runs = response.results[0].runs;
							this.benchmarks = response.results[0].results_count;

							this.last_run = response.results[0].last_run;
							this.last_run_machine = response.results[0].last_machine_alias;
							this.last_run_machine_id = response.results[0].last_machine_id;
							this.last_run_time = new Date(response.results[0].last_run_time).toString().substring(0, 25);
							this.last_month = response.results[0].recent_runs;

							this.os = response.results[0].os_count;
							this.machines = response.results[0].machines_count;
							this.users = response.results[0].users;

							this.repos = response.results[0].repos;
							this.branches = response.results[0].branches;
							this.configs = response.results[0].configs;

							this.benchmark = response.results[0].pgbench_benchmark_id;
							this.clients = response.results[0].clients;
							this.scale = response.results[0].scale;
							this.duration = response.results[0].duration;

							if (response.results[0].read_only == false) {
								this.read_only = 'read-only test';
							}
							else {
								this.read_only = 'read-write test';
							}

							this.benchmark_machine = response.results[0].machine_id_id;

						} 
						else {
							console.log(httpRequest.status);
						}
					}
				}
			}
		},

		mounted() {
			this.getHome();
		}
	}

</script>