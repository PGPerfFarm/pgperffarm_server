<template>
	<v-container fluid grid-list-md>
    <v-layout column>
      		<v-card flat class="machine-main-card">
      			<v-toolbar flat>
      				<v-toolbar-title>
      					Report page
      				</v-toolbar-title>
      				<v-spacer></v-spacer>
            		<v-btn class="login-button" v-on:click="downloadJSON()">Download JSON</v-btn>
            	</v-toolbar>
        	<v-layout row>
        	<v-flex>
        	<v-card flat>
		        <v-card-text class="machine-main-text">
		          Farmer:  <br>
		          Report number: 
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          Branch:  <br>
		          Commit 
		        </v-card-text>
		    </v-card>
		</v-flex>
		<v-flex>
		    <v-card flat>
		        <v-card-text class="machine-main-text">
		          Date:  <br>
		          Previous: 
		        </v-card-text>
		    </v-card>
		</v-flex>
         </v-layout>
     </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>Owner: <br>
                    Reports: <br>
                    Branch: 
                  </v-card-title> 
	                </v-card>
	                <v-card class="profile-left-bottom">
	                	<v-card-text>
                      OS:  <br>
                      Processor:  <br>
                      Email: <br>
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
                      <v-tab>
                        Progress
                      </v-tab>
                      <v-tab>
                      	Meta information
                      </v-tab>
                      <v-tab>
                      	Settings
                      </v-tab>
                      <v-tab>
                      	Hardware
                      </v-tab>
                      <v-tab>
                      	Operating system
                      </v-tab>


                <v-tabs-items>
                 <!-- progress -->
                  <v-tab-item :key=1>
                    <v-card flat>
                      <v-card-title> aaas </v-card-title>
                    </v-card>
                  </v-tab-item>

                <!-- meta information -->
                  <v-tab-item>
                    <v-card flat>
                      <v-card-title> test1 </v-card-title>
                    </v-card>
                  </v-tab-item>

                  <!-- settings -->
                  <v-tab-item>
                    <v-card flat>
                      <v-card-title> aaas </v-card-title>
                    </v-card>
                  </v-tab-item>

                  <!-- hardware -->
                  <v-tab-item>
                    <v-card flat>
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
                      <v-card-title> aaas </v-card-title>
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

	export default {
		name: 'Results',

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

		}),

		methods: {

			getResult() {

				var id = this.$route.params.id;

				axios.get(this.$store.state.endpoints.records)
        		.then((response) => {

        			var report = '';

        			for (var i = 0; i < response.data.count; i++) 
        				if (response.data.results[i].uuid == id)
        					report = response.data.results[i];

        			this.hardware[0].children[0].name = report.linux_info.cpuinfo.replace(/: /g, '');
        			this.hardware[1].children[0].name = report.linux_info.meminfo.replace(/: /g, '');

        			console.log(report.linux_info.cpuinfo);

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