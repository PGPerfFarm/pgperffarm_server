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
										                	<td class="profile-td">{{ props.item.alias }}</td>
										                    <td class="profile-td">{{ props.item.add_time }}</td>
										                    <td class="profile-td">{{ props.item.type }}</td>
										                    <td class="profile-td">{{ props.item.owner }}</td>
										                    <td class="profile-td">{{ props.item.count }}</td>
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
	import axios from 'axios';

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
		       	axios.get(this.$store.state.endpoints.benchmarks)
		        .then((response) => {

		        	for (let i = 0; i < response.data.count; i++) {

		        		var benchmark = 'Scale ' + response.data.results[i].scale + ', duration ' + response.data.results[i].duration + ', clients ' + response.data.results[i].clients + ', read-only ' + response.data.results[i].read_only;

		        		var machine = {
		        			alias: response.data.results[i].alias,
		        			add_time: response.data.results[i].add_time,
		        			type: response.data.results[i].machine_type,
		        			owner: response.data.results[i].username,
		        			count: response.data.results[i].count,
		        			config_id: response.data.results[i].pgbench_benchmark_id,
		        		};

		        		if (!this.machines.hasOwnProperty(benchmark)) {
		        			this.machines[benchmark] = [];
		        		}

		        		this.machines[benchmark].push(machine);

		        	}

		        	this.panel.push(true);
		        	this.loading = false;

		        
		         })
        		.catch((error) => {
          			console.log(error);
        		})
			}
		},

		mounted() {
    		this.getBenchmarks();
  		}

	}
</script>