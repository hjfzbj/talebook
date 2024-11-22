<template>
  <v-app full-height>
    <!-- 顶部菜单 -->
    <v-app-bar v-if="active_menu" density="compact" color="primary">
      <template v-slot:prepend> <v-btn icon> <v-icon>mdi-arrow-left</v-icon> </v-btn> </template>
      {{alert_msg}}
      <v-spacer></v-spacer>
      <v-btn icon> <v-icon>mdi-dots-vertical</v-icon> </v-btn>
    </v-app-bar>


    <!-- 底部菜单 -->
    <v-bottom-navigation :active="active_menu" color="primary" z-index="2599">
      <v-btn value="toc" @click="set_menu('toc')"> <v-icon>mdi-book-open-variant-outline</v-icon> <span>目录</span> </v-btn>
      <v-btn value="theme" @click="switch_theme"> <v-icon>{{ switch_theme_icon }}</v-icon> <span>{{ switch_theme_text }}</span> </v-btn>
      <v-btn value="setting" @click="set_menu('settings')"> <v-icon>mdi-cog</v-icon> <span>设置</span> </v-btn>
      <v-btn value="more" @click="set_menu('more')"> <v-icon>mdi-comment-text-outline</v-icon> <span>评论</span> </v-btn>
    </v-bottom-navigation>

    <v-bottom-sheet max-height="90%" v-model="menu_settings" contained persistent style="margin-bottom: 56px;" z-index="234">
      <settings :settings="settings" @update="update_settings"></settings>
    </v-bottom-sheet>

    <v-bottom-sheet max-height="90%" v-model="menu_toc" contained close-on-content-click style="margin-bottom: 56px;" z-index="234">
      <book-toc :meta="book_meta" :toc_items="toc_items" @click:select="on_click_toc"></book-toc>
    </v-bottom-sheet>

    <v-bottom-sheet max-height="90%" v-model="menu_more" contained close-on-content-click style="margin-bottom: 56px;" z-index="234">
        <!--
      <book-meta :meta="book_meta"></book-meta>
        -->
        <book-comments></book-comments>
    </v-bottom-sheet>

    <!-- 阅读界面 -->
    <v-main class="pa-0 fill-height">
        <div id="book-container" class="fill-height">
            <div id="reader" class="fill-height"></div>
        </div>
    </v-main>

  </v-app>
</template>

