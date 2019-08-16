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
            						Shown here is the latest status of each farm member for each branch it has reported on. Use the farm member link for history of that member on the relevant branch.
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
					    			 v-for="(item, i) in branches"
      								 :key="i">
						      			<template v-slot:header>
						      				<div class="panel-div"> {{ item }} </div>
						      			</template>
						      			<v-card>
						        			<template>
							              		<v-data-table
							              		 v-bind:headers="headers"
								                :items="machines[item]"
								                hide-actions
								                :loading="loading"
								                item-key="alias"
								                class="elevation-1"
								              	>
							             	
							                		<template v-slot:items="props">
							                  			<tr>
										                	<td class="profile-td"> <router-link :to="{path: '/machine/'+ props.item.alias }"> {{ props.item.alias }} </router-link></td>
										                    <td class="profile-td">{{ props.item.system }}</td>
										                    <td class="profile-td">{{ props.item.trending.improvement }}</td>
										                    <td class="profile-td">{{ props.item.trending.status_quo }}</td>
										                    <td class="profile-td">{{ props.item.trending.regression }}</td>
										                    <td class="profile-td"><router-link :to="{path: props.item.detail}">
										                    	<v-icon color="rgb(51, 103, 145)">link</v-icon>
                    											Link</router-link></td>
										                    <td class="profile-td">
										                    	<a :href=props.item.commit target="_blank"> <u>{{ props.item.commit.substring(63, 70) }} </u></a>
										                    </td>
										                    <td class="profile-td">{{ props.item.date }}</td>
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
		name: 'Status',

		data: () => ({
			panel: [true, false, false, false],
			branches: ['Head', '10 stable', '9.6 stable', '9.5 stable'],

			search: '',
      		loading: true,

      		headers: [
		        { text: 'Alias', align: 'center', value: 'alias' },
		        { text: 'System', align: 'center', value: 'system' },
		        { text: 'Improv.', align: 'center', value: 'improvement'},
		        { text: 'Status quo', align: 'center', value: 'status_quo'},
		        { text: 'Regr.', align: 'center', value: 'regression'},
		        { text: 'Detail', align: 'center', value: 'detail'},
		        { text: 'Commit', align: 'center', value: 'commit'},
		        { text: 'Date', align: 'center', value: 'date' }
      		],

      		machines: {
			'Head': [],
			'10 stable': [],
			'9.6 stable': [],
			'9.5 stable': []
			}

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

		        	var commit_url = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=';

		        	for(var i = 0; i < response.data.count; i++) {

		        		var machine = {
		        			alias: response.data.results[i].machine_info.alias,
              				system: response.data.results[i].machine_info.os_name + ' ' + response.data.results[i].machine_info.os_version,
		        			trending: {
		        				improvement: response.data.results[i].trend.improved,
		        				status_quo: response.data.results[i].trend.quo,
		        				regression: response.data.results[i].trend.regressive
		        			},	
		        			detail: '/records/' + response.data.results[i].uuid,
		        			commit: commit_url + response.data.results[i].commit,
		        			date: response.data.results[i].add_time.substring(0, 10) + ' ' + response.data.results[i].add_time.substring(11, 16)

		        		};

		        		if (response.data.results[i].branch == 'HEAD') {
		        			this.machines['Head'].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_10_STABLE') {
		        			this.machines['10 stable'].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_9_6_STABLE') {
		        			this.machines['9.6 stable'].push(machine);
		        		}

		        		else if (response.data.results[i].branch == 'REL_9_5_STABLE') {
		        			this.machines['9.5 stable'].push(machine);
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