<template>
  <v-app full-height density="compact">
    <!-- 顶部菜单 -->
    <v-app-bar v-if="active_menu" density="compact" color="primary">
      <template v-slot:prepend> <v-btn icon> <v-icon>mdi-arrow-left</v-icon> </v-btn> </template>
      {{ alert_msg }}
      <v-spacer></v-spacer>
      <v-btn @click="is_login = !is_login" :icon="is_login ? 'mdi-account-check' : 'mdi-account-plus'"></v-btn>
      <v-btn icon> <v-icon>mdi-dots-vertical</v-icon> </v-btn>
    </v-app-bar>

    <!-- 底部菜单 -->
    <v-bottom-navigation :active="active_menu" color="primary" z-index="2599">
      <v-btn value="toc" @click="set_menu('toc')">
        <v-icon>mdi-book-open-variant-outline</v-icon>
        <span>目录</span>
      </v-btn>
      <v-btn value="theme" @click="switch_theme">
        <v-icon>{{ switch_theme_icon }}</v-icon>
        <span>{{ switch_theme_text }}</span>
      </v-btn>
      <v-btn value="setting" @click="set_menu('settings')">
        <v-icon>mdi-cog</v-icon>
        <span>设置</span>
      </v-btn>
      <v-btn value="more" @click="set_menu('more')">
        <v-badge color="error" content="12">
          <v-icon>mdi-account-circle-outline</v-icon>
        </v-badge>
        <span>用户</span>
      </v-btn>
      <!--
      <v-btn value="more" @click="set_menu('more')">
        <v-icon>mdi-comment-text-outline</v-icon>
        <span>评论</span>
      </v-btn>
      -->
    </v-bottom-navigation>

    <v-bottom-sheet class="mb-14" max-height="90%" v-model="menu_settings" contained persistent z-index="234">
      <settings :settings="settings" @update="update_settings"></settings>
    </v-bottom-sheet>

    <v-bottom-sheet class="mb-14" max-height="90%" v-model="menu_toc" contained close-on-content-click z-index="234">
      <book-toc :meta="book_meta" :toc_items="toc_items" @click:select="on_click_toc"></book-toc>
    </v-bottom-sheet>

    <v-bottom-sheet class="mb-14" max-height="90%" v-model="menu_more" contained persistent z-index="234">
      <guest v-if="!is_login"></guest>
      <user v-else :messages="comments"></user>
    </v-bottom-sheet>

    <v-bottom-sheet class="" max-height="90%" v-model="menu_comments" contained style="z-index: 2600">
      <book-comments :login="is_login" :comments="comments" @click:add_review="on_add_review"></book-comments>
    </v-bottom-sheet>

    <!-- 浮动工具栏 -->
    <div id="comments-toolbar" :style="`left: ${toolbar_left}px; top: ${toolbar_top}px`">
      <v-toolbar density="compact" border dense floating elevation="10" rounded>
        <v-btn @click="on_click_toolbar_comments">发段评</v-btn>
        <v-divider vertical></v-divider>
        <v-btn>从这里听</v-btn>
        <v-divider vertical></v-divider>
        <v-btn>复制</v-btn>
        <v-divider vertical></v-divider>
        <v-btn>反馈</v-btn>
      </v-toolbar>
    </div>

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
      if (mode == "day") {
        this.settings.theme_mode = "night";
        this.rendition.themes.select(this.settings.theme_night);
      } else {
        this.settings.theme_mode = "day";
        this.rendition.themes.select(this.settings.theme_day);
      }
    },
    set_menu: function (target) {
      if (this.menu == target) {
        this.menu = 'hide';
      } else {
        this.menu = target;
      }
      console.log("set menu = ", this.menu);
      this.active_menu = true;
      this.menu_toc = false;
      this.menu_more = false;
      this.menu_settings = false;
      if (this.menu != 'hide') {
        this["menu_" + target] = true;
      }
    },
    update_settings: function (opt) {
      for (const key in opt) {
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
      this.hide_toolbar();
      const viewer = document.getElementById('reader');
      const width = viewer.offsetWidth;
      const x = event.clientX % viewer.offsetWidth;
      const y = event.clientY % viewer.offsetHeight;
      this.debug_click(x, y, width)

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
    on_select_content: function (cfiRange, contents) {
      console.log("on selectd", cfiRange, contents)
      var cfi = cfiRange.replace(/\[epub[^)]*\)\]/, '').replace(/,[^)]*/, '');
      console.log("get cfi = ", cfi)

      var p = contents.document.getElementById(cfi);
      // p.style.textDecoration = "underline";

      // 选中全部文字
      /*
      const range = contents.document.createRange();
      range.selectNodeContents(p);
      const selection = contents.window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      */


      // 把 toolbar 移动到段落附近
      const rect = p.getBoundingClientRect();
      const toolbar = document.getElementById('comments-toolbar');
      this.toolbar_left = (rect.width - toolbar.offsetWidth) / 2;
      if (rect.top >= (toolbar.offsetHeight + 64)) {
        this.toolbar_top = (rect.top - toolbar.offsetHeight - 12);
      } else {
        this.toolbar_top = (rect.bottom + 12);
      }

      this.selected_cfi = cfi;
      this.selected_cfi_base = contents.cfiBase;
      this.selected_segment_id = p.getAttribute("data-segment-id");

      // this.book.getRange(cfiRange).then((range) => {})

    },
    on_click_toolbar_comments: function () {
      console.log("点击发表评论按钮", this.selected_cfi_base, this.selected_segment_id)
      this.hide_toolbar();
      this.show_selected_comments(this.selected_cfi_base, this.selected_cfi, this.selected_segment_id);
    },
    on_keyup: function (e) {
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
    debug_click: function (x, y, width) {
      console.log("click at", x, y, width);
      if (!this.is_debug_click) return;

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
    init_listeners: function () {
      document.addEventListener('keyup', this.on_keyup, false);
      this.rendition.on('keyup', this.on_keyup, false);
      this.rendition.on('click', this.on_click_content, false);
      this.rendition.on('selected', this.on_select_content, false);
      this.rendition.hooks.content.register(this.load_comments);
      this.debug_signals();
    },
    debug_signals: function () {
      if (!this.is_debug_signal) return;
      var signals = ['click', 'selected', 'touchstart', 'touchend', 'touchmove'];
      var signals = ["added", "attach", "attached", "axis", "changed", "detach", "displayed", "displayerror", "expand", "hidden", "layout", "linkClicked", "loaderror", "locationChanged", "markClicked", "openFailed", "orientationchange", "relocated", "removed", "rendered", "resize", "resized", "scroll", "scrolled", "selected", "selectedRange", "shown", "started", "updated", "writingMode", "mouseup", "mousedown", "mousemove", "click", "touchend", "touchstart", "touchmove"]
      signals.forEach(sig => {
        this.rendition.on(sig, (e) => {
          this.alert_msg = sig;
          console.log(sig, e);
        }, false)
      });
    },
    init_themes: function () {
      this.rendition.themes.register("white", "themes.css");
      this.rendition.themes.register("dark", "themes.css");
      this.rendition.themes.register("grey", "themes.css");
      this.rendition.themes.register("brown", "themes.css");
      this.rendition.themes.register("eyecare", "themes.css");

      this.rendition.themes.select(this.settings.theme_day);
    },
    hide_toolbar: function () {
      this.toolbar_left = -999;
    },
    add_review: function (content) {
      const review = {
        bid: this.book_id,
        cfi: this.cfi,
        cfi_base: this.cfi_base,
        segment_id: this.segment_id,
      }
      const url = `/api/review/add`;

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(review),
      }).then(response => {
        if (!response.ok) {
          throw new Error('网络请求失败，状态码：' + response.status);
        }
        return response.json();
      });
    },
    load_comments: function (section) {
      // 在rendition加载完成后执行
      console.log("hook: ", section, section.cfiBase)

      var url = `/api/review/summary?bid=${this.review_bid}&cfi=${section.cfiBase}`;

      fetch(url).then(response => {
        if (!response.ok) {
          throw new Error('网络请求失败，状态码：' + response.status);
        }
        return response.json();
      }).then(rsp => {
        this.summary = {};
        rsp.data.list.forEach(item => {
          this.summary[item.segmentId] = item;
        })
        this.add_comment_icons(section);
      }).catch(function (error) {
        console.error('请求过程中出现错误：', error);
      });
    },
    show_selected_comments: function (cfiBase, cfi, segment_id) {
      const url = `/api/review/list?bid=${this.review_bid}&base=${cfiBase}&segment=${segment_id}&cfi=${cfi}`;
      fetch(url).then(rsp => rsp.json()).then(rsp => {
        this.comments = rsp.data.list;
        this.menu_comments = true;
        this.cfi_base = cfiBase;
        this.cfi = cfi;
        this.segment_id = segment_id;
        // this.set_menu("comments");
      })
    },
    add_comment_icons: function (section) {
      // 为每个段落添加评论图标和计数器
      const doc = section.document;
      const paragraphs = doc.getElementsByTagName("p");
      Array.from(paragraphs).forEach((p, index) => {
        // 获取段落的 CFI
        //const cfi = section.cfiFromElement(p);
        const cfi = new ePub.CFI(p, section.cfiBase).toString();
        // console.log(index, cfi, p.textContent)

        // 为段落添加唯一ID和CFI属性
        const paragraphId = `p-${section.cfiBase}-${index}`;
        p.setAttribute("data-segment-id", index);
        p.setAttribute("data-paragraph-id", paragraphId);
        p.setAttribute("data-cfi", cfi);
        p.setAttribute("id", cfi);

        // 获取当前段落的评论数量
        const state = this.summary[index];
        const count = state.reviewNum;
        const is_hot = state.is_hot ? "hot-comment" : "";

        // 创建评论计数器
        const commentCount = doc.createElement("span");
        commentCount.textContent = count > 0 ? count : "";
        commentCount.className = `comment-count ${is_hot}`;
        // 创建评论图标
        const commentContainer = doc.createElement("div");
        commentContainer.className = `comment-icon ${is_hot}`;

        // 将评论组件添加到段落末尾
        commentContainer.appendChild(commentCount);
        p.appendChild(commentContainer);

        commentContainer.addEventListener('click', (event) => {
          event.stopPropagation();
          console.log("点击评论按钮", paragraphId, section.cfiBase, cfi)
          this.show_selected_comments(section.cfiBase, cfi, index);
        });

      })
    },
  },
  mounted: function () {
    this.book = ePub("/guimi/");
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
      fetch(`/api/review/book?title=${this.book_title}`).then(rsp => rsp.json()).then(rsp => {
        this.review_bid = rsp.data.id;
      })
    });

    // 加载目录
    this.book.loaded.navigation.then(nav => {
      this.toc_items = nav.toc
    });

    window.rend = this.rendition

    this.init_listeners();
    this.init_themes();

    this.book.ready.then(() => {
      this.rendition.display('Text/Chapter_0217.xhtml');
    })

  },
  data: () => ({
    book: null,
    settings: {
      flow: "paginated",
      font_size: 18,
      brightness: 100,
      theme: "white",
      theme_mode: "day",
      theme_day: "white",
      theme_night: "grey",
    },
    server: "http://localhost/api/",
    is_login: true,
    book_title: "",
    book_meta: null,
    review_bid: 0,
    alert_msg: "x",
    rendition: null,
    auto_close: false,
    active_menu: true,
    menu: "hide",
    menu_toc: false,
    menu_more: false,
    menu_settings: false,
    menu_comments: false,
    theme_mode: "day",
    toc_items: [],
    comments: [],
    toolbar_left: -999,
    toolbar_top: 0,
    selected_segment_id: 0,
    selected_cfi_base: "",
    selected_cfi: "",
    is_debug_signal: true,
    is_debug_click: false,
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

#comments-toolbar {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 999;
}
</style>
