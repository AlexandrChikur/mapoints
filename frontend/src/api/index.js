import instance from './instance'
import users from './users'
import points from './points'
import maps from './maps'

export default {
    users: users(instance),
    points: points(instance),
    maps: maps(instance),
}