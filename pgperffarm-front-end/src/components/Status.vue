<template>
	<v-app>
		<main>
			<v-content>
				<v-layout justify-center column my-4>
					<v-flex>
      <v-card flat class="pg-v-card">
        <v-card-text class="pg-v-card-text-main">
            Status page
        </v-card-text>
      </v-card>
  </v-flex>
  <v-flex>
  	<v-layout row class="status-layout">
      <v-card flat>
            <v-card-title class="table-title">Shown here is the latest status of each farm member for each branch it has reported on in the last 30 days. Use the farm member link for history of that member on the relevant branch.
            </v-card-title>
        </v-card>
        <v-card flat>
              <v-btn @click="all">All</v-btn>
              <v-btn @click="none">None</v-btn>
          </v-card>
      </v-layout>
          <v-card flat class="pg-v-card">
					<template>
					  <v-expansion-panel 
					  expand
					  v-model="panel">
					    <v-expansion-panel-content
					      v-for="(item, i) in branches"
					      :key="i"
					    >
					      <template v-slot:header>
					        <div>{{item}}</div>
					      </template>
					      <v-card>
					        <v-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-card-text>
					      </v-card>
					    </v-expansion-panel-content>
					  </v-expansion-panel>
					</template>
				</v-card>
			</v-flex>
				</v-layout>
			</v-content>
		</main>
	</v-app>
</template>


<script>
	export default {
		name: 'Status',

		data: () => ({
			panel: [true, false, false, false],
			branches: ['Head', '10 stable', '9.6 stable', '9.5 stable']
		}),

		methods: {
      		all () {
        		this.panel = [true, true, true, true]
      		},

      		none () {
        		this.panel = [false, false, false, false]
      		},
		}
	}
</script>