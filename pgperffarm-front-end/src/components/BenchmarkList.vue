<template>

	<v-flex d-flex fluid>
          	<v-card flat class="profile-card-title" color="white">
                
	                      		<v-card-title class="results-card-title"> <router-link :to="{path: '/trend/'+ this.$route.params.id + '/' + this.$route.params.config }"> <v-icon color="rgb(51, 103, 145)">keyboard_backspace</v-icon> </router-link> &nbsp; Benchmarks for each run used to calculate average latency and TPS for commit {{this.$route.params.commit}}. </v-card-title>
	                      		<v-card-text>
		                    		<table class="mounts">
		                    			<tr class="mounts-r">
										    		<th class="mounts-h"> <b> Run link </b> </th>
										    		<th class="mounts-h"> <b> Add time </b> </th>
										    		<th class="mounts-h"> <b> Benchmark link </b> </th>
										  </tr>
										  		<tr v-for="(item, i) in results" :key="i" class="mounts-r">
													<td class="mounts-d"> <u> <router-link :to="{path: '/run/' + item.run_id }"> {{item.run_id}} </router-link> </u> </td>
													<td class="mounts-d"> {{item.add_time}} </td>
													<td class="mounts-d"> <u> <router-link :to="{path: '/result/' + item.pgbench_result_id }"> {{item.pgbench_result_id}} </router-link> </u> </td>
												    
										  		</tr>

		                    	</table>
		                    	</v-card-text>
	                    	
          	</v-card>
      	</v-flex>

</template>

<script>

  import axios from 'axios';

  export default {
  name: 'BenchmarkList',
  data: () => ({

	  results: [],

  	}),


  methods: {

	getBenchmarks() {

		var url = this.$store.state.endpoints.trends_benchmarks + this.$route.params.commit + '/' + this.$route.params.machine + '/' + this.$route.params.benchmark;

      axios.get(url).then((response) => {

          for(var i = 0; i < response.data.count; i++) {

            var result = {
              run_id: response.data.results[i].run_id,
              pgbench_result_id: response.data.results[i].pgbench_result_id,
              add_time: response.data.results[i].add_time,
              
            };

            this.results.push(result);
          }

          this.loading = false;

		}).catch((error) => {
		  console.log(error);
		})
	}
  },

  mounted() {
	this.getBenchmarks();
  },

}

</script>