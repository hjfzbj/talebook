<template>
  <v-card>
    <v-card-title>
      <h3 class="text-center">用户设置</h3>
    </v-card-title>

    <v-divider></v-divider>
    <v-card-text>消息</v-card-text>
    <v-list id="book-comments" density="compact" class="mr-4">
      <template v-for="c in messages">
        <v-list-item class="pr-0 align-self-start mb-4" :prepend-avatar="c.avatar" 
          :subtitle="c.nickName + ' @《宿命之环》'">
          <div class="my-2">{{ thumb_or_content(c) }}</div>
          <v-card variant="tonal" color="surface-variant" :subtitle="'这一段写得真厉害哦'"></v-card>
      </v-list-item>
      </template>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: 'User',
  computed: {
  },
  mounted: function () {
  },
  methods: {
    thumb_or_content: function (c) {
      if ( Math.random() > 0.5) {
        return c.content;
      } else {
        return "赞了你的评论"
      }

    },
  },
  props: ['messages'],
  data: () => ({
  })
}

</script>


<style>
#book-comments .v-list-item__append,
#book-comments .v-list-item__prepend {
  align-self: flex-start
}
</style>
