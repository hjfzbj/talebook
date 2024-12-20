<template>
    <!-- 未登录的游客状态  -->
    <v-list>
        <v-list-item class="my-8 text-center">
            <v-btn stacked size="148" variant="text">
                <template v-slot:prepend>
                    <v-icon size="124">mdi-account-circle-outline</v-icon>
                </template>
                <span class="text-h6">点击登录</span>
            </v-btn>
        </v-list-item>
        <v-list-item class="my-2 text-center">
            即将跳转到外部页面，登录后将自动跳转回来
        </v-list-item>
</v-list>
</template>

<script>
export default {
    name: 'Guest',
    computed: {
    },
    mounted: function () {
    },
    methods: {
    },
    data: () => ({
    })
}

</script>
