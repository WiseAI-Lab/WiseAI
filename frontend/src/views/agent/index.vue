<template>
  <div>
    <el-container>
      <el-divider></el-divider>
      <el-header style="background-color: transparent;text-align: center;">

        <!-- <router-link to="/index/agent/my_agent"> -->
        <router-link to="/my_agents">
          <el-button v-if="token" type="success">My Agents</el-button>
        </router-link>
        <!-- </router-link> -->
        <el-divider v-if="token" direction="vertical"></el-divider>
        <router-link to="/index/agent/basic_agent_list">
            <el-button type="primary" size="small">Agents</el-button>
        </router-link>
        <el-divider direction="vertical"></el-divider>
        <el-button type="primary" size="small">Behaviours</el-button>
      </el-header>
      <el-main id="main_agent_list">
        <el-container style="height: 100%; border-radius: 10px;background-color: rgb(255, 255, 255)">
          <!-- <el-divider>Wise Agent</el-divider> -->
          <el-main>
            <router-view />
          </el-main>
        </el-container>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getToken } from "@/utils/auth";
export default {
  name: "AgentIndex",
  data: () => {
    return {
        token: "",
    }
  },
  created() {
    this.token = getToken();
  },
};
</script>

<style lang="scss" scoped>
.el-header {
  text-align: right;
  padding: 0;
  background-color: transparent;
}

</style>