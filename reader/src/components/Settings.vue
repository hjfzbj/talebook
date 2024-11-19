<template>
    <!-- 设置: 分别列出亮度、字体、背景、翻页、其他 五行设置项  -->
    <v-list density="compact">
        <v-list-item class="my-2">
            <v-row class="align-center">
                <v-col cols="2">
                    <span>亮度</span>
                </v-col>
                <v-col cols="9">
                    <v-slider hide-details v-model="brightness" max="100" min="1" step=1
                        @update:modelValue="$emit('update:brightness', this.brightness)"></v-slider>
                </v-col>
            </v-row>
        </v-list-item>

        <v-list-item class="my-2">
            <v-row class="align-center">
                <v-col cols="2">
                    <span class="text-justify">字体</span>
                </v-col>
                <v-col cols="3" height="48">
                    <v-btn variant="outlined" density="comfortable">A-</v-btn>
                </v-col>
                <v-col cols="2">
                    <span class="d-inline-blockx text-center d-flex">{{ font_size }}</span>
                </v-col>
                <v-col cols="3">
                    <v-btn variant="outlined" density="comfortable">A+</v-btn>
                </v-col>
            </v-row>
        </v-list-item>

        <v-list-item class="my-2">
            <v-row class="align-center">
                <v-col cols="2">
                    <span>翻页</span>
                </v-col>
                <v-col cols="10">
                    <v-btn-group variant="outlined" divided density="compact">
                        <v-btn>仿真</v-btn>
                        <v-btn>平移</v-btn>
                        <v-btn active>上下</v-btn>
                        <v-btn>覆盖</v-btn>
                    </v-btn-group>
                </v-col>
            </v-row>
        </v-list-item>

        <v-list-item class="my-2">
            <v-row style="margin-bottom: 1px">
                <v-col cols="2">
                    <span density="compact">主题</span>
                </v-col>
                <v-col cols="2">
                    <v-btn @click='$emit("update:theme", "day")' density="compact" icon="mdi-weather-sunny" color="#F6F6F6"></v-btn>
                </v-col>
                <v-col cols="2">
                    <v-btn @click='$emit("update:theme", "eyecare")' density="compact" icon="mdi-eye" color="#D3E3D3"></v-btn>
                </v-col>
                <v-col cols="2">
                    <v-btn @click='$emit("update:theme", "night")' density="compact" icon="mdi-weather-night" color="#4B4B4B"></v-btn>
                </v-col>
                <v-col cols="2">
                    <v-btn @click='$emit("update:theme", "dark")' density="compact" icon="mdi-weather-night" color="#1A1A1A"></v-btn>
                </v-col>
            </v-row>
        </v-list-item>
    </v-list>
</template>

<script>
export default {
    name: 'Settings',
    computed: {
    },
    mounted: function () {
    },
    methods: {
    },
    props: {
    },
    data: () => ({
        brightness: 100,
        font_size: 106,
    })
}

</script>
