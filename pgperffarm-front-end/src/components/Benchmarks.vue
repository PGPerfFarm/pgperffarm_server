<template>
	<v-app>
		<main>
			<v-content>
				<v-layout justify-center column my-4>
					<v-flex>
						<v-card flat class="pg-v-card">
							<v-card-text class="pg-v-card-text-main">
								Benchmarks page
							</v-card-text>
						</v-card>
					</v-flex>
					<v-flex>
						<v-layout row class="status-layout">
							<v-card flat>
								<v-card-title class="table-title">
									Shown here is the list of different benchmark configurations as well as all machines which reported a run using them. Use the machine link for history of that member on the relevant configuration.
								</v-card-title>
							</v-card>
							<v-card flat>
								<v-btn @click="all">All</v-btn>
								<v-btn @click="none">None</v-btn>
							</v-card>
						</v-layout>
						<v-card flat class="pg-v-card">
							<template>
								<v-expansion-panel
								  expand
								  v-model="panel">
									<v-expansion-panel-content 
									 class="status-content"
									 v-for="(value, name) in machines"
									 :key="name">
										<template v-slot:header>
											<div class="panel-div"> {{ name }} </div>
										</template>
										<v-card>
											<template>
												<v-data-table
												 v-bind:headers="headers"
												:items="machines[name]"
												hide-actions
												:loading="loading"
												item-key="alias"
												class="elevation-1"
												>
													<template v-slot:items="props">
														<tr>
															<td class="profile-td"><u> <router-link :to="{path: '/machine/' + props.item.id}"> {{ props.item.alias }} </router-link> </u></td>
															<td class="profile-td">{{ props.item.add_time }}</td>
															<td class="profile-td">{{ props.item.type }}</td>
															<td class="profile-td">{{ props.item.owner }}</td>
															<td class="profile-td">{{ props.item.count }}</td>
															<td class="profile-td"> <u> <router-link :to="{path: '/trend/' + props.item.id + '/' + props.item.config_id}"> link </router-link> </u> </td>
														</tr>
													</template>
												</v-data-table>
											</template>
										</v-card>
									</v-expansion-panel-content>
								</v-expansion-panel>
							</template>
						</v-card>
					</v-flex>
				</v-layout>
			</v-content>
		</main>
	</v-app>
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
				{ text: 'Trend', align: 'center', value: 'trend'},
			],
		}),

		methods: {

			toggleAll() {
				if (this.selected.length) this.selected = []
				else this.selected = this.machines.slice()
			  },

			changeSort(column) {
				if (this.pagination.sortBy === column) {
				  this.pagination.descending = !this.pagination.descending
				} 
				else {
				  this.pagination.sortBy = column
				  this.pagination.descending = false
				}
			},

			all () {

				for (var i = 0; i < Object.keys(this.machines).length; i++) {
					this.panel.push(true)
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

								var benchmark = 'Scale ' + response.results[i].scale + ', duration ' + response.results[i].duration + ', clients ' + response.results[i].clients + ', read-only ' + response.results[i].read_only;

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
								}

								this.machines[benchmark].push(machine);

							}

							this.loading = false;
							this.panel.push(true);
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