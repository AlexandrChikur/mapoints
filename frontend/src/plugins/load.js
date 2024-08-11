export default {
    install(Vue) {
        Vue.prototype.$load = async (action) => {
            try {
                await action()
            } catch (error) {
                try {
                    console.error(error)
                    Vue.prototype.$notifyError(error.response.data.detail)
                } catch (error) {
                    console.error(error)
                    Vue.prototype.$notifyError("Happaned something unexpected. Send console log report to support team.")
                }
            }
        }
    }
}