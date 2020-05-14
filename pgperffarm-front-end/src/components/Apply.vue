<template>
	<v-card flat class="profile-card">
		<v-card-title class="table-title">
			Add machine
		</v-card-title>
		<v-card-text>
            <v-form ref="form" lazy-validation class="machine-form">
                <v-text-field 
                    prepend-icon="computer" 
                    name="os_name" 
                    label="Operating system" 
                    type="text"
                    v-model="machine.os_name"
                    :counter="20"
                    maxlength="20"
                    required
                    >
                    </v-text-field>
                    <v-text-field 
                    prepend-icon="list_alt" 
                    name="os_version" 
                    label="Operating system version" 
                    type="text"
                    v-model="machine.os_version"
                    :counter="20"
                    maxlength="20"
                    required
                    > 
                    </v-text-field>
                    <v-text-field 
                    prepend-icon="border_all" 
                    name="comp_name" 
                    label="Compiler" 
                    type="text"
                    v-model="machine.comp_name"
                    :counter="20"
                    maxlength="20"
                    required
                    > 
                    </v-text-field>
                    <v-text-field 
                    prepend-icon="table_chart" 
                    name="comp_version" 
                    label="Compiler version" 
                    type="text"
                    v-model="machine.comp_version"
                    :counter="20"
                    maxlength="20"
                    required
                    > 
                    </v-text-field>
            </v-form>
        </v-card-text>
    	<v-card-actions>
            <v-btn block class="login-button" v-on:click="addMachine()">Add machine</v-btn>
        </v-card-actions>
	</v-card>
</template>

<script>
	import axios from 'axios';

	export default {
  		name: 'Apply',
  		data () {
      		return {
		        machine: {
		          	os_name: '',
		          	os_version: '',
		          	comp_name: '',
		          	comp_version: '',
		          	machine_owner: this.$store.getters.username
		        }
		    }
		},

		methods: {
			addMachine() {

				axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;

      			axios.post(this.$store.state.endpoints.my_machine, this.machine)
		        .then((response) => {
		        	console.log(response);
		        	window.alert("Request succeeded!");
		        	this.$router.push('/profile');
		        })
		        .catch((error) => {
                console.log(error);
            	})


			}
		}
	}

</script>