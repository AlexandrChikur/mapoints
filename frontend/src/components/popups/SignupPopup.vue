<template>
  <div class="signup_popup_root">
    <notifications/>
    <div class="popup_dark_wrapper" ref="popup_wrapper">
      <div class="signup_popup popup">
        <div class="signup_popup__header popup_header">
          SIGN UP
        </div>
        <div class="signup_popup__form">
          <div class="signup_popup__form__fields">
            <input type="text" placeholder="Login" class="signup_popup__form__fields_signup popup_field" v-model.trim="form.login">
            <input type="password" placeholder="Password" class="signup_popup__form__fields_password popup_field" v-model.trim="form.password">
            <input type="password" placeholder="Password Again" class="signup_popup__form__fields_password_again popup_field" v-model.trim="form.passwordAgain">
          </div>
          <div class="signup_popup__form__button">
            <input type="submit" value="Go" class="signup_popup__form__button_submit cp popup_button" @click="signUp">
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
    mixins: [ validationMixin ],
    name: "SignupPopup",
    props: {},
    data() {
        return {
          form: {
            login: '',
            password: '',
            passwordAgain: ''
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
        },
        passwordAgain: {
          passEqualsValidate(value) {
            return value == this.form.password
          },
          required
        }
      }
    },
    computed: {},
    methods: {
      closePopUp() {
        this.$emit('closePopup')
      },
      signUp() {
        this.$v.form.$touch()
        if (this.$v.form.passwordAgain.$dirty && !this.$v.form.passwordAgain.passEqualsValidate) {
            this.$notifyError("A passwords does not match")
        } else if (this.$v.form.$error) {
            this.$notifyError("Probably some field is empty. They are all is required")
        } else {
          this.$load(async() => {
            await this.$api.users.signUp({
                          username: this.form.login,
                          password: this.form.password
            })
            this.$notifySuccess("A user has been created successfully. Now you are able to log in.")
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
    },
}
</script>

<style>

</style>