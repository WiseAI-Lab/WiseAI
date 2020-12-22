<template>
  <div class="app-container"  style="text-align:center;">
    <el-divider content-position="center">Agents</el-divider>
    <el-container>
      <el-header style="text-align: center; font-size: 12px" >
            <el-button type="primary" size="mini">Upload an Agent</el-button>
            <el-divider direction="vertical"></el-divider>
            <router-link to="init_agent">
            <el-button type="primary" size="mini">Launch Your Agent</el-button>
            </router-link>
      </el-header>
      <el-main>
          <el-container>
    <el-header>
      <el-input v-model="filterText" placeholder="Filter keyword" style="margin-bottom:10px;" />
    </el-header>
    <el-main>
      <el-col v-for="item in filter_node_list"
      :key="item.id"
      :xs="22"
      :sm="10"
      :md="8"
      :lg="7"
      :xl="5"
      :span="8"
      :offset="0"
      class="node_col grid-content bg-purple"
    > 
      <router-link :to="{ name: 'basic_agent_info', params: { agent_id: item.id }}">
      <el-card  class="node_card"  shadow="hover" >
        <el-badge :value="'ID:' + item.id" class="item" type="success">
          <el-row type="flex" justify="center">
            <el-col :xs="20" :sm="10" :md="4" :lg="3" :xl="1" style="width: 80%; height: 80%">
              <el-image
                style="width: 100%; height: 100%;text-align:center;"
                :src="item.avatar"
                fit="fill"
              />
            </el-col>
            <el-col :offset="2">
              <el-row>
                <span style="font-size: large; text-align:center;">
                  <el-button 
                  class="name_button"
                  size="small" type="primary" plain><strong>{{ item.name }}</strong></el-button>
                </span>
              </el-row>
              <el-divider></el-divider>
                  <el-tag v-if="item.is_office" size="mini" effect="dark" closable>office</el-tag>
                  <el-tag v-if="!item.is_office" size="mini" effect="dark" closable>user</el-tag>

                  <el-tag v-if="!item.in_docker" size="mini" effect="dark" closable>docker</el-tag>
                  
                  <el-tag v-if="item.status" size="mini" effect="dark" closable>Active</el-tag>
                  <el-tag v-if="!item.status" size="mini" type="info" effect="dark" closable>Rest</el-tag>
            </el-col>
          </el-row>

        </el-badge>
      </el-card>
      </router-link>
    </el-col>
    </el-main>
    <el-footer>
    <el-pagination
      background
      layout="prev, pager, next"
      :total=total>
  </el-pagination>
    </el-footer>
          </el-container>
      </el-main>
    </el-container>
  </div>
</template>
<style lang="scss" scoped>
  .el-col {
    margin-bottom: 5px;
    border-radius: 4px;

    &:last-child {
      margin-bottom: 3px;
    }
  }

  body {
    background: #f3f1f5;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
</style>
<script>
export default {
  name: 'BasicAgentList',
  data() {
    return {
      filterText: '',
      node_list: {},
      currentDate: new Date(),
      filter_node_list: [],
      next: 0,
      previous: 0,
      total: 0
    }
  },
  watch: {
    filterText(val) {
      this.filter_node_list = []
      this.node_list.forEach(node => {
        var agent_id = node.id.toString()
        var agent_name = node.name.toString()
        if (agent_id.search(val) !== -1) {
          this.filter_node_list.push(node)
        } else if (agent_name.search(val) !== -1) {
          this.filter_node_list.push(node)
        }
      })
    }
  },
  created() {
    this.$store.dispatch('agent/get_basic_agent_list').then((data) => {
      this.next = data['next']
      this.previous = data['previous']
      this.total = data['count']
      this.node_list = data['results']
      this.filter_node_list = data['results']
    }).catch(() => {
      this.loading = false
    })
  },
  methods: {
    handleView(el, cardId) {
      console.log(cardId)
      this.item.open = !this.item.open;
      let viewportOffset = el.target.getBoundingClientRect();

      if(this.item.open) {
        document.body.style.top = '-' + window.scrollY + 'px';
        document.body.style.position = 'fixed';

        this.styleObject.transform = 
          'translate('+ viewportOffset.left * -1 +'px, '+ viewportOffset.top * -1 +'px)';

        if(cardId !== this.id)
          this.$router.push({ name: 'card', params: {id: cardId}});
      }
      else {
        this.styleObject = {
          transform: 'translate(0px,0px)'
        };

        let scrollY = document.body.style.top;
        document.body.style.position = '';
        document.body.style.top = '';
        window.scrollTo(0, parseInt(scrollY) * -1);

        this.$router.push({ name: 'cardlist'});
      }
    },
  },

}
</script>

<style lang="scss" scoped>
.name_button {
  border-radius: 100px;
  background-color: #3b3594;
  color: #ffffff;
  font-size: 1.5em;
  border-width: 0.3em;
  border-color:#3b3594;
}

</style>