<template>
    <div class="root_point">
        <div class="point cp" :style="{backgroundColor: randomColor()}" @click="showPointDetail()">
            <p class="point__letter">{{ pointId }}</p>
            <div class="point__description" :class="{point__description_visible: showDescription}" v-if="enabledDesciprion">
                <div class="point__description_author">{{ authorName }}</div>
                <div class="point__description_name" :title="pointName">{{ pointName }}</div>
                <div class="point__description_points">
                    <div>
                        <div class="point__description_point">
                        <div class="point__description_points_coord_name">X</div>
                        <div class="point__description_point_coord_value point_coord_value">{{ coordX }}</div>
                        </div>
                        <div class="point__description_point">
                            <div class="point__description_points_coord_name">Y</div>
                            <div class="point__description_point_coord_value point_coord_value">{{ coordY }}</div>
                        </div>
                    </div>
                    <div>
                        <div class="point__description__point__delete" @click="deletePoint">Delete</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PointComponent',
    props: ["pointId", "pointName", "authorId", "authorName", "coordX", "coordY", "enabledDesciprion"],
    data() {
        return {
            pointBgColors: [
                "#8790FF", "#A7ADFF", "#5F6BFF", "#656CBF", "#1F29A6",
                "#8560BF", "#521CA6", "#9856FF", "#B280FF", "#C6A2FF",
                "#5D9BBF", "#1A72A6", "#50BEFF", "#50BEFF", "#9EDBFF",
                "#BFA357", "#A68016", "#FFCD45", "#FFDA74", "#FFE499"
            ],
            showDescription: false,
        }
    },
    methods: {
        randomColor(){
            const random = Math.floor(Math.random() * this.pointBgColors.length);
            return this.pointBgColors[random];
        },
        showPointDetail(){
            this.showDescription = !this.showDescription;
        },
        // getPointLetter(){
        //     return this.pointName.slice(0,1).toUpperCase()
        // },
        deletePoint() {
            this.$load(async() => {
                await this.$api.points.deletePointById(this.pointId)
                window.location.reload()
                this.$notifySuccess("This point were successfully deleted.")
          })
        }
    },
}
</script>

<style scoped>


</style>