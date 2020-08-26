<template>

				<v-layout justify-center column my-4>
					<v-flex>
						<v-card flat class="pg-v-card">
							<v-card-text class="pg-v-card-text-main">
								Benchmarks page
							</v-card-text>
						</v-card>
					</v-flex>
					<v-flex>
						<v-layout column class="status-layout">
							<v-card flat>
								<v-card-title class="table-title">
									Shown here is the list of different benchmark configurations as well as all machines which reported a run using them. Use the machine link for history of that member on the relevant configuration.
								</v-card-title>
							</v-card>
							<v-card flat>
								<v-col class="text-right">
								<v-btn class="login-button" @click="all">All</v-btn>
								<v-btn class="login-button" @click="none">None</v-btn>
							</v-col>
							</v-card>
						</v-layout>
						<v-card flat class="pg-v-card">
					
								<v-expansion-panels v-model="panel" multiple>
									<v-expansion-panel v-for="(value, name) in machines" :key="name">
										<v-expansion-panel-header class="panel-div"> {{ name }} </v-expansion-panel-header>
										<v-expansion-panel-content class="status-content">
											<v-card>
												<template>
													<v-data-table
													 v-bind:headers="headers"
													:items="machines[name]"
													hide-default-footer
													:loading="loading"
													item-key="alias"
													class="elevation-1"
													>
														<template #item.alias="{ item }"> <router-link :to="{path: '/machine/' + item.id }"> {{ item.alias }} </router-link> </template>
														<template #item.config_id="{ item }"> <router-link :to="{path: '/trend/' + item.id + '/' + item.config_id }"> link </router-link> </template>
													</v-data-table>
												</template>
											</v-card>
										</v-expansion-panel-content>
									</v-expansion-panel>
								</v-expansion-panels>
						
						</v-card>
					</v-flex>
				</v-layout>

</template>


<script>

	export default {
		name: 'Benchmarks',

		data: () => ({
			panel: [],
			machines: {},

			search: '',
			loading: true,

			headers: [
				{ text: 'Alias', align: 'center', value: 'alias' },
				{ text: 'Add time', align: 'center', value: 'add_time' },
				{ text: 'Type', align: 'center', value: 'type'},
				{ text: 'Owner', align: 'center', value: 'owner'},
				{ text: 'Count', align: 'center', value: 'count'},
				{ text: 'Trend', align: 'center', value: 'config_id'},
			],
			benchmarks: 0,
		}),

		methods: {

			all () {
				for (let i = 0; i < this.benchmarks; i++) {
					this.panel.push(i);
				}
			},
	 
			none () {
				this.panel = []
			},

			getBenchmarks() {

	  			const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", this.$store.state.endpoints.benchmarks);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {

							var response = JSON.parse(httpRequest.response);

							for (let i = 0; i < response.count; i++) {

								var read_only = '';

								if (response.results[i].read_only == true) {
									read_only = "read-only test";
								}

								else {
									read_only = "read-write test";
								}

								var benchmark = 'Scale ' + response.results[i].scale + ', duration ' + response.results[i].duration + ', clients ' + response.results[i].clients + ', ' + read_only;

								var machine = {
									alias: response.results[i].alias,
									add_time: response.results[i].add_time.substring(0, 10),
									type: response.results[i].machine_type,
									owner: response.results[i].username,
									count: response.results[i].count,
									config_id: response.results[i].pgbench_benchmark_id,
									id: response.results[i].machine_id,
								};

								if (!this.machines.hasOwnProperty(benchmark)) {
									this.machines[benchmark] = [];
									this.benchmarks++;
								}

								this.machines[benchmark].push(machine);

							}
						
							this.loading = false;
							this.panel.push(0);
						}

						else {
							console.log(httpRequest.status);
						}
					}
				}
			}
		},

		mounted() {
			this.getBenchmarks();
		}

	}
</script>