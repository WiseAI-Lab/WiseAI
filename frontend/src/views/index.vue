<template>
  <div style="background-color: black; overflow: hidden" class="image_class">
    <el-backtop></el-backtop>
    <div v-cloak
         ref="opacity_img"
         class="image_class"
         :style="{ backgroundImage: 'url(' + url + ')', backgroundColor: 'black' }">
      <el-container class="index_container">

        <el-header>
          <el-menu
              class="el-menu-demo"
              mode="horizontal"
              background-color="#545c64"
              text-color="#fff"
              active-text-color="#ffd04b">
            <el-menu-item index="1">
              <router-link to="/agent">
                <el-button type="primary" class="wise_button"
                >Agent
                </el-button>
              </router-link>
            </el-menu-item>
            <el-menu-item index="2">
              <el-dropdown v-if="token">
                <el-button type="primary" class="wise_button">
                  User
                  <i class="el-icon-arrow-down el-icon--right"/>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <!-- <el-dropdown-item @click.native="admin_manage"
                    >Manage</el-dropdown-item> -->
                  <router-link to="/index/user_agent/list">
                    <el-dropdown-item>My Agents</el-dropdown-item>
                  </router-link>
                  <el-dropdown-item @click.native="user_logout"
                  >Logout
                  </el-dropdown-item
                  >
                </el-dropdown-menu>
              </el-dropdown>

              <el-button
                  v-if="!token"
                  type="primary"
                  class="wise_button"
                  @click="submitForm()"
              >Login
              </el-button
              >
            </el-menu-item>
            <el-menu-item index="3">
              <router-link to="/wise">
                <el-avatar
                    shape="square"
                    size="large"
                    alt="index"
                    fit="contain"
                    :src="squareUrl"></el-avatar>
              </router-link>
            </el-menu-item>
          </el-menu>
          <el-dialog
              class="login_dialog"
              title="Login Form"
              :visible.sync="loginVisible"
              center
              :append-to-body="true"
              :lock-scroll="false"
          >
            <login-name/>
          </el-dialog>
        </el-header>
        <el-main class="index_main" style="padding:5px">
          <div style="text-align:center;">
            <el-row type="flex" justify="center" class="main_text">
              <div v-if="!token" class="w_text">WiseAI</div>
              <div v-if="token" class="w_text">
                Welcome!
                <div style="text-align: center">
                  {{ $store.getters.username }}
                </div>
              </div>

            </el-row>
            <br>
            <br>
            <div v-if="!token"
                 style="font-size: 30px;color: #cdcde7;
text-shadow: 0 0 10px #000000, 0 0 20px #e0cece, 0 0 30px #c6a8a8, 0 0 40px #1f1f1f;
">
              <!--      为了网站备案... -->
              <h5>"介绍：这是个人开发的Agent框架， 目前还在开发中，之后我的开发记录以及个人博客都会放到这个地方..."</h5>
            </div>
          </div>
        </el-main>
        <el-footer style="height: auto">
          <div class="footer_bar">
            <img
                style="width: 20px; height: 20px"
                src="http://www.beian.gov.cn/img/ghs.png"
                alt="备案标识"
            />
            <a href="http://beian.miit.gov.cn"
               target="_blank"
               rel="nofollow noopener noreferrer">粤ICP备18021686号-1</a>
          </div>
        </el-footer>
      </el-container>

    </div>
  </div>

</template>

<script>
import {getToken} from "@/utils/auth";
import LoginName from "@/views/login";

var url_path = require("../../public/login_before.jpg");
var url_path_after = require("../../public/login_after.png");
var squareUrl = require("../../public/wise_logo.png");

export default {
  name: "Index",
  components: {"login-name": LoginName},
  data: () => {
    return {
      url: url_path,
      token: "",
      loginVisible: false,
      squareUrl: squareUrl
    };
  },
  created() {
    this.token = getToken();
    if (this.token) {
      this.url = url_path_after;
    }
  },
  mounted() {
    this.$refs.opacity_img.style.transform = "scale(0.95, 0.95)";
    setTimeout(() => {
      this.$refs.opacity_img.style.transform = "scale(1, 1)";
      this.$refs.opacity_img.style.transition = "all 1s ease";
    }, 0);
  },
  methods: {
    user_logout() {
      this.$store.dispatch("user/logout");
      this.$message({
        message: "Logout Success",
        type: "success",
      });
      setTimeout(function () {
        window.location.reload();
      }, 1000);
    },
    admin_manage() {
      this.$router.push("/manage");
    },
    submitForm() {
      this.loginVisible = true; // 默认页面不显示为false,点击按钮将这个属性变成true
    },
  },
};
</script>

<style lang="scss" scoped>
[v-cloak] {
  display: none !important;
}

.index_main {
  position: relative;

  .login_dialog {
    font-size: 26px;
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
}

.el-header {
  text-align: right;
  padding: 0;
  background-color: transparent;
}

.el-header .el-menu.el-menu--horizontal {
  border-bottom: none;
}

.el-header .el-menu {
  display: flex;
  justify-content: flex-end;
  background-color: transparent;
}

.footer_bar {
  color: white;
  text-align: center;
  font-size: 1px;
  height: auto;
}

.el-footer {
  height: auto;
}


</style>
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