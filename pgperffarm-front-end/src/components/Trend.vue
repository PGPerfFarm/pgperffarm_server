<template>
	<v-container fluid grid-list-md>
    	<v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat class="result-toolbar">
      				<v-toolbar-title class="result-toolbar"> 
      					Average TPS and latency in milliseconds: {{ alias }}
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
      				<v-btn class="login-button" :href="'/machine/'+ id"> View history </v-btn>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            		<v-btn class="login-button" v-on:click="downloadCSV()">Download CSV</v-btn>
            	</v-toolbar>
     		</v-card>
    	<v-layout>
      		<v-flex d-flex xs12 sm6 md3>
            	<v-layout column>
	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-title>
		                  	Owner: {{ owner }} <br> <br>
                  	  	</v-card-title> 
	                </v-card>
	                <v-card flat class="run-left-bottom" min-width=15>
	                	<v-card-text>
	                		<p>
								<v-icon color="rgb(51, 103, 145)">computer</v-icon> {{ os }} <br>
	                    	</p>
	                    		<v-icon color="rgb(51, 103, 145)">border_all</v-icon> {{ compiler }}
	                	</v-card-text>
	                </v-card>

	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-title>
		                  	Command line <br> <br>
                  	  	</v-card-title> 
	                </v-card>
	                <v-card flat class="run-left-bottom" min-width=15>
	                	<v-card-text class="run-left-bottom-monospace" id="command-line">
	                		<p>
	                		pgbench -i -s {{ scale }} -p 5432 && pgbench -r -c {{ clients }} -j {{ clients }} -T {{ duration }} -l --aggregate-interval 1 {{ read_only_command }}
	                		</p>
	                	</v-card-text>
	                	<v-card-actions>
	                		<v-btn block class="profile-button" v-on:click="copy()"> COPY </v-btn>
	                	</v-card-actions>
	                </v-card>

	                <v-card flat class="run-left-top" min-width=15>
	                	<v-card-text>
	                		Benchmark configuration: <br>
		                  	<v-icon color="white">account_tree</v-icon> Clients: {{ clients }} <br>
		                  	<v-icon color="white">linear_scale</v-icon> Scale: {{ scale }} <br>
		                  	<v-icon color="white">timelapse</v-icon> Duration: {{ duration }} <br>
		                  	<v-icon color="white">edit</v-icon> {{ read_only }} <br> <br>
                  	  	</v-card-text> 
	                </v-card>

            	</v-layout>
      		</v-flex>
      		<v-flex d-flex fluid>
          		<router-view ref="plots"></router-view>
      	</v-flex>
    </v-layout>
  </v-layout>
  </v-container>
	

</template>

<script>

	export default {
		name: 'Trend',

		data: () => ({
			
			alias: '',
			owner: '',
			compiler: '',
			os: '',
			id: '',

			clients: '',
			duration: '',
			scale: '',
			read_only: '',
			read_only_command: '',

			json_data: '',
			
		}),

		methods: {

			getTrend() {

				var url = this.$store.state.endpoints.trends + this.$route.params.id + '/' + this.$route.params.config;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							console.log(response);

							this.json_data = response;

			        		var main = response.results[0];

			        		this.alias = main.alias;
			        		this.owner = main.username;
			        		this.id = main.machine_id;

			        		this.clients = main.clients;
			        		this.duration = main.duration;
			        		this.scale = main.scale;

							if (main.read_only == true) {
								this.read_only = "Read-only test";
								this.read_only_command = '-S';
							}

							else {
								this.read_only = "Read-write test";
							}

			        		this.os = main.kernel_name + ' ' + main.dist_name + ' ' + main.machine_type;
			        		this.compiler = main.compiler;
			        	}
			        }
			    }
			},

			downloadJSON() {
				const url = window.URL.createObjectURL(new Blob([JSON.stringify(this.json_data, null, 2)], {type: 'application/json'}));
			    const link = document.createElement('a');
			    link.href = url;
			    link.setAttribute('download', 'trend.json');
			    document.body.appendChild(link);
			    link.click();
    		},

    		downloadCSV() {
    			this.$refs.plots.downloadCSV();
    		},

    		copy() {
				var text = document.getElementById("command-line");
				var str = text.firstChild.data;
				const el = document.createElement('textarea');
				el.value = str;
				document.body.appendChild(el);
				el.select();
				document.execCommand('copy');
				document.body.removeChild(el);
    		},

		},

		mounted() {
			this.getTrend();
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