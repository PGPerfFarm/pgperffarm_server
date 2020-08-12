<template>
  <v-container fluid grid-list-md>
	  <v-layout row wrap>
	  <v-flex d-flex xs12 sm6 md3>
			<v-layout row v-bind="binding">
			  <v-flex d-flex xs12>
				<v-layout column>
					<v-card flat class="profile-left-top" min-witdh=25>
					  <v-card-title><v-icon color="white">person</v-icon>Your information</v-card-title>
					</v-card>
					<v-card flat class="profile-left-bottom" min-witdh=25>
						<v-card-text>
							<v-icon color="rgb(51, 103, 145)">email</v-icon> {{ email }} <br>
					  <v-icon color="rgb(51, 103, 145)">archive</v-icon> Total reports: {{ reports }} <br>
							<v-icon color="rgb(51, 103, 145)">computer</v-icon> N. machine(s): {{ machines_count }} <br>
						</v-card-text>
					</v-card>
				</v-layout>
			  </v-flex>
			  <v-flex d-flex xs12>
				<v-layout column>
					<v-card flat class="profile-left-top" min-witdh=25>
					  <v-card-title><v-icon color="white">add</v-icon>Add machine</v-card-title>
				  </v-card>
				  <v-card flat class="profile-left-bottom" min-witdh=25>
					
				 </v-card>
				</v-layout>
		  </v-flex>
		</v-layout>
	  </v-flex>
	  <v-flex d-flex fluid>
		<v-layout column>
		  <v-card flat class="profile-card-title">
			<v-card-title class="profile-card-title-text">Welcome back, {{ username }}!</v-card-title>
		  </v-card>
		  <v-card flat class="profile-card">

    <v-card-title class="table-title"> Here is a list of your machines.
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
					<td class="profile-td"> <router-link :to="{path: '/machine/'+ props.item.id }"> {{ props.item.alias }} </router-link></td>
					<td class="profile-td">{{ props.item.type}}</td>
					<td class="profile-td">{{ props.item.approved }}</td>
					<td class="profile-td"> <u> <router-link :to="{path: '/run/'+ props.item.latest }"> {{ props.item.latest }} </router-link> </u></td>
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
               </td>
          </tr>
        </template>
			  </v-data-table>
			</template>
		  </v-card>
		</v-layout>
	  </v-flex>
	</v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'Profile',

  data: () => ({

  	username: '',
  	reports: 0,
  	machines_count: 0,
  	email: '',

  	search: '',
	  loading: true,
	  dialog: false,

	  headers: [
		{ text: 'Alias', align: 'center', value: 'alias' },
		{ text: 'Type', align: 'center', value: 'system' },
		{ text: 'Approved', align: 'center', value: 'state' },
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
	logout() {
		this.$store.commit('removeToken', this.$store.state);
		this.$router.push("/");
	},

	getProfile() {

		this.username = this.$route.params.username;
				var url = this.$store.state.endpoints.user + this.username;

				const httpRequest = new XMLHttpRequest();
				httpRequest.open("GET", url);
				httpRequest.send();

				httpRequest.onreadystatechange = () => {

					if (httpRequest.readyState === XMLHttpRequest.DONE) {

						if (httpRequest.status === 200) {
							var response = JSON.parse(httpRequest.response);

							this.username = response.username;
							this.email = response.email;
							this.machines_count = response.machines.length;

							for (var i = 0; i < response.machines.length; i++) {

								var machine = {
									alias: response.machines[i].alias,
									id: response.machines[i].machine_id,
									type: response.machines[i].machine_type,
									approved: response.machines[i].approved,
									latest: response.machines[i].latest.run_id,
									addDate: response.machines[i].add_time.substring(0, 10),
									secret: response.machines[i].machine_secret,
								};

								this.machines.push(machine);
								this.count += response.machines[i].count;
							}

							this.loading = false;
							console.log(this.machines);


						}
					}
					else {
							console.log(httpRequest.status);
						}
					}
				},


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

	 stopMachine () { /*
	  	axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
		var url = this.$store.state.endpoints.my_machine + machine.sn + '/';
      	axios.put(url, {state: 'I'})
      	.then (() => {
	        window.alert("State changed successfully!")
	        location.reload(); 
      	})
      	.catch((error) => {
      	console.log(error);
    	}) */
    },

    startMachine () {
      //var url = this.$store.state.endpoints.my_machine + machine.sn + '/';
      /*
      axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
      axios.put(url, {state: 'A'})
      .then (() => {
        window.alert("State changed successfully!")
        location.reload(); 
      })
      .catch((error) => {
      console.log(error);
    }) */
	  },

	  close () { /*
		this.dialog = false
		setTimeout(() => {
		}, 300)
		*/
	  },

	  save () {
	  	/*
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
		*/
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
	

},



  mounted() {
	//if (!this.$store.getters.authenticated)
	  //this.$router.push("/");
	  this.getProfile();
  },


  computed: {
	binding () {
	  const binding = {};

	  if (this.$vuetify.breakpoint.mdAndUp) 
		  binding.column = true;

	  return binding;
	  }
	}
}

</script>