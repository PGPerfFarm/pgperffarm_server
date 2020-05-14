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
	                <v-card flat class="profile-left-top" min-width=15>
	                  <v-card-title>
	                  	Owner: {{owner.username}} <br>
                    	Reports: {{reports}} <br>
                  	  </v-card-title> 
	                </v-card>
	                <v-card flat class="profile-left-bottom" min-width=15>
	                	<v-card-text>
	                      <v-icon color="rgb(51, 103, 145)">computer</v-icon> OS: {{os}} <br>
	                      <v-icon color="rgb(51, 103, 145)">border_all</v-icon> Processor: {{compiler}} <br>
	                      <v-icon color="rgb(51, 103, 145)">email</v-icon> Email: {{ owner.email }} <br> <br>
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
                    <v-tab> <span style="color: white"> Progress </span> </v-tab>
                    <v-tab> <span style="color: white"> Meta information </span> </v-tab>
                    <v-tab> <span style="color: white"> Settings </span> </v-tab>
                    <v-tab> <span style="color: white"> Hardware </span> </v-tab>
					<v-tab> <span style="color: white"> Operating system </span> </v-tab>

                	<v-tabs-items>

	                 	<!-- progress -->
	                  	<v-tab-item>
	                    	<v-card flat>
	                      		<v-card-title class="results-card-title"> Progress for each test, showing read-only and read-write. </v-card-title>
	                      		<v-container class="results-container">
		                      		<v-layout row v-bind="binding">
		                      			<v-container>
				                      		<v-layout column>
				                      			<v-card-title class="results-title"> Read only </v-card-title>
				                      			<v-flex v-for="(object, index) in this.ro" v-bind:key="index">
				                      				<v-card flat>
				                      					<results-table v-bind:data="ro[index]"></results-table>
				                      				</v-card>
				                      			</v-flex>
				                      		</v-layout>
			                      		</v-container>
			                      		<v-container>
				                      		<v-layout column>
				                      			<v-card-title class="results-title"> Read/write </v-card-title>
				                      			<v-flex v-for="(object, index) in this.rw" v-bind:key="index">
				                      				<v-card flat>
				                      					<results-table v-bind:data="rw[index]"></results-table>
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
		                    	<v-card-title class="results-card-title">
		                    		Displayed below is detail about the testing meta information.
		                    	</v-card-title>
		                    	<v-card-text v-for="(item, index) in meta_info_keys" v-bind:key="item" class="results-text">
		                    		<b>{{ meta_info_keys[index] }}</b>: {{ meta_info_data[item] }}
		                    	</v-card-text>

		                    </v-card>
		                </v-tab-item>

		                <!-- settings -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title class="results-card-title">
		                    		Displayed below is information about the testing operating settings.
		                    	</v-card-title>
		                    	<v-card-text v-for="(item, index) in pg_info_keys" v-bind:key="item" class="results-text">
		                    		<b>{{ pg_info_keys[index] }}</b>: {{ pg_info_data[item] }}
		                    	</v-card-text>

		                    </v-card>
		                </v-tab-item>

		                <!-- hardware -->
		                <v-tab-item>
		                    <v-card flat>
		                    	<v-card-title class="results-card-title">
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
		                    	<v-card-title class="results-card-title">
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

			report: '',

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

		}),

		methods: {

			getResult() {

				var id = this.$route.params.id;
				var url = this.$store.state.endpoints.record + id;

				axios.get(url)
        		.then((response) => {

        			var report = response.data;
        			this.report = report;

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

	        		//this.owner.username = report.test_machine.owner_username;
	        		var email = report.test_machine.owner_email;
                  	email = email.replace('@', '<at>');
                  	this.owner.email = email;
                  	
			        this.reports = report.test_machine.reports;
			        this.branch = report.branch;
			        this.date = report.meta_time.substring(0, 10) + ' ' + report.meta_time.substring(11, 16);
			        this.commit = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=' + report.commit;

			        if (report.prev != undefined)
			        	this.previous = '/records/' + report.prev;
			      
			        for (let number in report.dataset_info.ro)
			        	for (let result in report.dataset_info.ro[number]) {

			        		let data = {};

			        		data.latency = report.dataset_info.ro[number][result][0]["results"][0].latency;
			        		data.mode = report.dataset_info.ro[number][result][0]["results"][0].mode;
			        		data.clients = report.dataset_info.ro[number][result][0].clients;
			       			data.median = report.dataset_info.ro[number][result][0].median;
			       			data.run = report.dataset_info.ro[number][result][0]["results"][0].run;
			       			data.tps = report.dataset_info.ro[number][result][0]["results"][0].tps;
			       			data.percentage = report.dataset_info.ro[number][result][0].percentage;

			        		this.ro.push(data);
			        	}

			        for (let number in report.dataset_info.rw) 
			        	for (let result in report.dataset_info.rw[number]) {

			        		let data = {};

			        		data.latency = report.dataset_info.rw[number][result][0]["results"][0].latency;
			        		data.mode = report.dataset_info.rw[number][result][0]["results"][0].mode;
			        		data.clients = report.dataset_info.rw[number][result][0].clients;
			       			data.median = report.dataset_info.rw[number][result][0].median;
			       			data.run = report.dataset_info.rw[number][result][0]["results"][0].run;
			       			data.tps = report.dataset_info.rw[number][result][0]["results"][0].tps;
			       			data.percentage = report.dataset_info.rw[number][result][0].percentage;

			        		this.rw.push(data);

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