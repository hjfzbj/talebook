<template>
    <v-list density="compact">
        <template v-for="c in comments">
            <v-list-item align=start class="mb-4" slim :prepend-avatar="c.avatar" append-icon="mdi-thumb-up" :title="c.nickName">
                <v-list-item-content>{{c.content}}</v-list-item-content>
                <v-list-item-subtitle>{{c.level}}楼 * {{c.createTime}} * {{c.ipAddress}}</v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-avatar class="text-center" :icon="c.avatar"></v-avatar>
                </template>
                <template v-slot:append>
                    <v-icon icon="mdi-thumb-up"></v-icon>
                    <br></br>
                    {{c.likeCount}}
                </template>
            </v-list-item>

        </template>
    </v-list>
</template>

<script>
export default {
    name: 'BookComments',
    computed: {
    },
    mounted: function () {
        fetch('/comments.json').then(function(response) {
            if (!response.ok) {
                throw new Error('网络请求失败，状态码：' + response.status);
            }
            return response.json();
        })
        .then( rsp => {
            this.comments = rsp.data.list;
            console.log(this.comments);
        })
        .catch(function(error) {
            console.error('请求过程中出现错误：', error);
        });
    },
    methods: {
    },
    props: {
    },
    data: () => ({
        comments: [],
    })
}

</script>
