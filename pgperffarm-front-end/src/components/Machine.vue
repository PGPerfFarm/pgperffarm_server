<template>
	<v-container fluid grid-list-md>
	<v-layout column>
	  <v-card class="machine-main-card">
		<v-card-title class="machine-main-title">
		  Machine page: {{ alias }}
		<v-spacer></v-spacer>
        <v-btn class="login-button" :href="'/postgres/'+ id"> View Postgres history </v-btn>
        </v-card-title>
	  </v-card>
	<v-layout>
	  <v-flex d-flex sm7 md4>
				<v-layout column>
					<v-card flat class="profile-left-top" min-width=15>
						<v-card-title>
						  	Type: {{ type }}  <br>
							Reports: {{ reports }} <br>
						 	{{ branches.length }} branch(es) involved
				  		</v-card-title> 
					</v-card>
					<v-card class="profile-left-bottom" min-width=15>
						<v-card-text class="profile-left-text">
					  <v-icon color="rgb(51, 103, 145)">account_circle</v-icon> Owner: {{ owner }} <br>
					  <v-icon color="rgb(51, 103, 145)">schedule</v-icon> Add time: {{ add_time }} <br>
						</v-card-text>
					</v-card>
					<v-card flat class="profile-left-top" min-width=15>
						<v-card-title>
						 	Available configurations
				  		</v-card-title> 
					</v-card>
					<v-card min-width=15 class="profile-left-bottom">
						<v-card-text class="profile-left-text" v-for="(value, name) in benchmarks" :key="name">
						<u> <router-link :to="{path: '/trend/'+ id + '/' + name }"> {{ value }} </router-link> </u>
						</v-card-text>
					</v-card>
				</v-layout>
	  </v-flex>
	  <v-flex fluid>
		  <v-card flat class="machine-card">
				<v-toolbar flat dark color="rgb(51, 103, 145)">
				  <v-toolbar-title><b>Machine history (reporting major changes in hardware)</b></v-toolbar-title>
				  <v-spacer></v-spacer>

				  <template v-slot:extension>
					<v-tabs
					  v-model="tab"
					>
					  <v-tabs-slider color="#d3e1ed"></v-tabs-slider>

					  <v-tab v-for="item in settings" :key="item">
						{{ item }}
					  </v-tab>
					</v-tabs>
				  </template>
				</v-toolbar>

				<v-tabs-items v-model="tab" class="tabs-div">
				  <v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> OS and kernel history, showing name and release (an entry in the table represents the first run with a new reported version). </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> OS and kernel </b> </th>
										    		<th class="mounts-h"> <b> Link </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in os_data" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.os}} </td>
												    <td class="mounts-d"> <u> <router-link :to="{path: '/run/'+ item.run_id }"> {{ item.run_id }} </router-link> </u> </td>
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Compiler history (an entry in the table represents the first run with a new reported compiler). </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Compiler </b> </th>
										    		<th class="mounts-h"> <b> First run </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in compiler_data" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.compiler}} </td>
												    <td class="mounts-d"> <u> <router-link :to="{path: '/run/'+ item.run_id }"> {{ item.run_id }} </router-link> </u> </td>
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Sysctl history (an entry in the table represents the first run with new systcl settings of interest). </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Sysctl </b> </th>
										    		<th class="mounts-h"> <b> First run </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in sysctl_data" :key="i" class="mounts-r">
													<td class="mounts-d"> <pre>{{item.sysctl}}</pre> </td>
												    <td class="mounts-d"> <u> <router-link :to="{path: '/run/'+ item.run_id }"> {{ item.run_id }} </router-link> </u> </td>
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Hardware information (static). </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    <th class="mounts-h"> <b> CPU brand </b> </th>
										    <th class="mounts-h"> <b> CPU cores </b> </th>
										    <th class="mounts-h"> <b> CPU HZ </b> </th>
										    <th class="mounts-h"> <b> Memory </b> </th>
										    <th class="mounts-h"> <b> Swap </b> </th>
										</tr>
										<tr class="mounts-r">
											<td class="mounts-d"> {{ cpu_brand }} </td>
											<td class="mounts-d"> {{ cpu_cores }} </td>
											<td class="mounts-d"> {{ hz }} </td>
											<td class="mounts-d"> {{ parseFloat(memory).toFixed(2) }} GB </td>
											<td class="mounts-d"> {{ parseFloat(swap).toFixed(2) }} GB </td>
										</tr>
		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
				</v-tabs-items>
		  </v-card>
	  </v-flex>
	</v-layout>
  </v-layout>
  </v-container>
