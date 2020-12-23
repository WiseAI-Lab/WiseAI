<template>
  <div>
    <el-card :id="`card-${item.id}`" class="node_card"  shadow="hover" >
        <el-badge :value="'ID:' + item.id" class="item" type="success">
          <el-row type="flex" justify="center">
            <el-col :xs="20" :sm="10" :md="4" :lg="3" :xl="1" style="width: 80%; height: 80%">
              <el-image
                style="width: 100%; height: 100%; text-align:center;"
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
  </div>
</template>

<script>
export default {
  name: 'NodeCard',
  props: ["item"],
};
</script>

<style lang="scss" scoped>
.node_title {
  background: white;
  border-radius: 30px 10px 10px 10px;
  box-shadow: 2px 2px 7px 1px rgb(189, 189, 189);
  margin-top: 2em;
  text-align: center;
  display: inline-block;
  transition: .3s all;
}

.node_card {
  position: relative;
  left: 0;
  top: 0;
  background: white;
  border-radius: 10px;
  box-shadow: 2px 2px 7px 1px rgb(84, 87, 87);

  margin: 1em;
  transition-duration: .1s;
  transition-property: all;
  justify-content: space-between;
  padding: 0 1em;
  cursor: pointer;
}
  .name_button {
  border-radius: 100px;
  background-color: #3b3594;
  color: #ffffff;
  font-size: 1.5em;
  border-width: 0.3em;
  border-color:#3b3594;
}
</style>
