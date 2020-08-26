<template>

		<v-layout justify-center column my-4>
			<v-flex>
				<v-card flat class="pg-v-card">
					<v-card-text class="pg-v-card-text-main">
						Machines list
					</v-card-text>
				</v-card>
			</v-flex>
			<v-flex>
				<v-card flat class="pg-v-card-bottom">
					<v-card-title class="table-title">Shown here is the machine list, along with a summary of relevant information.
						<v-spacer></v-spacer>
						<v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
					</v-card-title>
					<template>
						<v-data-table :headers="headers" :items="machines" hide-default-footer :search="search" :loading="loading" item-key="alias" class="elevation-1" sort-by="addDate">
							<template #item.alias="{ item }"> <router-link :to="{path: '/machine/'+ item.id }"> {{ item.alias }} </router-link> </template>
							<template #item.latest="{ item }"> <router-link :to="{path: '/runs/'+ item.latest }"> {{ item.latest }} </router-link> </template>
						</v-data-table>
					</template>
				</v-card>
			</v-flex>
		</v-layout>

</template>

<script>

	export default {
		name: 'Machines',

		data: () => ({
			search: '',
			loading: true,

			headers: [
				{ text: 'Alias', align: 'center', value: 'alias' },
				{ text: 'System', align: 'center', value: 'system' },
				{ text: 'Approved', align: 'center', value: 'approved' },
				{ text: 'Owner', align: 'center', value: 'owner' },
				{ text: 'Add date', align: 'center', value: 'addDate' },
				{ text: 'Latest run', align: 'center', value: 'latest' },
			],

			machines: [],
				
		}),

		methods: {

			getMachines() {

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", this.$store.state.endpoints.machines);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							for (var i = 0; i < response.count; i++) {

								var machine = {
									alias: response.results[i].alias,
									id: response.results[i].machine_id,
									system: response.results[i].machine_type,
									approved: response.results[i].approved,
									latest: response.results[i].latest.run_id,
									owner: response.results[i].owner.username,
									addDate: response.results[i].add_time.substring(0, 10)
								};

								this.machines.push(machine);
							}

							this.loading = false;

						} 
						else {
							console.log(httpRequest.status);
						}
					}
				}
			}
		},

		mounted() {
			this.getMachines();
		}
	}

</script>