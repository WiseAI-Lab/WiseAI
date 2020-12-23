<template>
  <div style="height: 100%; border-radius: 10px;background-color: rgb(255, 255, 255); margin:20px;">
    <el-container>
      <el-header style="text-align:center;">
        <h3>My Agents</h3>
      </el-header>
      <el-main style="padding:15px;text-align:center;">
        <el-container>
          <el-header>
            <el-input v-model="filterText" placeholder="Filter keyword" style="margin-bottom:10px;"/>
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
              <router-link :to="{ name: 'user_agent_info', params: { agent_id: item.id }}">
                <Card :key="item.id"
                      :item="item">
                </Card>
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

<script>
import Card from "@/components/card/Card"

export default {
  name: 'MyAgents',
  components: {Card},
  data() {
    return {
      filterText: '',
      node_list: {},
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
    this.$store.dispatch('agent/get_user_agent_list').then((data) => {
      this.next = data['next']
      this.previous = data['previous']
      this.total = data['count']
      this.node_list = data['results']
      this.filter_node_list = data['results']
    }).catch(() => {
      this.loading = false
    })
  },


}
</script>
<style lang="scss" scoped>
.el-col {
  margin-bottom: 5px;
  border-radius: 4px;

  &:last-child {
    margin-bottom: 3px;
  }
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>