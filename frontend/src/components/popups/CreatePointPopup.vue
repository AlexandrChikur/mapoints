<template>
  <div class="create_point_popup_root">
    <notifications/>

    <div class="popup_dark_wrapper" ref="popup_wrapper">
      <div class="create_point_popup popup">
        <div class="create_point_popup__header popup_header">
          NEW POINT
        </div>
        <div class="create_point_popup__form popup_form">
          <div class="create_point_popup__fields">
              <div class="create_point_popup__fields__name">
                <input type="text" placeholder="Name" class="create_point_popup__fields__name_name popup_field" v-model.trim="form.name">
              </div>
              <div class="create_point_popup__fields__coordinates">
                  <input type="text" placeholder="X" class="create_point_popup__fields__coordinates_x point_coord_field" v-model.trim="form.x">
                  <input type="text" placeholder="Y" class="create_point_popup__fields__coordinates_y point_coord_field" v-model.trim="form.y">
              </div>
              <div class="create_point_popup__fields__button">
                <input type="submit" value="Create" class="create_point_popup__fields__button cp popup_button" @click="createPoint">
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, numeric } from 'vuelidate/lib/validators'
export default {
    name: "CreatePointPopup",
    mixins: [ validationMixin ],
    props: {},
    data() {
        return {
          form: {
            name: '',
            x: null,
            y: null
          }
        }
    },
    validations: {
      form: {
        name: {
          required
        },
        x: {
          required,
          numeric
        },
        y: {
          required,
          numeric
        },
      }
    },
    computed: {},
    methods: {
      closePopUp() {
        this.$emit('closePopup')
      },
      createPoint() {
        this.$v.form.$touch()
        if (this.$v.form.$error) {
            if (this.$v.form.x.$dirty && !this.$v.form.x.numeric) {
              this.$notifyError("The X property should be only numeric") 
            } else if (this.$v.form.y.$dirty && !this.$v.form.y.numeric) {
              this.$notifyError("The Y property should be only numeric") 
            } else {
              this.$notifyError("Probably some field is empty. They are all is required") 
            }
        } else {
          this.$load(async() => {
            await this.$api.points.pointAdd({
                          name: this.form.name,
                          x: this.form.x,
                          y: this.form.y,
            })
            this.closePopUp()
            window.location.reload()
            this.$notifySuccess("The point were created successfully.")
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