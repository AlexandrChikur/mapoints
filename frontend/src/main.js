import Vue from 'vue'
import App from './App.vue'
import NotifyPlugin from 'vue-easy-notify'
import 'vue-easy-notify/dist/vue-easy-notify.css'
import store from './store/index'

import '../src/assets/styles/main.css'

import Constants from './plugins/Constants'
import ApiPlugin from './plugins/api'
import LoadPlugin from './plugins/load'

Vue.config.productionTip = false

Vue.use(Constants)
Vue.use(NotifyPlugin)
Vue.use(ApiPlugin)
Vue.use(LoadPlugin)

new Vue({
  render: h => h(App),
  store
}).$mount('#app')
