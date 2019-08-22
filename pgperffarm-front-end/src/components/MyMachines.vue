<template>

<v-card flat class="profile-card">

    <v-card-title class="table-title">My machines
			  <v-spacer></v-spacer>
			     <v-text-field
      				v-model="search"
      				append-icon="search"
      				label="Search"
      				single-line
      				hide-details
			     ></v-text-field>
			</v-card-title>

      <v-dialog v-model="dialog" max-width="500px">

            <v-card>
              <v-card-title>
                 <span class="headline">Edit machine</span>
              </v-card-title>

              <v-card-text>
                   <v-container grid-list-md>
                    <v-layout wrap>
                        <v-flex xs12 sm6 md4>
                           <v-text-field v-model="editedMachine.os_name" label="OS name"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                           <v-text-field v-model="editedMachine.os_version" label="OS version"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                           <v-text-field v-model="editedMachine.comp_name" label="Compiler name"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                           <v-text-field v-model="editedMachine.comp_version" label="Compiler version"></v-text-field>
                        </v-flex>
                    </v-layout>
                 </v-container>
              </v-card-text>

              <v-card-actions>
                 <v-spacer></v-spacer>
                 <v-btn class="login-button" text @click="close">Cancel</v-btn>
                 <v-btn class="login-button" text @click="save">Save</v-btn>
              </v-card-actions>
           </v-card>
        </v-dialog>

			<!-- check server side pagination-->
			<template>
			  <v-data-table
				v-bind:headers="headers"
				:items="machines"
				:search="search"
				item-key="alias"
				class="elevation-1"
				hide-actions
				:loading="loading"
				loading-text="Loading..."
			  >

				<template v-slot:items="props">
				  <tr>
					<td class="profile-td"> <router-link :to="{path: '/machine/'+ props.item.alias }"> {{ props.item.alias }} </router-link></td>
					<td class="profile-td">{{ props.item.system.os_name + ' ' + props.item.system.os_version + ' ' + props.item.system.comp_name + ' ' + props.item.system.comp_version}}</td>
					<td class="profile-td">{{ props.item.state }}</td>
					<td class="profile-td"> 
						<router-link :to="{path: props.item.uuid}">
							{{ props.item.latest }}
						</router-link> 
					</td>
					<td class="profile-td">{{ props.item.addDate }}</td>
				  <td class="profile-td">
				  	<v-tooltip top>
				  		<template v-slot:activator="{ on }">
							 <v-icon
			                  small
			                  class="mr-2"
			                  @click="viewSecret(props.item)"
			                  v-on="on"
			                  >
			                  lock_open
           					</v-icon>
           				</template>
           				<span>View machine secret</span>
           			</v-tooltip>
           			<v-tooltip top>
				  		<template v-slot:activator="{ on }">
			                <v-icon
			                  small
			                  class="mr-2"
			                  @click="editMachine(props.item)"
			                  v-on="on"
			                  >
			                  edit
			              </v-icon>
			          </template>
			          <span>Edit machine</span>
			      </v-tooltip>
			      <v-tooltip top>
				  		<template v-slot:activator="{ on }">
				            <v-icon
				                v-if="props.item.state == 'A'"
				                small
				                @click="stopMachine(props.item)"
				                v-on="on"
				                >
				                stop
				          	</v-icon>
				        </template>
				        <span>Deactivate machine</span>
				   </v-tooltip>
				  <v-tooltip top>
				  		<template v-slot:activator="{ on }">
				          <v-icon
				                v-if="props.item.state == 'I'"
				                small
				                @click="startMachine(props.item)"
				                v-on="on"
				                >
				                play_arrow
				          </v-icon>
				      </template>
				      <span>Activate machine</span>
				</v-tooltip>
            </td>
          </tr>
        </template>
			  </v-data-table>
			</template>
		  </v-card>
		</template>

