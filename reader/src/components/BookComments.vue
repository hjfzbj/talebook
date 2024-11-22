<template>
    <v-list id='book-comments' density="compact">
        <template v-for="c in comments">
            <v-list-item class="pr-0 align-self-start mb-4" :prepend-avatar="c.avatar" append-icon="mdi-thumb-up" :title="c.nickName">
                    {{c.content}}
                <v-list-item-subtitle>{{c.level}}楼 * {{c.createTime}} * {{c.ipAddress}}</v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-avatar class="text-center" :icon="c.avatar"></v-avatar>
                </template>
                <template v-slot:append>
                    <v-btn class="px-0" size="small" variant=plain stacked prepend-icon="mdi-thumb-up">{{c.likeCount}}</v-btn>
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

<style>
#book-comments .v-list-item__append,
#book-comments .v-list-item__prepend {
    align-self: flex-start
}
</style>
