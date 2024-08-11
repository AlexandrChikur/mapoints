let Constants = {
    install(Vue) {
      Vue.prototype.$constants = {
        TITLE: "Mapoints",
        VERSION: "1.0.0",
        DEBUG: true
      };
    }
  };
  
  export default Constants;