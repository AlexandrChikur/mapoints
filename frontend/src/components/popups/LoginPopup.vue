<template>
  <div class="login_popup_root">
      <notifications/>

      <div class="popup_dark_wrapper" ref="popup_wrapper">
        <div class="login_popup popup">
          <div class="login_popup__header popup_header">
            LOG IN
          </div>
          <div class="login_popup__form">
            <div class="login_popup__form__fields">
              <input type="text" placeholder="Login" class="login_popup__form__fields_login popup_field" v-model.trim="form.login">
              <input type="password" placeholder="Password" class="login_popup__form__fields_password popup_field" v-model.trim="form.password">
            </div>
            <div class="login_popup__form__button">
              <input type="submit" value="Go" class="login_popup__form__button_submit cp popup_button" @click="logIn">
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
    name: "LoginPopup",
    props: {},
    mixins: [ validationMixin ],
    data() {
        return {
          form: {
            login: '',
            password: '',
          }
        }
    },
    validations: {
      form: {
        login: {
          required
        },
        password: {
          required
        }
      }
    },
    computed: {},
    methods: {
      closePopUp() {
        this.$emit('closePopup')
      },
      logIn() {
        this.$v.form.$touch()
        if (this.$v.form.$error) {
            this.$notifyError("Probably some field is empty. They are all is required") 
        } else {
          this.$load(async() => {
            const data = (await this.$api.users.logIn({
                          username: this.form.login,
                          password: this.form.password
            })).data
            localStorage.setItem("user", JSON.stringify(data.user))
            localStorage.setItem("token", data.user.token)
            this.$store.dispatch('setUser', JSON.stringify(data.user))
            this.$store.dispatch('setToken', data.user.token)
            this.$notifySuccess("You are logged in successfully")
            this.closePopUp()
          })
        }
      }
    },
    mounted() {
      let vm = this;
      document.addEventListener('click', function(item){
        if(item.target == vm.$refs['popup_wrapper']){
          vm.closePopUp();
        }
      })
    }
}
</script>

<style>

</style>