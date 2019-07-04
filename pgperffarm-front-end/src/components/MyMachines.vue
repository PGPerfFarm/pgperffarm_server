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
                    <td class="profile-td">
                        <router-link :to="{path: props.item.uuid}">
                            {{ props.item.latest }}
                        </router-link>
                    </td>
                    <td class="profile-td">{{ props.item.addDate }}</td>
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

  methods: {

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

      axios.defaults.headers.common["Authorization"] = 'Token ' + this.$store.getters.token;

      var url = this.$store.state.endpoints.my_machine + '?page=1&machine_owner__username=' + this.$store.getters.username;

      axios.get(url)
        .then((response) => {

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
              info.email = response.data.results[i].lastest[0].machine_info.owner.email;
              uuid = '/records/' + response.data.results[i].lastest[0].uuid;
            }

            var machine = {
              alias: response.data.results[i].alias,
              system: response.data.results[i].os_name + ' ' + response.data.results[i].os_version + ' ' + response.data.results[i].comp_version,
              state: response.data.results[i].state,
              latest: lastest,
              uuid: uuid,
              addDate: response.data.results[i].add_time.substring(0, 10)
            };

            info.reports += response.data.results[i].reports;

            this.machines.push(machine);
          }

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
  }

}

</script>