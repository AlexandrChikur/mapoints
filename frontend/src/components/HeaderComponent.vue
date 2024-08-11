<template>
    <div class="root_header">
        <login-popup v-if="isLoginPopUpVisible" @closePopup="closePopUp"/>
        <signup-popup v-if="isSignUpPopUpVisible" @closePopup="closePopUp"/>

        <div class="header">
            <div class="header__title block_header_font_size">
                <div class="header__title_name">{{ this.$constants.TITLE }}</div>
                <div class="header__title_version">v.{{ this.$constants.VERSION }}</div>
            </div>
            <div class="header__user" v-if="loggedIn">
                <div class="header__user_name">{{ username }}</div>
                <img src="../assets/img/ico/logout.svg" class="header__user__logout_icon cp" @click="logOut">
            </div>
            <div class="header__auth" v-else>
                <ul>
                    <li><a class="header__auth__signin-popup-show" @click="showLoginPopup">SIGN IN</a></li>
                    <li><a class="header__auth__signup-popup-show" @click="showSignUpPopup">SIGN UP</a></li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import LoginPopup from '../components/popups/LoginPopup'
import SignupPopup from '../components/popups/SignupPopup'

export default {
    components: { LoginPopup, SignupPopup },
    name: 'HeaderComponent',
    props: ["loggedIn", "username", "userId" ],
    data() {
        return {
            isLoginPopUpVisible: false,
            isSignUpPopUpVisible: false,
        }
    },
    methods: {
        showLoginPopup() {
            this.isLoginPopUpVisible = true;
        },
        showSignUpPopup() {
            this.isSignUpPopUpVisible = true;
        },
        closePopUp() {
            this.isLoginPopUpVisible = false;
            this.isSignUpPopUpVisible = false;
        },
        logOut() {
            this.$store.dispatch('deleteToken')
            this.$store.dispatch('deleteUser')
        }
    },
}
</script>

<style scoped>


</style>