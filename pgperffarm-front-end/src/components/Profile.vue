<template>
  <v-container fluid grid-list-md>
	  <v-layout row wrap>
	  <v-flex d-flex xs12 sm6 md3>
			<v-layout column>
			  <v-flex d-flex md5>
				<v-layout column>
					<v-card flat class="profile-left-top" min-witdh=15>
					  <v-card-title><v-icon color="white">person</v-icon>Your information</v-card-title>
					</v-card>
					<v-card flat class="profile-left-bottom" min-witdh=15>
						<v-card-text class="profile-left-text">
							<v-icon color="rgb(51, 103, 145)">email</v-icon> {{ email }} <br>
					  <v-icon color="rgb(51, 103, 145)">archive</v-icon> Total reports: {{ reports }} <br>
							<v-icon color="rgb(51, 103, 145)">computer</v-icon> N. machine(s): {{ machines_count }} <br>
						</v-card-text>
					</v-card>
				</v-layout>
			  </v-flex>
			  <v-flex d-flex md5>
				<v-layout column>
					<v-card flat class="profile-left-top" min-witdh=15>
					  <v-card-title><v-icon color="white">add</v-icon>Add machine</v-card-title>
				  </v-card>
				  <v-card flat class="profile-left-bottom" min-witdh=15>
						<v-card-text class="profile-left-text">
							<v-form ref="form" lazy-validation class="machine-form">
								<v-text-field label="Alias" single-line dense prepend-inner-icon="public" v-model="new_machine.alias" :counter="20" maxlength="20" required></v-text-field>
								<v-text-field label="Description" single-line dense prepend-inner-icon="subject" v-model="new_machine.description" :counter="20" maxlength="20" required></v-text-field>
						</v-form>
						</v-card-text>
						<v-card-actions>
	                		<v-btn block class="profile-button" v-on:click="addMachine()"> ADD </v-btn>
	                	</v-card-actions>
					</v-card>
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
                           <v-text-field v-model="editedMachine.description" label="Description"></v-text-field>
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

			<template>
				<v-data-table v-bind:headers="headers" :items="machines" hide-default-footer :search="search" :loading="loading" item-key="alias" class="elevation-1">
					<template #item.alias="{ item }"> <router-link :to="{path: '/machine/'+ item.id }"> {{ item.alias }} </router-link> </template>
					<template #item.latest="{ item }"> <router-link :to="{path: '/runs/'+ item.latest }"> {{ item.latest }} </router-link> </template>
					<template v-slot:item.actions="{ item }"> 
						<v-icon small class="mr-2" @click="viewSecret(item)"> visibility </v-icon>
						<v-icon small @click="editMachine(item)"> create </v-icon>
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
		{ text: 'Description', align: 'center', value: 'description' },
		{ text: 'Type', align: 'center', value: 'system' },
		{ text: 'Approved', align: 'center', value: 'approved' },
		{ text: 'Runs', align: 'center', value: 'count' },
		{ text: 'Latest', align: 'center', value: 'latest' },
		{ text: 'Add date', align: 'center', value: 'addDate' },
		{ text: 'Actions', align: 'center', value: 'actions', sortable: false },
	  ],

	  machines: [],
	  editedMachine: {
		description: '',
	  },

	  new_machine: {
	  	'alias': '',
	  	'description': '',
	  }
	  
  	}),

  watch: {
	  dialog (val) {
		val || this.close()
	  },
	},


  methods: {

  	getCookie(name) {
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) return parts.pop().split(';').shift();
	},

	getProfile() {

		var url = this.$store.state.endpoints.user;
		const httpRequest = new XMLHttpRequest();
		httpRequest.open("GET", url);
		httpRequest.withCredentials = true;
		httpRequest.setRequestHeader("Content-Type", "application/json");
		httpRequest.send();

		httpRequest.onreadystatechange = () => {

			if (httpRequest.readyState === XMLHttpRequest.DONE) {

				if (httpRequest.status === 200) {
					var response = JSON.parse(httpRequest.response);

					this.username = response.results[0].username;
					this.$store.commit('setUsername', response.results[0].username);
					this.email = response.results[0].email;
					this.machines_count = response.results[0].machines.length;

					for (var i = 0; i < this.machines_count; i++) {

						var machine = {
							alias: response.results[0].machines[i].alias,
							description: response.results[0].machines[i].description,
							count: response.results[0].machines[i].count,
							id: response.results[0].machines[i].machine_id,
							type: response.results[0].machines[i].machine_type,
							approved: response.results[0].machines[i].approved,
							latest: response.results[0].machines[i].latest.run_id,
							addDate: response.results[0].machines[i].add_time.substring(0, 10),
							secret: response.results[0].machines[i].machine_secret,
						};

						this.machines.push(machine);
						this.reports += response.results[0].machines[i].count;
					}

					this.loading = false;
				}
			}
			else {
					console.log(httpRequest.status);
			}
		}
	},

	editMachine (machine) {
		this.editedIndex = machine.id;
	    this.editedMachine.description = machine.description;
		this.dialog = true
	  },

	  viewSecret (machine) {
		window.alert('Machine secret: ' + machine.secret);
	  },

	  close () { 
		this.dialog = false
		setTimeout(() => {
		}, 300)
	  },

	  save () {

	  	var url = this.$store.state.endpoints.edit + this.editedIndex + '/';
	  	var token = this.getCookie('csrftoken');
		const httpRequest = new XMLHttpRequest();
		httpRequest.open("PUT", url);
		httpRequest.withCredentials = true;
		httpRequest.setRequestHeader("X-CSRFTOKEN", token);
		httpRequest.setRequestHeader("Content-Type", "application/json");
		httpRequest.send(JSON.stringify({description: this.editedMachine.description}));

		httpRequest.onreadystatechange = () => {

			if (httpRequest.readyState === XMLHttpRequest.DONE) {

				if (httpRequest.status === 200) {

					window.alert("Information changed successfully!")
        			location.reload(); 
					
				}
			}
			else {
					console.log(httpRequest.status);
					this.close()
			}
		}
	  },

	  addMachine () {

	  	var url = this.$store.state.endpoints.add;
	  	var token = this.getCookie('csrftoken');
		const httpRequest = new XMLHttpRequest();
		httpRequest.open("POST", url);
		httpRequest.withCredentials = true;
		httpRequest.setRequestHeader("X-CSRFTOKEN", token);
		httpRequest.setRequestHeader("Content-Type", "application/json");
		httpRequest.send(JSON.stringify(this.new_machine));

		httpRequest.onreadystatechange = () => {

			if (httpRequest.readyState === XMLHttpRequest.DONE) {

				if (httpRequest.status === 201) {

					window.alert("Machine added successfully!")
        			location.reload(); 
					
				}
			}
			else {
					console.log(httpRequest.status);
					this.close()
			}
		}
	  },

},

  mounted() {
	if (this.getCookie('csrftoken') == null) {
	  this.$router.push("/");
	}
	else {
	  this.getProfile();
	}
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