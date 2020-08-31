<template>
	<v-container fluid grid-list-md>
    	<v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Report page: {{this.$route.params.id}}
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
        	<v-layout row>
        	<v-flex>
        	<v-card flat>
		        <v-card-text class="machine-main-text">
		          Farmer: <u> <router-link :to="{path: '/machine/'+ id }"> {{ alias }} </router-link> </u> <br>
		          Owner: {{owner}} 
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          Branch: {{branch}} <br>
		          Commit: <a :href=commit target="_blank"> <u>{{ commit.substring(63, 70) }} </u></a>
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          Uploaded: {{date}} <br>
		          Repository: {{git_repo}} 
		        </v-card-text>
		    </v-card>
		</v-flex>
    </v-layout>
    </v-card>
    <v-layout>
      <v-flex d-flex sm7 md4>
              	<v-layout column>
	                <v-card flat class="profile-left-top" min-width=15>
	                  <v-card-title>
                    	Type: {{type}} <br>
                  	  </v-card-title> 
	                </v-card>
	                <v-card flat class="profile-left-bottom" min-width=15>
	                	<v-card-text class="profile-left-text">
	                      <v-icon color="rgb(51, 103, 145)">computer</v-icon> OS: {{os}} <br>
	                      <v-icon color="rgb(51, 103, 145)">border_all</v-icon> Compiler: {{compiler}} <br>
	                      <v-icon color="rgb(51, 103, 145)">dvr</v-icon> Kernel: {{ kernel }} <br> 
	                      <v-icon color="rgb(51, 103, 145)">memory</v-icon> Memory: {{ parseFloat(memory).toFixed(2) }} GB <br> 
	                      <v-icon color="rgb(51, 103, 145)">swap_horiz</v-icon> Swap: {{ parseFloat(swap).toFixed(2) }} GB <br> 
	                      <v-icon color="rgb(51, 103, 145)">developer_board</v-icon> CPU: {{ cpu }} <br> <br>
	                	</v-card-text>
	                </v-card>
            	</v-layout>
      </v-flex>
      <v-flex fluid>
          	<v-card flat class="profile-card-title">
		
				<template class="tabs">
					<v-tabs
					  v-model="tab"
					  class="tabs"
					>
					  <v-tabs-slider color="white"></v-tabs-slider>

					  <v-tab v-for="item in settings" :key="item">
						{{ item }}
					  </v-tab>

					</v-tabs>
				</template>
				
                	<v-tabs-items v-model="tab" class="tabs-div">

	                 	<!-- results -->
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Progress for each iteration, showing latency and TPS. </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Configuration </b> </th>
										    		<th class="mounts-h"> <b> Start time </b> </th>
										    		<th class="mounts-h"> <b> Link </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in benchmarks" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.config}} </td>
													<td class="mounts-d"> {{item.start}} </td>
												    <td class="mounts-d"> <u> <router-link :to="{path: '/result/'+ item.id }"> {{ item.id }} </router-link> </u> </td>
										  		</tr>
		                    	</table>
		                    	</v-card-text>
	                    	</v-card>
	                  	</v-tab-item>
		                <!-- sysctl -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title class="results-card-title">
		                    		Displayed below is information about the sysctl settings.
		                    	</v-card-title>
		                    	<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Parameter </b> </th>
										    		<th class="mounts-h"> <b> Value </b> </th>
										  </tr>
										  		<tr v-for="(value, name) in sysctl" :key="name" class="mounts-r">
													<td class="mounts-d"> {{name}} </td>
												    <td class="mounts-d"> {{value}} </td>
										  		</tr>
		                    		</table>
		                    	</v-card-text>

		                    </v-card>
		                </v-tab-item>

		                <!-- postgres -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title class="results-card-title">
		                    		Displayed below is information about the Postgres settings.
		                    	</v-card-title>
		                    	<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Name </b> </th>
										    		<th class="mounts-h"> <b> Unit </b> </th>
											    	<th class="mounts-h"> <b> Value </b> </th>
											    	
										  	
										  </tr>
										  		<tr v-for="(item, i) in postgres_settings" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.setting_name}} </td>
												    <td class="mounts-d"> {{item.setting_unit}} </td>
												    <td class="mounts-d"> {{item.setting_value}} </td>
												   
										  		</tr>

		                    	</table>
		                    	</v-card-text>
		                    </v-card>
		                 </v-tab-item>

		                  <!-- mounts -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title class="results-card-title">
		                    		Displayed below is information about the mounts of the hardware.
		                    	</v-card-title>
		                    	<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> OPTS </b> </th>
										    		<th class="mounts-h"> <b> Device </b> </th>
											    	<th class="mounts-h"> <b> FStype </b> </th>
											    	<th class="mounts-h"> <b> Mountpoint </b> </th>
										  	
										  </tr>
										  		<tr v-for="(mount, i) in mounts" :key="i" class="mounts-r">
													<td class="mounts-d"> {{mount.opts}} </td>
												    <td class="mounts-d"> {{mount.device}} </td>
												    <td class="mounts-d"> {{mount.fstype}} </td>
												    <td class="mounts-d"> {{mount.mountpoint}} </td>
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
		name: 'Run',

		data: () => ({

			tab: null,

			settings: ['Results', 'Sysctl', 'Postgres', 'Mounts'],

	        alias: '',
	        os: '',
	        id: '',
	        compiler: '',
	        owner: '',
	        branch: '',
	        date: '',
	        commit: '',
	        previous: '',
	        git_repo: '',
	        kernel: '',
	        type: '',
	        memory: '',
	        swap: '',
	        cpu: '',
	        sysctl: '',
	        mounts: '',
	        postgres_settings : '',
	        benchmarks: [],

		}),

		methods: {

			getRun() {

				var id = this.$route.params.id;
				var url = this.$store.state.endpoints.run + id;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response)[0];

							this.run = response;

		        			this.branch = response.git_branch_id__name;
		        			this.commit = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + response.git_commit;
		        			this.date = new Date(response.add_time);
		        			this.owner = response.machine_id__owner_id__username;
		        			this.alias = response.machine_id__alias;
		        			this.git_repo = response.git_branch_id__git_repo_id__url;
		        			this.id = response.machine_id;

		        			this.kernel = response.os_kernel_version_id__kernel_id__kernel_name + ' ' + response.os_kernel_version_id__kernel_release;
		        			this.os = response.os_version_id__dist_id__dist_name + ' ' + response.os_version_id__release;
		        			this.compiler = response.compiler_id__compiler;
		        			this.type = response.machine_id__machine_type;

		        			this.memory = response.hardware_info_id__total_memory / 1073741824;
		        			this.swap = response.hardware_info_id__total_swap / 1073741824;
		        			this.cpu = response.hardware_info_id__cpu_brand + ', ' + response.hardware_info_id__cpu_cores + ' cores';

		        			if (this.swap == 0) {
				  				this.swap = "not available";
				  			}

		        			this.mounts = response.hardware_info_id__mounts;
		        			this.sysctl = response.hardware_info_id__sysctl;
		        			this.postgres_settings = response.postgres_info;

		        			for (let i = 0; i < response.pgbench_result.length; i++) {

		        				var read_only = '';

								if (response.pgbench_result[i].benchmark_config[0].read_only == true) {
									read_only = "read-only test";
								}

								else {
									read_only = "read-write test";
								}

		        				var config = 'Scale ' + response.pgbench_result[i].benchmark_config[0].scale + ', duration ' + response.pgbench_result[i].benchmark_config[0].duration + ', clients ' + response.pgbench_result[i].benchmark_config[0].clients + ', ' + read_only;

		        				var date = new Date(response.pgbench_result[i].start * 1000).toLocaleString();

		        				var json = {
		        					"config": config,
		        					"id": response.pgbench_result[i].pgbench_result_id,
		        					"start": date,
		        				}
		        				this.benchmarks.push(json);
		        			}
		        		}
		        		else {
							console.log(httpRequest.status);
						}
					}
				}
			},

			downloadJSON() {
				const url = window.URL.createObjectURL(new Blob([JSON.stringify(this.run, null, 2)], {type: 'application/json'}));
			    const link = document.createElement('a');
			    link.href = url;
			    link.setAttribute('download', 'run.json');
			    document.body.appendChild(link);
			    link.click();
    		},

		},

		mounted() {
			this.getRun();
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