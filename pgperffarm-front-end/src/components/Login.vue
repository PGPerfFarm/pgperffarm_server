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
                  <v-form>
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
  import swal from 'sweetalert2';
  import router from '../router';

  export default {
    name: 'Login',

    data: () => ({
        credentials: {},
        valid: true,
        loading: false,
        rules: {
          username: [
            v => !!v || "Username is required",
            v => (v && v.length > 3) || "A username must be more than 3 characters long",
            v => /^[a-z0-9_]+$/.test(v) || "A username can only contain letters and digits"
          ],
          password: [
            v => !!v || "Password is required",
            v => (v && v.length > 5) || "The password must be longer than 5 characters"
          ]
        }
    }),
    methods: {
        login() {
          // checking if the input is valid
            if (this.$refs.form.validate()) {
              this.loading = true;
              axios.post('http://localhost:8000/profile/', this.credentials).then(res => {
                this.$session.start();
                this.$session.set('token', res.data.token);
                router.push('/');
              }).catch(e => {
                this.loading = false;
                swal({
                  type: 'warning',
                  title: 'Error',
                  text: 'Wrong username or password',
                  showConfirmButton:false,
                  showCloseButton:false,
                  timer:3000
                })
              })
            }
        }
    }
}
    
  </script>
