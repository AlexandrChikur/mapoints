<template>
    <div class="root_points-list">

        <div class="points-list" v-if="loggedIn">
            <create-point-popup v-if="isCreatePointPopUpVisible" @closePopup="closePopUp"/>
            <div class="points-list__header">
                <div class="points-list__header_title">My points</div>
                <div class="points__header__btns flex_nowrap cp">
                    <!-- <div class="points__header__btns__interact flex_nowrap">
                        <div class="points__header__btns__interact_text points__header__btn_txt">Interact</div>
                        <img src="../assets/img/ico/play.svg" alt="" class="points__header__btns_interact-icon points__header__btn_ico">
                    </div> -->
                    <div class="points__header__btns__create flex_nowrap cp">
                        <div class="points__header__btns__interact_text points__header__btn_txt" @click="showCreatePointPopUp">Create a point</div>
                        <img src="../assets/img/ico/add.svg" alt="" class="points__header__btns_add-icon points__header__btn_ico" @click="showCreatePointPopUp">
                    </div>
                </div>
            </div>
            <div class="points-list__body">
                <div v-if="points.length > 0" class="points-list__body-points">
                    <div v-for="(point, idx) in points" :key="idx" class="points-list__body-points-point">
                        <point-component 
                            :pointId="point.id"
                            :pointName="point.name" 
                            :authorId="point.user_id"
                            :authorName="point.author_name"
                            :coordX="point.x" 
                            :coordY="point.y"
                            :enabledDesciprion="true"
                        />
                    </div>
                </div>
                <div class="points__body__nothing" v-else>
                    Nothing here yet :)
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import PointComponent from './PointComponent.vue'
import CreatePointPopup from './popups/CreatePointPopup.vue'
export default {
  components: { PointComponent, CreatePointPopup },
    name: 'PointsComponent',
    props: ["loggedIn"],
    data() {
        return {
            isCreatePointPopUpVisible: false,
            points: []
        }
    },
    created() {
        if (this.loggedIn) {
            this.$load(async() => {
                const data = (await this.$api.points.userPointsList()).data
                this.points = data.results
            })
        }
    },
    methods: {
        showCreatePointPopUp() {
            this.isCreatePointPopUpVisible = true;
        },
        closePopUp() {
            this.isCreatePointPopUpVisible = false;
        },
        deletePoint(pointId) {
            let i = this.points.map(item => item.id).indexOf(pointId)
            this.points.splice(i, 1) 
        },
    },
    computed: {

    }
}
</script>

<style scoped>


</style>