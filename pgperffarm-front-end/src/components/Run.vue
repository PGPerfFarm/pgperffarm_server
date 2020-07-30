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
		          Farmer: {{alias}} <br>
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
		          Date: {{date}} <br>
		          Repository: {{git_repo}} 
		        </v-card-text>
		    </v-card>
		</v-flex>
         </v-layout>
     </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top" min-width=15>
	                  <v-card-title>
                    	Type: {{type}} <br>
                  	  </v-card-title> 
	                </v-card>
	                <v-card flat class="profile-left-bottom" min-width=15>
	                	<v-card-text>
	                      <v-icon color="rgb(51, 103, 145)">computer</v-icon> OS: {{os}} <br>
	                      <v-icon color="rgb(51, 103, 145)">border_all</v-icon> Compiler: {{compiler}} <br>
	                      <v-icon color="rgb(51, 103, 145)">dvr</v-icon> Kernel: {{ kernel }} <br> 
	                      <v-icon color="rgb(51, 103, 145)">memory</v-icon> Memory: {{ memory }} <br> 
	                      <v-icon color="rgb(51, 103, 145)">swap_horiz</v-icon> Swap: {{ swap }} <br> 
	                      <v-icon color="rgb(51, 103, 145)">developer_board</v-icon> CPU: {{ cpu }} <br> <br>
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
                    <v-tab> <span style="color: white"> Results </span> </v-tab>
                    <v-tab> <span style="color: white"> Sysctl </span> </v-tab>
                    <v-tab> <span style="color: white"> Postgres </span> </v-tab>
                    <v-tab> <span style="color: white"> Mounts </span> </v-tab>

                	<v-tabs-items>

	                 	<!-- results -->
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Progress for each iteration, showing latency and TPS. </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Configuration </b> </th>
										    		<th class="mounts-h"> <b> Link </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in benchmarks" :key="i" class="mounts-r">
													<td class="mounts-d"> {{item.config}} </td>
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
										  		<tr v-for="(value, name) in sysctl" :key="value" class="mounts-r">
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
										  		<tr v-for="item in postgres_settings" :key="item" class="mounts-r">
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
              	</v-tabs>
          	</v-card>
      	</v-flex>
    </v-layout>
  </v-layout>
  </v-container>
	

</template>

<script>
	import axios from 'axios';
	import ResultsTable from './ResultsTable.vue'

	export default {
		name: 'Run',
		components: {
			ResultsTable
		},

		data: () => ({

	        alias: '',
	        os: '',
	        compiler: '',
	        owner: '',
	        email: '',
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

				axios.get(url)
        		.then((response) => {

        			this.branch = response.data.git_branch.name;
        			this.commit = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + response.data.git_commit;
        			this.date = response.data.add_time;
        			this.owner = response.data.machine.owner.username;
        			this.alias = response.data.machine.alias;
        			this.email = response.data.machine.owner.email;
        			this.git_repo = response.data.git_repo.url;
        			this.farmer = response.data.machine.alias;

        			this.kernel = response.data.os_kernel.kernel.kernel_name + ' ' + response.data.os_kernel.kernel_release;
        			this.os = response.data.os_version.dist.dist_name + ' ' + response.data.os_version.release;
        			this.compiler = response.data.compiler.compiler;
        			this.type = response.data.machine.machine_type;

        			this.memory = response.data.hardware_info.total_memory;
        			this.swap = response.data.hardware_info.total_swap;
        			this.cpu = response.data.hardware_info.cpu_brand + ', ' + response.data.hardware_info.cpu_cores + ' cores';

        			this.mounts = response.data.hardware_info.mounts;
        			this.sysctl = response.data.hardware_info.sysctl;
        			this.postgres_settings = response.data.postgres_info.settings;

        			for (let i = 0; i < response.data.pgbench_result.length; i++) {
        				var config = 'Scale ' + response.data.pgbench_result[i].benchmark_config.scale + ', duration ' + response.data.pgbench_result[i].benchmark_config.duration + ', clients ' + response.data.pgbench_result[i].benchmark_config.clients + ', read-only ' + response.data.pgbench_result[i].benchmark_config.read_only;

        				var json = {
        					"config": config,
        					"id": response.data.pgbench_result[i].pgbench_result_id
        				}
        				this.benchmarks.push(json);
        			}

			      
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