import axios from 'axios'

const instance = axios.create({
    baseURL: "http://localhost:8000/api/",
    // withCredentials: true,
    // headers: {
    //     accept: "application/json",
    //     "Access-Control-Allow-Origin": "*"
    // }
})

export default instance