<template>
  <div style="padding:20px">
    <el-page-header @back="goBack"></el-page-header>
    <el-divider></el-divider>
    <div id="agent_info">
      <el-row style="text-align: center"><span style="font-size: 10px; ">
        </span>
        <el-button type="primary" size="large">
          <span style="font-size: 30px; ">
          {{ agent.name }}</span>
        </el-button>
      </el-row>
      <!-- name update modify -->
      <el-divider><strong>Deploy</strong></el-divider>
      <el-row>
        <strong>Anaconda:</strong>
        <vue-markdown :source="conda_source"> > </vue-markdown>
        <br>
        <strong>Python:</strong>
        <vue-markdown :source="python_source"> > </vue-markdown>
      </el-row>
      <el-divider></el-divider>
      <!-- tags -->
      <el-row>
        <el-tag v-if="agent.in_docker" size="mini" effect="dark" closable>docker</el-tag>
        <el-tag v-if="!agent.in_docker" size="mini" effect="dark" type="info" closable>docker</el-tag>
      </el-row>
      <el-divider><strong>More Detail</strong></el-divider>
      <!-- Category -->
      <el-row>
        <el-divider content-position="left">Category</el-divider>
        <el-button type="primary" size="mini">{{ agent.agent_category.name }}</el-button>
      </el-row>
      <!-- Behaviours: -->
      <el-row>
        <el-divider content-position="left">Behaviours</el-divider>
        <el-col
            v-for="item in agent.behaviours"
            :key="item.id"
            :span="2"
            class="grid-content bg-purple">
          <el-button type="primary" size="small">{{ item.name }}</el-button>
        </el-col>
      </el-row>
      <!-- Basic Agent -->
      <el-row>
        <el-divider content-position="left">Basic Agent</el-divider>
        <el-button type="primary" size="small">{{ agent.basic_agent.name }}</el-button>
      </el-row>

    </div>
  </div>
</template>

<style>
#agent_info .el-button:hover {
  border-radius: 50px;
  transition-duration: 0.1s;
  transition-property: all;
  background-color: #2c3e50;
  color: #d7ebff;
  font-size: 1.1em;
  border-color: #2c3e50;
  border-width: 0.1em;
}

#agent_info {
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0px 0px 10px #000;
}

</style>

<script>
import VueMarkdown from 'vue-markdown'

export default {
  name: "NullAgent",
  components: {
    VueMarkdown
  },
  data() {
    return {
      agent: {
        "id": 0,
        "avatar": "",
        "belong_to": {
          "id": 0,
          "name": ""
        },
        "credit": "",
        "behaviours": [
          {
            "id": 0,
            "name": ""
          }
        ],
        "agent_category": {
          "id": 0,
          "name": ""
        },
        "agent_configs": {},
        "behaviour_configs": {},
        "basic_agent": 0,
        "created_at": "",
        "modified_at": "",
        "name": "",
        "is_office": true,
        "in_docker": false,
      },
      conda_source: new Date().toLocaleTimeString(),
      python_source: new Date().toLocaleTimeString(),
      anchorAttrs: {
        target: '_blank',
        rel: 'noopener noreferrer nofollow'
      }
    };
  },
  created() {
    var agent_id = this.$route.params.agent_id;
    this.$store.dispatch("agent/get_user_agent_info", {agent_id: agent_id}).then((data) => {
      this.agent = data;
      this.conda_source = " > ```conda create -f environment.yml && " +
          "python load_agent.py --agent_id "+ data.id +" --credit "+ data.credit +" ```"
      this.python_source = " > ```python load_agent.py --agent_id " + data.id +" --credit " + data.credit +"```"
    })
        .catch(() => {
          this.loading = false;
        });
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>

h3 {
  margin-top: 32px;
  margin-bottom: 16px;
}
</style>