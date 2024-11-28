<template>
    <!-- 设置: 分别列出亮度、字体、背景、翻页、其他 五行设置项  -->
    <v-list density="compact">
        <v-list-item class="my-2">
            <v-row class="align-center">
                <v-col cols="2">
                    <span>亮度</span>
                </v-col>
                <v-col cols="9">
                    <v-slider hide-details v-model="opt.brightness" max="100" min="1" step=1
                        @update:modelValue="$emit('update', opt)"></v-slider>
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
                    <span class="d-inline-blockx text-center d-flex">{{ opt.font_size }}</span>
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
                        <v-btn :active="opt.flow == 'paginated'" @click='$emit("update", opt)'>左右点击翻页</v-btn>
                        <v-btn :active="opt.flow == 'scrolled'" @click='$emit("update", opt)'>上下滑动翻页</v-btn>
                    </v-btn-group>
                </v-col>
            </v-row>
        </v-list-item>

        <v-list-item class="my-2">
            <v-row style="margin-bottom: 1px">
                <v-col cols="2">
                    <span density="compact">章评</span>
                </v-col>
                <v-col cols="10">
                    <v-btn-group variant="outlined" divided density="compact">
                        <v-btn :active="opt.flow == 'paginated'" @click='$emit("update", opt)'>开启</v-btn>
                        <v-btn :active="opt.flow == 'scrolled'" @click='$emit("update", opt)'>关闭</v-btn>
                    </v-btn-group>
                </v-col>
            </v-row>
        </v-list-item>

        <v-list-item class="my-2">
            <v-row style="margin-bottom: 1px">
                <v-col cols="2">
                    <span density="compact">主题</span>
                </v-col>
                <v-col cols="2" v-for="item in themes">
                    <v-btn :active="opt.theme == item.name" density="compact" :icon="item.icon" :color="item.color"
                        @click='opt.theme = item.name; opt.theme_mode = item.mode; $emit("update", opt)'></v-btn>
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
        this.opt = {
            flow: this.settings.flow,
            theme: this.settings.flow,
            theme_mode: this.settings.theme_mode,
            font_size: this.settings.font_size,
            brightness: this.settings.brightness,
        }
    },
    methods: {
    },
    props: ['settings'],
    data: () => ({
        opt: {
            flow: "scrolled",
            theme: "eyecare",
            theme_mode: "day",
            font_size: 18,
            brightness: 100,
        },
        themes: [{
            name: "white",
            mode: "day",
            color: '#F6F6F6',
            icon: "mdi-weather-sunny",
        }, {
            name: "eyecare",
            mode: "day",
            color: '#D3E3D3',
            icon: "mdi-eye",
        }, {
            name: "grey",
            mode: "night",
            color: '#4B4B4B',
            icon: "mdi-weather-night",
        }, {
            name: "dark",
            mode: "night",
            color: '#1A1A1A',
            icon: "mdi-candle",
        } ],
    })
}

</script>
