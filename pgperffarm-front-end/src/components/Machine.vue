<template>
	<v-container fluid grid-list-md>
    <v-layout column>
      <v-card>
        <v-card-title>
          Farmer: name
        </v-card-title>
        no: y65yhgfdeeg
      </v-card>
    <v-layout>
      <v-flex d-flex xs12 sm6 md3>
              	<v-layout column>
	                <v-card flat class="profile-left-top">
	                  <v-card-title>Owner: name <br>
                    Report num: xyz</v-card-title>
	                </v-card>
	                <v-card flat class="profile-left-bottom">
	                	<v-card-text>
                      OS <br>
                      Processor <br>
                      email <br>
                      <v-btn> n branches involved </v-btn>
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

                      <v-tab v-for="item in items" :key="item">
                        {{ item }}
                      </v-tab>
                    </v-tabs>
                  </template>
                </v-toolbar>

                <v-tabs-items v-model="tab">
                  <v-tab-item v-for="item in items" :key="item">
                    <v-card flat>
                      <v-card-text>{{ text[items.indexOf(item)] }}</v-card-text>
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
    export default {
        name: 'Machine',

        data () {
            return {
              tab: null,
              items: [
                'Head', '10 stable', '9.6 stable', '9.5 stable'
              ],
              text: [1, 2, 3, 4]
            }
    }

  }


</script>