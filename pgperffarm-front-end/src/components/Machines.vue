<template>
  <v-app>
  <main>
  <v-content>
  <v-layout justify-center column my-4>
    <v-flex>
      <v-card flat class="pg-v-card">
        <v-card-text class="pg-v-card-text-main">
            Machines list
            <v-btn block v-on:click="getMachines()">Get machines</v-btn>
        </v-card-text>
      </v-card>
  </v-flex>
  <v-flex>
      <v-card flat class="pg-v-card">
            <v-card-title class="table-title">Shown here is the latest status of each farm member for each branch it has reported on in the last 30 days. Use the farm member link for history of that member on the relevant branch.
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="search"
                label="Search"
                single-line
                hide-details
              ></v-text-field>
            </v-card-title>

            <!-- check server side pagination-->
            <template>
              <v-data-table
                :headers="headers"
                :items="machines"
                :pagination.sync="pagination"
                :search="search"
                select-all
                item-key="alias"
                class="elevation-1"
              >
              <template v-slot:no-data>
                <v-alert :value="true" color="error" icon="warning">
                  Sorry, nothing to display here :(
                </v-alert>
              </template>
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
                <template v-slot:items="props">
                  <tr>
                    <td class="profile-td">{{ props.item.alias }}</td>
                    <td class="profile-td">{{ props.item.system }}</td>
                    <td class="profile-td">{{ props.item.state }}</td>
                    <td class="profile-td">{{ props.item.latest }}</td>
                    <td class="profile-td">{{ props.item.history }}</td>
                    <td class="profile-td">{{ props.item.addDate }}</td>
                  </tr>
                </template>
              </v-data-table>
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
  name: 'Machines',

   data () {

      return {
      }
  },

  computed: {
    // fix this
      binding () {
        const binding = {}

        if (this.$vuetify.breakpoint.mdAndUp) binding.rows = true

        return binding
      }
  },


  methods: {
    logout() {
        this.$store.commit('removeToken', this.$store.state);
        this.$router.push("/");
    },

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

    getMachines() {
       axios.get(this.$store.state.endpoints.machines)
        .then((response) => {
          // alias = response.data.results[0].alias
          // system = response.data.results[0].os_name + os_version
          // state = state
          // latest = [] / 
          // history = link todo
          // addDate = add_time (fetch date)
          console.log(response)
        })
        .catch((error) => {
          console.log(error);
        })
    }
  }
}

</script>