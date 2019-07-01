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
                    <td class="profile-td">{{ props.item.latest }}</td>
                    <td class="profile-td">{{ props.item.addDate }}</td>
                  </tr>
                </template>
              </v-data-table>
            </template>
          </v-card>
        </template>

<script>

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

      machines: [
        {
          alias: 'Dandelion',
          system: 'Debian 9',
          state: 'active',
          latest: 'head',
          addDate: '2018-80-10'
        }
      ]
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
    }
  }
}

</script>