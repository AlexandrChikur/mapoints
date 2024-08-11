export default function(instance) {
    return {
        signUp(payload) {
            return instance.post('users/signup', payload)
        },
        logIn(payload) {
            return instance.post('users/login', payload)
        },
        userById(userId) {
            const url = "users/" + userId
            return instance.get(url)
        },
    }
}