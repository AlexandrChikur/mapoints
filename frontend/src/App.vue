<template>
  <div id="app">
    <notifications/>

    <header-component
        :loggedIn="loggedIn"
        :username="getUserName"
        :userId="getUserId"/>
    <points-list-component
        :loggedIn="loggedIn"
        :username="getUserName"
        :userId="getUserId"/>
    <points-component
        :loggedIn="loggedIn"
        :username="getUserName"
        :userId="getUserId"/>
    <route-component 
        :loggedIn="loggedIn"/>
  </div>
</template>

<script>
import HeaderComponent from './components/HeaderComponent'
import PointsComponent from './components/PointsComponent'
import PointsListComponent from './components/PointsListComponent.vue'
import RouteComponent from './components/RouteComponent.vue'

export default {
  name: 'App',
  components: {
    HeaderComponent,
    PointsComponent,
    PointsListComponent,
    RouteComponent,
  },
  computed: {
      
    loggedIn(){
        if(this.$store.getters.getUser){
          return this.$store.getters.getToken
        }
        return null;
      },
      getUserName(){
        if(this.$store.getters.getUser){
          return JSON.parse(this.$store.getters.getUser).username
        }
        return null;
      },
      getUserId(){
        if(this.$store.getters.getUser){
          return JSON.parse(this.$store.getters.getUser).id
        }
        return null;
      }
  }
}
</script>

<style>

</style>
