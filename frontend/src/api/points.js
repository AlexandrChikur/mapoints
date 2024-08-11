export default function(instance) {
    return {
        pointsList() {
            return instance.get('points')
        },
        pointsListLookup(lookup) {
            return instance.get('points', {
                params: {
                    lookup: lookup
                }
            })
        },
        userPointsList() {
            const token = localStorage.getItem("token")
            return instance.get('points/my', {
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
        },
        pointAdd(payload) {
            const token = localStorage.getItem("token")
            return instance.post('points', payload, {
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
        },
        pointById(pointId) {
            const url = "points/" + pointId
            return instance.get(url)
        },
        deletePointById(pointId) {
            const url = "points/my/" + pointId
            const token = localStorage.getItem("token")
            return instance.delete(url,{
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
        },
    }
}