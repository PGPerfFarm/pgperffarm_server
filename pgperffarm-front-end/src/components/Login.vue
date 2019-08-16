<template>
  <v-app>
    <main>
      <v-content>
        <v-container>
          <v-layout column>
            <v-flex>
              <v-card flat class="login-v-card-upper">
                <img src="../assets/images/full-logo.png" height="10%" width="10%" align-center>
                <div class="login-v-card-upper-toolbar">
                  <v-toolbar-title class="login-v-card-upper-toolbar-title">Log in to manage your machines!</v-toolbar-title>
                </div>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card flat class="login-v-card">
                <v-card-text>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-text-field 
                    prepend-icon="person" 
                    name="username" 
                    label="Username" 
                    type="text"
                    v-model="credentials.username"
                    :counter="20"
                    :rules="rules.username"
                    maxlength="20"
                    required
                    >
                    </v-text-field>
                    <v-text-field 
                    prepend-icon="lock" 
                    name="password" 
                    label="Password" 
                    id="password" 
                    type="password"
                    v-model="credentials.password"
                    :counter="20"
                    :rules="rules.password"
                    maxlength="20"
                    required
                    > 
                    </v-text-field>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-btn block class="login-button" :disabled="!valid" v-on:click="login()">Login</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
    </main>
  </v-app>
</template>

<script>
  import axios from 'axios';

  // curl -d '{"username":"test", "password":"password"}' -H "Content-Type: application/json" -X POST http://localhost:8000/login/

  export default {
    name: 'Login',

    data () {
      return {
        credentials: {
          username: '',
          password: '',
        },
        valid: true,
        loading: false,
        rules: {
          username: [
            v => !!v || "Username is required",
            v => (v && v.length > 1) || "A username must be more than 1 character long",
            v => /^[a-z0-9_]+$/.test(v) || "A username can only contain letters and digits"
          ],
          password: [
            v => !!v || "Password is required",
            v => (v && v.length > 5) || "The password must be longer than 5 characters"
          ]
        }
      }
    },

    methods: {
      login() {
          // checking if the input is valid
            if (this.$refs.form.validate()) {
              this.loading = true;

              axios.post(this.$store.state.endpoints.obtainJWT, this.credentials)
              .then((response) => {
                    this.$store.commit('updateToken', response.data.access)

                    axios.defaults.headers.common["Authorization"] = 'Bearer ' + this.$store.getters.token;
                    var url = this.$store.state.endpoints.users + this.credentials.username + '/';

                    axios.get(url)
                    .then((response) => {

                        var email = response.data.email;
                        email = email.replace('@', '<at>');

                        this.$store.commit('setAuthUser', {authUser: response.data.username, isAuthenticated: true, email: email})
                        this.$router.push('/profile');
                      })
                    .catch((error) => {
                      window.alert("Server error!");
                      console.log(error);
                    });

                  })
                  .catch((error) => {
                    window.alert("Wrong username or password!");
                    console.log(error);
                  });
            }
        },

    }
}
    
  </script>
