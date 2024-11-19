<template>
        <v-list @click:select="click_toc">
            <template v-for="(item, idx) in toc_items">
                <v-list-item v-if="item.subitems.length == 0" prepend-icon="mdi-book-open-page-variant-outline"
                    :title="item.label" :value="item.href"></v-list-item>

                <v-list-group v-else :key="item.href">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" prepend-icon="mdi-book-open-page-variant-outline"
                            :title="item.label" :value="item.href"></v-list-item>
                    </template>

                    <v-list-item v-for="(subitem, subidx) in item.subitems" :key="item.href" :title="subitem.label"
                        :value="subitem.href"></v-list-item>
                </v-list-group>

            </template>
        </v-list>
</template>

<script>
export default {
    name: 'BookToc',
    computed: {
    },
    mounted: function () {
    },
    methods: {
        click_toc: function (item) {
            this.$emit('click:select', item);
        },

    },
    props: {
        toc_items: {
            type: Array,
            required: true
        }
    },
    data: () => ({
    })
}

</script>
