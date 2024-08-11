export default function(instance) {
    return {
        routes(pointIdArray) {
            // let query1 = "maps/routes?$"
            let queryParams = pointIdArray.map((n) => `points_ids=${n}`).join('&')
            return instance.get('maps/routes?' + queryParams)
        },
        bestRoute(pointIdArray) {
            let queryParams = pointIdArray.map((n) => `points_ids=${n}`).join('&')
            return instance.get('maps/routes/best?' + queryParams + '&with_total=false')
        },
    }
        
}