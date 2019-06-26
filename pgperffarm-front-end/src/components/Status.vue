<template>
	<v-app>
		<main>
			<v-content>
				<v-layout justify-center column my-4>
					<v-flex>
    					<v-card flat class="pg-v-card">
        					<v-card-text class="pg-v-card-text-main">
            					Status page
        					</v-card-text>
      					</v-card>
  					</v-flex>
  					<v-flex>
  						<v-layout row class="status-layout">
     						<v-card flat>
            					<v-card-title class="table-title">
            						Shown here is the latest status of each farm member for each branch it has reported on in the last 30 days. Use the farm member link for history of that member on the relevant branch.
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
								      v-for="(item, i) in branches"
								      :key="i"
								    >
						      			<template v-slot:header>
						        			<div>{{item}}</div>
						        			<template>
							              		<v-data-table
								                 :headers="headers"
								                 :items="machines"
								                 :pagination.sync="pagination"
								                 :search="search"
								                 :loading="loading"
								                 select-all
								                 item-key="alias"
								                 class="elevation-1"
								              	>
									            <!--
									            <template v-slot:no-data>
									                <v-alert :value="true" color="error" icon="warning">
									                	Sorry, nothing to display here :(
									                </v-alert>
									            </template>
									            -->
							             			<template v-slot:no-results>
							                			<v-alert :value="true" color="error" icon="warning">
							                  				Your search for "{{ search }}" found no results.
							                			</v-alert>
							              			</template>
							              			<template v-slot:headers="props">
							                  			<tr>
							                    			<th class="profile-th"
							                     				v-for="header in props.headers"
							                      				:key="header.text"
							                      				:class="['column sortable', pagination.descending ? 'desc' : 'asc', header.value === pagination.sortBy ? 'active' : '']"
							                      				@click="changeSort(header.value)"
							                    			>
							                      				<v-icon small>arrow_upward</v-icon>
							                      				{{ header.text }}
							                    			</th>
							                  			</tr>
							                		</template>
							                		<!--
							                		<template v-slot:items="props">
							                  			<tr>
										                	<td class="profile-td">{{ props.item.alias }}</td>
										                    <td class="profile-td">{{ props.item.system }}</td>
										                    <td class="profile-td">{{ props.item.trending.improvement }}</td>
										                    <td class="profile-td">{{ props.item.trending.status_quo }}</td>
										                    <td class="profile-td">{{ props.item.trending.regression }}</td>
										                    <td class="profile-td">{{ props.item.detail }}</td>
										                    <td class="profile-td">{{ props.item.commit }}</td>
										                    <td class="profile-td">{{ props.item.link }}</td>
							                  			</tr>
							                		</template>
							                	-->
							              		</v-data-table>
	            							</template>
						      			</template>
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
		name: 'Status',

		data: () => ({
			panel: [true, false, false, false],
			branches: ['Head', '10 stable', '9.6 stable', '9.5 stable'],

			search: '',
      		loading: true,
      		pagination: {
        		sortBy: 'name'
      		},

      		headers: [
		        { text: 'Alias', align: 'left', value: 'alias' },
		        { text: 'System', value: 'system' },
		        { text: 'Improvement', value: 'improvement'},
		        { text: 'Status quo', value: 'status_quo'},
		        { text: 'Regression', value: 'regression'},
		        { text: 'Detail', value: 'detail'},
		        { text: 'Commit', value: 'commit'},
		        { text: 'Date', value: 'date' }
      		],

      		machines: [
      			[],
				[],
				[],
				[]
      		]	

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
        		this.panel = [true, true, true, true]
      		},

      		none () {
        		this.panel = [false, false, false, false]
      		},

      		getStatus() {
		       	axios.get(this.$store.state.endpoints.status)
		        .then((response) => {

		        	for(var i = 0; i < response.data.count; i++) {

		        		var machine = {
		        			alias: response.data.results[i].alias,
              				system: response.data.results[i].os_name + ' ' + response.data.results[i].os_version + ' ' + response.data.results[i].comp_version,
		        			trending: {
		        				improvement: response.data.results[i].trend.improved,
		        				status_quo: response.data.results[i].trend.quo,
		        				regression: response.data.results[i].trend.regressive
		        			},	
		        			detail: 'link',
		        			commit: 'commit',
		        			date: response.data.results[i].add_time.substring(0, 10) + response.data.results[i].add_time.substring(11, 16)

		        		};

		        		if (response.data.results[i].branch == 'HEAD') {
		        			this.machines[0].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_10_STABLE') {
		        			this.machines[1].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_9_6_STABLE') {
		        			this.machines[2].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_9_5_STABLE') {
		        			this.machines[3].push(machine);
		        		}

		        		this.loading = false;

		        	}
		         })
        		.catch((error) => {
          			console.log(error);
        		})
			}
		},

		mounted() {
    		this.getStatus();
  		}

	}
</script>