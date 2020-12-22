<template>
    <div>
      <el-row type="flex" justify="center" class="main_text">
            <div v-if="!token" class="w_text">WiseAI</div>
            <div v-if="token" class="w_text">
              Welcome!
              <div style="text-align: center">
                {{ $store.getters.username }}
              </div>
            </div>
          </el-row>
    </div>
</template>

<script>
import { getToken } from "@/utils/auth";


export default {
    name: 'wise',
    data: () => {
      return {
        token: ""
      }
    },
    created() {
      this.token = getToken()
    }
}

</script>

<style lang="scss" scoped>
[v-cloak] {
  display: none !important;
}

.index_main {
  position: relative;
  .main_text {
    margin-top: 300px;
  }

  .w_text {
    font-size: 1.5em;
  }

}

// 中间文字的自适应
@media screen and (max-width: 1024px) {
  .index_main {
    .main_text {
      margin-top: 500px;
    }

    .w_text {
      font-size: 1.2em;
    }
  }
}

@media screen and (max-width: 768px) {
  .index_main {
    .main_text {
      margin-top: 400px;
    }

    .w_text {
      font-size: 1.2em;
    }
  }
}

@media screen and (max-width: 415px) {
  .index_main {
    .main_text {
      margin-top: 270px;
    }

    .w_text {
      font-size: 1.2em;
    }
  }
}

@media screen and (max-width: 415px) {
  .index_main {
    .main_text {
      margin-top: 200px;
    }

    .w_text {
      font-size: 1.1em;
    }
  }
}
</style>