<script>

  import axios from 'axios';

  export default {
  name: 'MyMachines',
  data: () => ({
	  search: '',
	  loading: true,
	  dialog: false,

	  headers: [
		{ text: 'Alias', align: 'center', value: 'alias' },
		{ text: 'System', align: 'center', value: 'system' },
		{ text: 'State', align: 'center', value: 'state' },
		{ text: 'Latest', align: 'center', value: 'latest' },
		{ text: 'Add date', align: 'center', value: 'addDate' },
		{ text: 'Actions', align: 'center', value: 'action', sortable: false },
	  ],

	  machines: [],
	  editedMachine: {
		os_name: '',
		os_version: '',
		comp_name: '',
		comp_version: '',
    	sn: ''
	  	},
	  	editedIndex: -1,
  	}),

  watch: {
	  dialog (val) {
		val || this.close()
	  },
	},

  methods: {

	editMachine (machine) {
		this.editedIndex = this.machines.indexOf(machine)
		this.editedMachine.os_name = machine.system.os_name;
	    this.editedMachine.os_version = machine.system.os_version;
	    this.editedMachine.comp_name = machine.system.comp_name;
	    this.editedMachine.comp_version = machine.system.comp_version;
	    this.editedMachine.sn = machine.sn;
		this.dialog = true
	  },

	  viewSecret (machine) {
		window.alert('Machine secret: ' + machine.secret);
	  },

	 stopMachine (machine) {
	  	axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
		var url = this.$store.state.endpoints.my_machine + machine.sn + '/';
      	axios.put(url, {state: 'I'})
      	.then (() => {
	        window.alert("State changed successfully!")
	        location.reload(); 
      	})
      	.catch((error) => {
      	console.log(error);
    	})
    },

    startMachine (machine) {
      var url = this.$store.state.endpoints.my_machine + machine.sn + '/';
      axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
      axios.put(url, {state: 'A'})
      .then (() => {
        window.alert("State changed successfully!")
        location.reload(); 
      })
      .catch((error) => {
      console.log(error);
    })
	  },

	  close () {
		this.dialog = false
		setTimeout(() => {
		}, 300)
	  },

	  save () {
	  	axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
		var url = this.$store.state.endpoints.my_machine + this.editedMachine.sn + '/';
      	axios.put(url, {os_name: this.editedMachine.os_name, os_version: this.editedMachine.os_version, comp_name: this.editedMachine.comp_name, comp_version: this.editedMachine.comp_version})
      .then (() => {
        window.alert("Information changed successfully!")
        location.reload(); 
      })
      .catch((error) => {
      console.log(error);
    })
		this.close()
	  },

	toggleAll () {
		if (this.selected.length) this.selected = []
		else this.selected = this.machines.slice()
	  },

	changeSort (column) {
		if (this.pagination.sortBy === column) {
		  this.pagination.descending = !this.pagination.descending
		} 
		else {
		  this.pagination.sortBy = column
		  this.pagination.descending = false
		}
	},

	getMachines() {
	  // reports, machines, branches

	  axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
	  var url = this.$store.state.endpoints.my_machine //+ '?page=1&machine_owner__username=' + this.$store.getters.username;

	  axios.get(url)
		.then((response) => {

		  var branches = [];

		  var info = {
			  reports: 0,
			  machines: response.data.count,
			  branches: 0,
			  email: ''
		  }

		  for(var i = 0; i < response.data.count; i++) {

			var lastest = '';
			var uuid = '';

			if (response.data.results[i].lastest.length > 0) {
			  lastest = response.data.results[i].lastest[0].branch;
			  uuid = '/records/' + response.data.results[i].lastest[0].uuid;
			  branches.push(response.data.results[i].lastest[0].branch);
			}

			var machine = {
			  alias: response.data.results[i].alias,
		      sn: response.data.results[i].sn,
		      secret: response.data.results[i].machine_secret,
			  system: {
		          os_name: response.data.results[i].os_name,
		          os_version: response.data.results[i].os_version,
		          comp_name: response.data.results[i].comp_name,
		          comp_version: response.data.results[i].comp_version
		      },
			  state: response.data.results[i].state,
			  latest: lastest,
			  uuid: uuid,
			  addDate: response.data.results[i].add_time.substring(0, 10)
			};

			info.reports += response.data.results[i].reports;

			this.machines.push(machine);
		  }

		  info.branches = new Set(branches).size;

		  this.$store.commit('setProfile', info);

		  this.loading = false;

		})
		.catch((error) => {
		  console.log(error);
		})
	}
  },

  mounted() {
	this.getMachines();
  },

}

</script>