<template>
	<v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex d-flex xs12 sm6 md3>
            <v-layout column v-bind="binding">
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>Your information</v-card-title>
	                </v-card>
	                <v-card flat class="profile-left-bottom">
	                	<v-card-text>
                      Total reports: <br>
	                		N. machine(s): <br>
	                		N. branch(es) involved: <br>
	                		mail@mail.com
	                	</v-card-text>
	                </v-card>
            	</v-layout>
              </v-flex>
              <v-flex d-flex xs12>
              	<v-layout column>
	                <v-card flat class="profile-left-top"
	                >
	                  <v-card-title>Shortcuts</v-card-title>
                  </v-card>
                  <v-card flat class="profile-left-bottom">
                    <v-card-actions>
                    <v-btn block flat class="profile-button">Add a new machine</v-btn>
                    </v-card-actions>
                    <v-card-actions>
                    <v-btn block flat class="profile-button" v-on:click="logout()">Logout</v-btn>
                </v-card-actions>
	             </v-card>
	            </v-layout>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex d-flex fluid>
        <v-layout column>
          <v-card flat class="profile-card-title">
            <v-card-title class="profile-card-title-text">Welcome back, {{ $store.getters.username }}!</v-card-title>
          </v-card>
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
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'Profile',

  data: () => ({
      search: '',
      pagination: {
        sortBy: 'name'
      },

      headers: [
        { text: 'Alias', align: 'left', value: 'alias' },
        { text: 'System', value: 'system' },
        { text: 'State', value: 'state' },
        { text: 'Latest', value: 'latest' },
        { text: 'History', value: 'history' },
        { text: 'Add date', value: 'addDate' }
      ],

      machines: [
        {
          alias: 'Dandelion',
          system: 'Debian 9',
          state: 'active',
          latest: 'head',
          history: 'link',
          addDate: '2018-80-10'
        }
      ]
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
    logout() {
        this.$store.commit('removeToken', this.$store.state);
        this.$router.push("/");
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
    }
  }
}

</script>