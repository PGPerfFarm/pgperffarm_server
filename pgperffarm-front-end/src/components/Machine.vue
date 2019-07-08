<template>
	<v-container fluid grid-list-md>
    <v-layout column>
      <v-card class="machine-main-card">
        <v-card-title class="machine-main-title">
          Machine page
        </v-card-title>
        <v-card-text class="machine-main-text">
          Farmer: {{ this.$route.params.alias }} <br>
          Number: {{ serial_number }}
        </v-card-text>
      </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>Owner: {{ owner.username }} <br>
                    Reports: {{ reports }} <br>
                    {{ branches_involved }} branch(es) involved
                  </v-card-title> 
	                </v-card>
	                <v-card class="profile-left-bottom">
	                	<v-card-text>
                      <v-icon color="rgb(51, 103, 145)">computer</v-icon> OS: {{ os }} <br>
                      <v-icon color="rgb(51, 103, 145)">border_all</v-icon> Processor: {{ compiler }} <br>
                      <v-icon color="rgb(51, 103, 145)">email</v-icon> Email: <a :href="`mailto:${owner.email}`"> {{ owner.email }} </a> <br>
	                	</v-card-text>
	                </v-card>
            	</v-layout>
      </v-flex>
      <v-flex d-flex fluid>
          <v-card flat class="profile-card-title">
                <v-toolbar color="cyan" dark tabs>
                  <v-toolbar-title>Machine by branch</v-toolbar-title>
                  <v-spacer></v-spacer>

                  <template v-slot:extension>
                    <v-tabs
                      v-model="tab"
                      color="cyan"
                      align-with-title
                    >
                      <v-tabs-slider color="yellow"></v-tabs-slider>

                      <v-tab v-for="item in branches" :key="item">
                        {{ item }}
                      </v-tab>
                    </v-tabs>
                  </template>
                </v-toolbar>

                <v-tabs-items v-model="tab">
                  <v-tab-item v-for="item in branches" :key="item">
                    <v-card flat>
                      <v-card-title> {{ item }} </v-card-title>
                      <template>
                                <v-data-table
                                 hide-actions
                                 :headers="headers"
                                 :items="machines[item]"
                                 :search="search"
                                 :loading="loading"
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
                                        >
                                            <v-icon small>arrow_upward</v-icon>
                                            {{ header.text }}
                                        </th>
                                      </tr>
                                  </template>
                                  <template v-slot:items="props">
                                      <tr>
                                      <td class="profile-td">{{ props.item.alias }}</td>
                                        <td class="profile-td">{{ props.item.trending.improvement }}</td>
                                        <td class="profile-td">{{ props.item.trending.status_quo }}</td>
                                        <td class="profile-td">{{ props.item.trending.regression }}</td>
                                        <td class="profile-td">
                                          <router-link :to="{path: props.item.detail}">
                                            <v-icon color="rgb(51, 103, 145)">link</v-icon>
                                            Link
                                          </router-link>
                                        </td>
                                        <td class="profile-td">
                                          <a :href=props.item.commit target="_blank"> <u>{{ props.item.commit.substring(63, 70) }} </u></a>
                                        </td>
                                        <td class="profile-td">{{ props.item.date }}</td>
                                      </tr>
                                  </template>
                                </v-data-table>
                            </template>
                    </v-card>
                  </v-tab-item>
                </v-tabs-items>
          </v-card>
      </v-flex>
    </v-layout>
  </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'Machine',

    data: () => ({
      tab: null,
      branches: ['Head', '10 stable', '9.6 stable', '9.5 stable'],

      search: '',
      loading: true,

      headers: [
            { text: 'Alias', align: 'left', value: 'alias', sortable: true },
            { text: 'Improvement', value: 'improvement'},
            { text: 'Status quo', value: 'status_quo'},
            { text: 'Regression', value: 'regression'},
            { text: 'Detail', value: 'detail'},
            { text: 'Commit', value: 'commit'},
            { text: 'Date', value: 'date' }
          ],

          machines: {
          'Head': [],
          '10 stable': [],
          '9.6 stable': [],
          '9.5 stable': []
      },

      branches_involved: 0,
      reports: 0,
      owner: '',
      os: '',
      compiler: '',
      serial_number: '',

    }),

    methods: {

          getMachine() {
            var machine_name = this.$route.params.alias;

            axios.get(this.$store.state.endpoints.machine)
            .then((response) => {

              axios.get(this.$store.state.endpoints.machines)
              .then((response) => {

                for(var i = 0; i < response.data.count; i++)
                  if (response.data.results[i].alias == machine_name) 
                    this.serial_number = response.data.results[i].machine_sn;
                    
              });

              var commit_url = 'https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=';

              for(var i = 0; i < response.data.count; i++) {

                if (response.data.results[i].machine_info.alias == machine_name) {

                  this.reports += 1;

                  this.owner = {
                    username: response.data.results[i].machine_info.owner.username,
                    email: response.data.results[i].machine_info.owner.email,
                  }

                  this.os = response.data.results[i].machine_info.os_name + ' ' + response.data.results[i].machine_info.os_version;
                  this.compiler = response.data.results[i].machine_info.comp_version;

                  var machine = {
                    alias: response.data.results[i].machine_info.alias,
                        system: response.data.results[i].machine_info.os_name + ' ' + response.data.results[i].machine_info.os_version + ' ' + response.data.results[i].machine_info.comp_version,
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
                }

              }

              if (this.machines['Head'].length > 0)
                    this.branches_involved += 1;
                  if (this.machines['10 stable'].length > 0)
                    this.branches_involved += 1;
                  if (this.machines['9.6 stable'].length > 0)
                    this.branches_involved += 1;
                  if (this.machines['9.5 stable'].length > 0)
                    this.branches_involved += 1;

                this.loading = false;
             })
            .catch((error) => {
                console.log(error);
            })
      }
    },

    mounted() {
        this.getMachine();
      }

  }

</script>