<template>
    <v-app>
    <main>
      <v-content>
        <pg-toolbar></pg-toolbar>
        <pg-navbar></pg-navbar>

            <v-container>
            <v-layout column>
              <v-flex xs4>
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
                      <v-text-field prepend-icon="person" name="username" v-model="input.username" label="Username" type="text"></v-text-field>
                      <v-text-field prepend-icon="lock" name="password" v-model="input.password" label="Password" id="password" type="password"></v-text-field>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn v-on:click="login()">Login</v-btn>
                  </v-card-actions>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>

        <pg-footer></pg-footer>
      </v-content>
    </main>
  </v-app>
</template>

<script>
    import PgNavbar from './Navbar.vue'
    import PgFooter from './Footer.vue'
    import PgToolbar from './Toolbar.vue'

    import PGUtil from '../util/util.jsx'
    import PGConstant from '../util/constant.jsx'
    import User from '../service/user-service.js'

    const util = new PGUtil();
    const user = new User();

    export default {
        name: 'Login',
        components: {
            PgNavbar,
            PgFooter,
            PgToolbar
        },
        data() {
            return {
                input: {
                    username: "",
                    password: ""
                }
            }
        },

        methods: {
            login() {

                let username = this.input.username
                let password = this.input.password

                if(username != "" && password != "") {

                    let loginInfo = {username, password}
                    
                    user.login(loginInfo).then((res) => {

                        util.setStorage('userInfo', res);
                        window.alert('Login succeeded!');
                        window.location.href = this.state.redirect;

                    }, (err) => {

                        if (PGConstant.AuthorizedErrorCode === err) {
                            util.errorTips('Wrong username or password!');
                        }
                        else {
                            // ReferenceError: $ is not defined
                            window.alert(err);
                        }

                    });

                // this.$emit("authenticated", true);
                // this.$router.replace({ name: "secure" });
                // this.$store.dispatch('login', { email, password })
                // .then(() => this.$router.push('/'))
                // .catch(err => console.log(err))

            }

                else {
                    window.alert('Empty username or password!');
                }
            }
        }
    }
</script>