</template>

<script>

	export default {
		name: 'Machine',

		data: () => ({
	  		tab: null,
	  		settings: ['OS', 'Compiler', 'Sysctl', 'Hardware'],

			search: '',
	 		loading: true,

	 		owner: '',
	 		reports: 0,
	 		type: '',
	 		alias: '',
	 		add_time: '',
	 		id: '',

	 		compiler_data: [],
	 		os_data: [],
	 		branches: [],
	 		sysctl_data: [],
	 		benchmarks: {},

	 		cpu_brand: '',
	 		cpu_cores: '',
	 		hz: '',
	 		memory: '',
	 		swap: '',

		}),

		methods: {

			getMachine() {

				var url = this.$store.state.endpoints.machine + this.$route.params.id;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

			  		if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {

				  			var response = JSON.parse(httpRequest.response);
				  			console.log(response);
				  			
				  			this.owner = response[0].username;
				  			this.alias = response[0].alias;
				  			this.id = response[0].machine_id;
				  			this.add_time = new Date(response[0].add_time);
				  			this.type = response[0].machine_type;

				  			this.cpu_brand = response[0].cpu_brand;
				  			this.cpu_cores = response[0].cpu_cores;
				  			this.hz = response[0].hz;
				  			this.memory = response[0].total_memory / 1073741824;
				  			this.swap = response[0].total_swap/ 1073741824;

				  			if (this.swap == 0) {
				  				this.swap = "not available";
				  			}

				  			for (let i = 0; i < response.length; i++) {

				  				this.reports += response[i].count;

				  				if (this.compiler_data == '') {
				  					this.compiler_data.push({'compiler': response[i].compiler, 'run_id': response[i].run_id});
				  				}
				  				else {
				  					if (!this.compiler_data.some(item => item.compiler === response[i].compiler)) {
				  						this.compiler_data.push({'compiler': response[i].compiler, 'run_id': response[i].run_id});
				  					}
				  				}

				  				var read_only = '';

				  				if (response[i].read_only == true) {
									read_only = "read-only";
								}

								else {
									read_only = "read-write";
								}

								var benchmark = 'Scale ' + response[i].scale + ', duration ' + response[i].duration + ', clients ' + response[i].clients + ', ' + read_only;
				  			
				  				this.benchmarks[response[i].pgbench_benchmark_id] = benchmark;

				  				var os_string = response[i].kernel_name + ' ' + response[i].dist_name + ' ' + response[i].release + ' (' + response[i].codename + ') ' + response[i].kernel_release + ' ' + response[i].kernel_version;

				  				if (this.os_data == '') {
				  					this.os_data.push({'os': os_string, 'run_id': response[i].run_id});
				  				}
				  				else {
				  					if (!this.os_data.some(item => item.os === os_string)) {
				  						this.os_data.push({'os': os_string, 'run_id': response[i].run_id});
				  					}
				  				}

				  				if (!this.branches.includes(response[i].name)) {
				  					this.branches.push(response[i].name);
				  				}

				  				var sysctl_object = response[i].sysctl;
				  				var sysctl_string = '';

				  				if (sysctl_object != null) {
					  				for (const [key, value] of Object.entries(sysctl_object)) {
					  					sysctl_string += key + ' = ' + value + '\n';
					  				}

					  				if (this.sysctl_data == '') {
					  					this.sysctl_data.push({'sysctl': sysctl_string, 'run_id': response[i].run_id});
					  				}
					  				else {
					  					if (!this.sysctl_data.some(item => item.sysctl === sysctl_string)) {
					  						this.sysctl_data.push({'sysctl': sysctl_string, 'run_id': response[i].run_id});
					  					}
					  				}
					  			}
				  			}
				  			
				  		}
				  	}
				  	else {
							console.log(httpRequest.status);
					}
				}
		  	}

		},

		mounted() {
			this.getMachine();
		}
  	}

</script>