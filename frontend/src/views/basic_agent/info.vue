<template>
  <div style="padding:20px">
    <el-page-header @back="goBack"></el-page-header>
    <el-divider></el-divider>
    <div id="basic_agent_info">
    
    <!-- avator -->
    <el-badge :value="'ID:' + agent.id" class="item" type="success"> </el-badge>
    <!-- name update modify -->
    <el-row>
      <el-col :span="6">
        <el-image
          :src="agent.avatar"
          fit="fill"/>
      </el-col>
      <el-col :span="15">
        <el-row>
          <span style="font-size: 30px">{{ agent.name }}</span>
        </el-row>
        <el-row>
          By:
          <span style="font-size: 20px; color: blue">{{agent.author.name
          }}</span>
        </el-row>
        <el-row>
          Create at: <span>{{ agent.created_at }}</span> 
        </el-row>
        <el-row>
          Last Updated:<span>{{ agent.modified_at }}</span>
        </el-row>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <!-- tags -->
    <el-row>
      <el-tag v-if="agent.is_office" size="mini" effect="dark" closable >office</el-tag>
      <el-tag v-if="!agent.is_office" size="mini" effect="dark" closable >user</el-tag>
      <el-tag v-if="agent.is_docker" size="mini" effect="dark" closable>docker</el-tag>
    </el-row>
    <el-divider>More Detail</el-divider>
    <!-- Description -->
    <el-divider content-position="left">Description</el-divider>
    <el-row> {{ agent.description }} </el-row>

    <!-- Category -->
    <el-row>
      <el-divider content-position="left">Category</el-divider>
      <el-button type="primary" size="mini" >{{ agent.agent_category.name }}</el-button>
    </el-row>
    <!-- Prerequisite behaviour categories: -->
    <el-row>
      <el-divider content-position="left">Prerequisite behaviour categories</el-divider>
      <el-col
        v-for="item in agent.prerequisite_behaviour_categories"
        :key="item.id"
        :span="2"
        class="grid-content bg-purple">
        <el-button type="primary" size="small">{{ item.name }}</el-button>
      </el-col>
    </el-row>
    <!-- Default behaviours -->
    <el-row>
      <el-divider content-position="left">Default Behaviours</el-divider>
      <el-col
        v-for="item in agent.default_behaviours"
        :key="item.id"
        :span="3"
        class="grid-content bg-purple">
        <el-button type="primary" size="mini">{{ item.name }}</el-button>
      </el-col>
    </el-row>
    <!-- Parent Agent -->
    <el-row>
      <el-divider content-position="left">Inherit Tree</el-divider>
          <div class="container">
          <div style="display: flex;">
            <el-button @click="controlScale('bigger')">+</el-button>
            <el-button @click="controlScale('smaller')">-</el-button>
            <el-button @click="controlScale('restore')">1:1</el-button>
          </div>
          <vue-tree
            ref="scaleTree"
            style="width: 500px; height: 300px;"
            :dataset="agent.parent_agent"
            :config="treeConfig"
            direction="horizontal">
            <template v-slot:node="{ node, collapsed }">
              <el-button
                type="primary"
                size="mini"
                class="rich-media-node"
                :style="{ border: collapsed ? '2px solid grey' : '' }">
                <span style="font-weight: bold;">{{ node.name }}</span>
              </el-button>
            </template>
          </vue-tree>
        </div>
    </el-row>

    </div>
    <!-- Initial a Agent base this. -->
    <el-divider></el-divider>
    <el-row style="text-align:center;">
      <router-link :to="{name:'init_agent', params: { basic_agent_id: agent.id }}">
        <el-button 
        class="initial_button"
        type="primary" 
        size="large">Init an Agent</el-button>
      </router-link>
    </el-row>
  </div>
</template>

<style>
#basic_agent_info .el-button:hover {
  border-radius: 50px;
  transition-duration: 0.1s;
  transition-property: all;
  background-color: #2c3e50;
  color: #d7ebff;
  font-size: 1.1em;
  border-color: #2c3e50;
  border-width: 0.1em;
}
#basic_agent_info {
  border-radius:10px;
  padding: 10px;
  box-shadow:0px 0px 10px #000;
}

</style>

<script>
import VueTree from './VueTree.vue'

export default {
  name: "NullAgent",
  components: { 'vue-tree': VueTree },
  data() {
    return {
      agent: {
        "id": 0,
        "avatar": "",
        "author": {
            "id": 0,
            "name": ""
        },
        "prerequisite_behaviour_categories": [
            {
                "id": 0,
                "name": ""
            }
        ],
        "default_behaviours": [
            {
                "id": 0,
                "name": ""
            }
        ],
        "agent_category": {
            "id": 0,
            "name": ""
        },
        "configs": {
        },
        "parent_agent": {},
        "created_at": "",
        "modified_at": "",
        "name": "",
        "url": "",
        "description": "",
        "is_office": true,
        "in_docker": false,
        "extra_support_version": [],
        "version": null
      },
      richMediaData: {},
      treeConfig: { nodeWidth: 70, nodeHeight: 40, levelHeight: 100 }
    };
  },
  created() {
    var agent_id = this.$route.params.agent_id;
    this.$store.dispatch("agent/get_basic_agent_info", { agent_id: agent_id }).then((data) => {
        this.richMediaData = JSON.parse(JSON.stringify(data["parent_agent"]));
        this.agent = data;
      })
      .catch(() => {
        this.loading = false;
      });
  },
  methods: {
      goBack() {
        this.$router.go(-1);
      },
      controlScale(command) {
      switch (command) {
        case 'bigger':
          this.$refs.scaleTree.zoomIn()
          break
        case 'smaller':
          this.$refs.scaleTree.zoomOut()
          break
        case 'restore':
          this.$refs.scaleTree.restoreScale()
          break
      }
    }
    },
};
</script>

<style lang="scss" scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .rich-media-node {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
  }
  h3 {
    margin-top: 32px;
    margin-bottom: 16px;
  }
  .initial_button {
    border-radius: 100px;
    transition-duration: 0.1s;
    transition-property: all;
    background-color: #2c3e50;
    color: #69adf1;
    font-size: 1.5em;
    border-color: #2c3e50;
    border-width: 0.3em;
  }
  .initial_button:hover {
    background-color: #328be4;
    border-color: #328be4;
    color: #ffffff;
}
</style>