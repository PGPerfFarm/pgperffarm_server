<template>
  <v-app>
  <main>
  <v-content>
  <v-layout justify-center column my-4>
    <v-flex>
      <v-card flat class="pg-v-card">
        <v-card-text class="pg-v-card-text-main">
            Machines list
        </v-card-text>
      </v-card>
  </v-flex>
  <v-flex>
      <v-card flat class="pg-v-card">
            <v-card-title class="table-title">Shown here is the machine list, along with a summary of relevant information.
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
                <template v-slot:items="props">
                  <tr>
                    <td class="profile-td">{{ props.item.alias }}</td>
                    <td class="profile-td">{{ props.item.system }}</td>
                    <td class="profile-td">{{ props.item.state }}</td>
                    <td class="profile-td">{{ props.item.latest }}</td>
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

  data: () => ({
      search: '',
      loading: true,
      pagination: {
        sortBy: 'name'
      },

      headers: [
        { text: 'Alias', align: 'left', value: 'alias' },
        { text: 'System', value: 'system' },
        { text: 'State', value: 'state' },
        { text: 'Latest', value: 'latest' },
        { text: 'Add date', value: 'addDate' }
      ],

      machines: [],
        
  }),

  computed: {
    // fix this
      binding () {
        const binding = {}

        if (this.$vuetify.breakpoint.mdAndUp) binding.rows = true

        return binding
      }
  },


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

    getMachines() {
       axios.get(this.$store.state.endpoints.machines)
        .then((response) => {

          for(var i = 0; i < response.data.count; i++) {

            var lastest = '';

            if (response.data.results[i].lastest.length > 0)
              lastest = response.data.results[i].lastest[0].branch;

            var machine = {
              alias: response.data.results[i].alias,
              system: response.data.results[i].os_name + ' ' + response.data.results[i].os_version + ' ' + response.data.results[i].comp_version,
              state: response.data.results[i].state,
              latest: lastest,
              addDate: response.data.results[i].add_time.substring(0, 10)
            };

            this.machines.push(machine);
          }

          this.loading = false;

        })
        .catch((error) => {
          console.log(error);
        })
    }
  },

  mounted() {
    this.getMachines();
  }

}

</script>