export default {
    // namespaced: true,
    state: {
        status: { loading: true },
        user: localStorage.getItem('user'),
        token: localStorage.getItem('token') || null,
    },
    getters: {
        getToken(state) {
            return state.token
        },
        getUser(state) {
            return state.user
        },
    },
    actions: {
        setToken({ commit }, payload) {
            commit('SET_TOKEN', payload)
        },
        deleteToken({ commit }) {
            commit('DELETE_TOKEN')
        },

        setUser({ commit }, payload) {
            commit('SET_USER', payload)
        },
        deleteUser({ commit }) {
            commit('DELETE_USER')
        }
    },
    mutations: {
        SET_TOKEN(state, payload) {
            state.token = payload
        },
        DELETE_TOKEN(state) {
            localStorage.removeItem('token')
            state.token = localStorage.getItem('token') || null
        },
        SET_USER(state, payload) {
            state.user = payload
        },
        DELETE_USER(state) {
            localStorage.removeItem('user')
            state.user = localStorage.getItem('user') || null
        }
    },
}