<script>
export default {
  name: 'EpubReader',
  components: {
  },
  computed: {
    switch_theme_icon: function () {
      return this.settings.theme_mode == "day" ? "mdi-weather-night" : "mdi-weather-sunny";
    },
    switch_theme_text: function () {
      return this.settings.theme_mode == "day" ? "夜晚" : "白天";
    },
  },
  methods: {
    switch_theme: function () {
        const mode = this.settings.theme_mode;
        if ( mode == "day" ) {
            this.settings.theme_mode = "night";
            this.rendition.themes.select(this.settings.theme_night);
        } else {
            this.settings.theme_mode = "day";
            this.rendition.themes.select(this.settings.theme_day);
        }
    },
    set_menu: function(target) {
        if ( this.menu == target ) {
            this.menu = 'hide';
        } else {
            this.menu = target;
        }
        console.log("set menu = ", this.menu);
        this.menu_toc = false;
        this.menu_more = false;
        this.menu_settings = false;
        if ( this.menu != 'hide' ) {
            this["menu_" + target] = true;
        }
    },
    update_settings: function (opt) {
        for ( const key in opt ) {
            this.settings[key] = opt[key];
        }
        // 更新主题设定
        const mode = opt["theme_mode"];
        const theme_key = "theme_" + mode;
        this.settings[theme_key] = this.settings.theme;
        this.rendition.themes.select(this.settings.theme);
    },
    on_click_toc: function (item) {
      console.log(item);
      this.rendition.display(item.id);
    },
    on_click_content: function (event) {
      const viewer = document.getElementById('reader');
      const width = viewer.offsetWidth;
      const x = event.clientX % viewer.offsetWidth;
      const y = event.clientY % viewer.offsetHeight;
      // this.show_click(x, y, width)

      if (x < width / 3) {
        // 点击左侧，往前翻页
        console.log("prev page")
        this.rendition.prev();
      } else if (x > width * 2 / 3) {
        // 点击右侧，往后翻页
        console.log("next page")
        this.rendition.next().then();
      } else {
        // 点击中间，显示菜单
        this.active_menu = !this.active_menu;
      }
    },
    on_keyup: function(e) {
        const c = e.keyCode || e.which;
        // Left & Up
        if (c == 37 || c == 38) {
            this.rendition.prev();
        }
        // Right & Down
        if (c == 39 || c == 40) {
            this.rendition.next();
        }
    },
    show_click: function (x, y, width) {
      console.log("click at", x, y, width)
      x = x - 10;
      y = y - 10;
      const dotDiv = document.createElement('div');
      dotDiv.classList.add('dot');
      dotDiv.style.left = `${x}px`;
      dotDiv.style.top = `${y}px`;

      document.body.appendChild(dotDiv);

      // 为每个点设置3秒后缓慢消失的效果
      setTimeout(() => {
        document.body.removeChild(dotDiv);
      }, 2000);
    },
    init_listeners: function() {
        document.addEventListener('keyup', this.on_keyup, false);
        this.rendition.on('keyup', this.on_keyup, false);
        this.rendition.on('click', this.on_click_content, false);

        var signals = ['click', 'selected', 'touchstart', 'touchend', 'touchmove'];
        var signals = ["added", "attach", "attached", "axis", "changed", "detach", "displayed", "displayerror", "expand", "hidden", "layout", "linkClicked", "loaderror", "locationChanged", "markClicked", "openFailed", "orientationchange", "relocated", "removed", "rendered", "resize", "resized", "scroll", "scrolled", "selected", "selectedRange", "shown", "started", "updated", "writingMode", "mouseup", "mousedown", "mousemove", "click", "touchend", "touchstart", "touchmove"]
        signals.forEach( sig => {
            this.rendition.on(sig, (e) => {
                this.alert_msg = sig;
                console.log(sig, e);
            }, false)
        });

    },
    init_themes: function() {
        this.rendition.themes.register("day", "themes.css");
        this.rendition.themes.register("dark", "themes.css");
        this.rendition.themes.register("night", "themes.css");
        this.rendition.themes.register("brown", "themes.css");
        this.rendition.themes.register("eyecare", "themes.css");

        /*
        this.rendition.themes.default({
          h2: {
            'font-size': '32px',
            color: 'purple'
          },
          p: {
            "margin": '10px'
          }
        });
        */

        this.rendition.themes.select('day');

    },
  },
  mounted: function () {
    this.book = ePub("/book/");
    this.rendition = this.book.renderTo("reader", {
      manager: "continuous",
      flow: this.settings.flow,
      width: "100%",
      height: "100%",
      //snap: true
    });

    this.book.loaded.metadata.then(metadata => {
        console.log(metadata);
        this.book_meta = metadata;
      this.book_title = metadata.title;
    });

    // 加载目录
    this.book.loaded.navigation.then(nav => {
      this.toc_items = nav.toc
    });

    window.rend = this.rendition

    this.init_listeners();

    this.book.ready.then( () => {
        this.rendition.display();
    })
    this.init_themes();

  },
  data: () => ({
    book: null,
    settings: {
        flow: "paginated",
        font_size: 18,
        brightness: 100,
        theme: "eyecare",
        theme_mode: "day",
        theme_day: "eyecare",
        theme_night: "night",
    },
    book_title: "",
    book_meta: null,
    alert_msg: "x",
    rendition: null,
    auto_close: false,
    active_menu: true,
    menu: "hide",
    menu_toc: false,
    menu_more: false,
    menu_settings: false,
    theme_mode: "day",
    toc_items: [],
    comments: [
      { icon: 'mdi-user', nick: "用户1", text: "这一一条评论", },
      { icon: 'mdi-user', nick: "用户1", text: "这一一条评论", },
      { icon: 'mdi-user', nick: "用户1", text: "这一一条评论", },
      { icon: 'mdi-user', nick: "用户1", text: "这一一条评论", },
      { icon: 'mdi-user', nick: "用户1", text: "这一一条评论", },
    ]

  })
}
</script>

<style>
.dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: rgba(255, 0, 0, 0.6);
  position: absolute;
  transition: opacity 1s ease-out;
  z-index: 999;
}
</style>
