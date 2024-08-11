<template>
    <div class="root_route">
        <div class="routes">
            <div class="routes__header">
                <div class="routes__header_title">Routes</div>
                <div class="routes__header_description">You must provide points ids</div>
                <div class="routes__header_buttons">
                    <div class="routes__header_buttons-add cp">
                        <input type="text" name="" id="" class="routes__header_buttons-add_input" placeholder="ID" v-model="form.id">
                        <img src="../assets/img/ico/addPoint.svg" alt="" class="routes__header_buttons-add-btn" @click="addPoint">
                    </div>
                    <div class="routes__header_buttons-autoAdd cp" v-if="loggedIn" @click="autoAddPoints">
                        <img src="../assets/img/ico/autoAddPoint.svg" alt="" class="routes__header_buttons-autoAdd-btn">
                        <div>Auto add all created points</div>
                    </div>
                </div>
            </div>
            <div class="routes__points-area">
                <div v-for="(pointAreaItem, idx) in pointsArea" :key="idx" class="routes__points-area-item cp" @click="removePointId(idx)">
                    {{ pointAreaItem.value }}
                </div>
            </div>
            <div class="routes__footer">
                <div class="routes__footer_help-info">
                    Use LMB to delete added point
                </div>
                <div class="routes__footer_buttons">
                    <input type="submit" value="Clean" class="routes__footer_buttons-clean cp " @click="cleanArea">
                    <input type="submit" value="Build All" class="routes__footer_buttons-build-all cp popup_button" @click="buildAllRoutes">
                    <input type="submit" value="Build Best Way" class="routes__footer_buttons-build-best cp popup_button" @click="buildBestRoute">
                </div>
            </div>
            <div class="routes__routes-area">
                <div class="routes__routes-area-clean">
                    <input type="submit" value="Clean Routes" class="routes__routes-area-clean-btn cp" @click="cleanRoutes">
                </div>
                <atom-spinner
                    :animation-duration="1000"
                    :size="60"
                    :color="'#ff1d5e'"
                v-if="showSpinner"/>
                <div class="routes__routes-area-item" v-for="(route, idx) in builtRoutes" :key="idx">
                    <points-chain-component 
                        :pointList="route.route"
                        :totalDist="route.total"
                        :isBest="false"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, numeric } from 'vuelidate/lib/validators'
import { AtomSpinner } from 'epic-spinners'
import PointsChainComponent from './PointsChainComponent.vue'
export default {
    components: { PointsChainComponent, AtomSpinner},
    mixins: [ validationMixin ],
    name: 'RouteComponent',
    props: ["loggedIn"],
    data() {
        return {
            pointsArea: [],
            builtRoutes: [],
            form: {
                id: null
            },
            showSpinner: false
        }
    },
    validations: {
      form: {
        id: {
          required,
          numeric
        }
      },
    },
    methods: {
        cleanArea(){
            this.pointsArea = []
        },
        cleanRoutes() {
            this.builtRoutes = []
        },
        buildAllRoutes() {
            if (this.pointsArea.length > 0) {
                this.cleanRoutes();
                this.$load(async() => {
                    this.showSpinner = true
                    const map = (await this.$api.maps.routes(this.pointsArea.map((obj) => obj.value))).data
                    this.parseMap(map)
                })
            }

        },
        parseMap(map){
            var routes = []
            for (const route of map) {
                var idx = 0;
                var full_route = [];
                var route_total = 0;
                for (const pair of route) {
                    full_route.push(pair.from)
                    route_total += pair.dist
                    if (idx === route.length - 1) {
                        full_route.push(pair.to)
                    }
                    idx += 1
                }
                routes.push({
                    route: full_route,
                    total: route_total
                })
            }
            this.showSpinner = false;
            this.builtRoutes = routes
        },
        parseRoute(route) {
            var routes = []

            var idx = 0;
            var full_route = [];
            var route_total = 0;
            for (const pair of route) {
                full_route.push(pair.from)
                route_total += pair.dist
                if (idx === route.length - 1) {
                    full_route.push(pair.to)
                }
                idx += 1
            }
            routes.push({
                route: full_route,
                total: route_total
            })
            this.showSpinner = false;
            this.builtRoutes = routes
        },
        buildBestRoute() {
            if (this.pointsArea.length > 0) {
                this.cleanRoutes();
                this.$load(async() => {
                    this.showSpinner = true
                    const map = (await this.$api.maps.bestRoute(this.pointsArea.map((obj) => obj.value))).data
                    this.parseRoute(map.route)
                })
            }
        },
        removePointId(idx) {
            this.pointsArea.splice(idx, 1)
        },
        addPoint() {
            this.$v.form.$touch()
            if (this.$v.form.$error) {
                if (this.$v.form.id.$dirty && !this.$v.form.id.numeric) {
                    this.$notifyError("ID property should be numeric only") 
                } else if (this.$v.form.id.$dirty && !this.$v.form.id.required) {
                    this.$notifyError("ID Field should not be empty") 
                }
            } else {
                this.pointsArea.push({value: this.form.id})
            }
        },
        autoAddPoints() {
            this.$load(async() => {
                const points = (await this.$api.points.userPointsList()).data
                points.results.forEach(point => {
                    this.pointsArea.push({value: point.id})
                });
                this.$notifySuccess("The User's point were added to area successfully.")
            })
        }
    },
}
</script>

<style scoped>


</style>