<template>
	<v-container fluid grid-list-md>
    <v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat>
      				<v-toolbar-title>
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
		          Report number: {{reports}}
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
		          Previous: <a :href="$router.resolve(previous).href"> <u> {{previous.substring(9, 16)}} </u> </a>
		        </v-card-text>
		    </v-card>
		</v-flex>
         </v-layout>
     </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>
	                  	Owner: {{owner.username}} <br>
                    	Reports: {{reports}} <br>
                  	  </v-card-title> 
	                </v-card>
	                <v-card class="profile-left-bottom">
	                	<v-card-text>
                      OS: {{os}} <br>
                      Processor: {{compiler}} <br>
                      Email: <a :href="`mailto:${owner.email}`"> {{ owner.email }} </a> <br> <br>
	                	</v-card-text>
	                </v-card>
            	</v-layout>
      </v-flex>
      <v-flex d-flex fluid>
          	<v-card flat class="profile-card-title">
                
            	<v-tabs
                    color="cyan"
                    align-with-title
                >
                    <v-tabs-slider color="yellow"></v-tabs-slider>
                    <v-tab> Progress </v-tab>
                    <v-tab> Meta information </v-tab>
                    <v-tab> Settings </v-tab>
                    <v-tab> Hardware </v-tab>
					<v-tab> Operating system </v-tab>

                	<v-tabs-items>

	                 	<!-- progress -->
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title> Progress for each test </v-card-title>
	                      		<v-container>
		                      		<v-layout row>
		                      			<v-container>
				                      		<v-layout column>
				                      			<v-flex v-for="(item, i) in this.ro" v-bind:key="item">
				                      				<v-card flat>
				                      					<results-table v-bind="data"></results-table>
				                      				</v-card>
				                      			</v-flex>
				                      		</v-layout>
			                      		</v-container>
			                      		<v-container>
				                      		<v-layout column>
				                      			<v-flex v-for="(item, i) in this.rw" v-bind:key="item">
				                      				<v-card flat>
				                      					<results-table></results-table>
				                      				</v-card>
				                      			</v-flex>
				                      		</v-layout>
			                      		</v-container>
		                      		</v-layout>
	                      	</v-container>
	                    	</v-card>
	                  	</v-tab-item>

		                <!-- meta information -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title>
		                    		Displayed below is detail about the testing meta information.
		                    	</v-card-title>
		                    	<v-card-text v-for="(item, index) in meta_info_keys" v-bind:key="item">
		                    		{{ meta_info_keys[index] }}: {{ meta_info_data[item] }}
		                    	</v-card-text>

		                    </v-card>
		                </v-tab-item>

		                <!-- settings -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title>
		                    		Displayed below is information about the testing operating settings.
		                    	</v-card-title>
		                    	<v-card-text v-for="(item, index) in pg_info_keys" v-bind:key="item">
		                    		{{ pg_info_keys[index] }}: {{ pg_info_data[item] }}
		                    	</v-card-text>

		                    </v-card>
		                </v-tab-item>

		                <!-- hardware -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title>
		                    		Displayed below is information about the testing hardware.
		                    	</v-card-title>
		                    	<template>
		                    		<pre>
		  								<v-treeview :items="hardware"></v-treeview>
		  							</pre>
								</template>
		                    </v-card>
		                 </v-tab-item>

		                  <!-- os -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title>
		                    		Displayed below is information about the testing operating system.
		                    	</v-card-title>
		                    	<template>
		                    		<pre>
		  								<v-treeview :items="os_info"></v-treeview>
		  							</pre>
								</template>
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
		name: 'Results',
		components: {
			ResultsTable
		},

		data: () => ({

			hardware: [
				{
		         	id: 1,
		          	name: 'CPU',
		          	children: [{id: 2, name: ''}]
		        },
	          	{
	          		id: 3,
		          	name: 'Memory',
		          	children: [{id: 4, name: ''}],
	          	}
	          ],

	        os_info: [
				{
		         	id: 1,
		          	name: 'Mounts',
		          	children: [{id: 2, name: ''}]
		        },
	          	{
	          		id: 3,
		          	name: 'sysctl',
		          	children: [{id: 4, name: ''}],
	          	}
	        ],

	        pg_info_data: '',
	        pg_info_keys: '',

	        meta_info_data: '',
	        meta_info_keys: '',

	        alias: '',
	        os: '',
	        compiler: '',
	        owner: {
	        	username: '',
	        	email: ''
	        },
	        reports: '',
	        branch: '',
	        date: '',
	        commit: '',
	        previous: '',

	        ro: [],
	        rw: [],

	        data: {
	        	run: 123,
	        	latency: 456
	        }

		}),

		methods: {

			getResult() {

				var id = this.$route.params.id;
				var url = this.$store.state.endpoints.record + id;

				axios.get(url)
        		.then((response) => {

        			var report = response.data;

        			this.hardware[0].children[0].name = report.hardware_info.cpuinfo.replace(/: /g, '');
        			this.hardware[1].children[0].name = report.hardware_info.meminfo.replace(/: /g, '');

        			this.os_info[0].children[0].name = report.linux_info.mounts.replace(/: /g, '');
        			this.os_info[1].children[0].name = report.linux_info.sysctl.replace(/: /g, '');

        			this.pg_info_data = report.pg_info;
        			this.pg_info_keys = Object.keys(this.pg_info_data);

        			this.meta_info_data = report.meta_info;
        			this.meta_info_keys = Object.keys(this.meta_info_data);

        			this.alias = report.test_machine.alias;
	        		this.os = report.test_machine.os_name + ' ' + report.test_machine.os_version;
	        		this.compiler = report.test_machine.comp_name + ' ' + report.test_machine.comp_version;
	        		this.owner.username = report.test_machine.owner.username;
	        		this.owner.email = report.test_machine.owner.email;
			        this.reports = report.test_machine.reports;
			        this.branch = report.branch;
			        this.date = report.meta_time.substring(0, 10) + ' ' + report.meta_time.substring(11, 16);
			        this.commit = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + report.commit;

			        if (report.prev != undefined)
			        	this.previous = '/records/' + report.prev;

			        let data = {};

			        for (let number in report.dataset_info.ro) 
			        	for (let result in report.dataset_info.ro[number]) {

			        		console.log(result);

			        		data.latency = report.dataset_info.ro[number][result][0]["results"][0].latency;
			        		data.mode = report.dataset_info.ro[number][result][0]["results"][0].mode;
			        		data.clients = report.dataset_info.ro[number][result][0].clients;
			       			data.median = report.dataset_info.ro[number][result][0].median;
			       			data.run = report.dataset_info.ro[number][result][0]["results"][0].run;
			       			data.tps = report.dataset_info.ro[number][result][0]["results"][0].tps;
			       			data.percentage = report.dataset_info.ro[number][result][0].percentage;

			        		console.log(data);

			        		this.ro.push(data);
			        	}

			        console.log(this.ro[0]);

			        for (let number in report.dataset_info.rw) 
			        	for (let result in report.dataset_info.rw[number])
			        		for (let object in report.dataset_info.rw[number][result]) {
			        			this.rw.push(report.dataset_info.rw[number][result][object]);
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
			this.getResult();
		}
	}


</script>