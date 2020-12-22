<template>
    <div>
        <el-container>
            <el-header style="text-align:center;">
                    <h3>Describe your Agent</h3>
            </el-header>
            <el-main style="padding:15px;">
            <el-form ref="form" :model="form" label-width="100px">
                <el-form-item label="Agent Name">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="Base Agent">
                    <el-select v-model="form.base_agent" :placeholder="basic_agent_id == 0 ? 'select': basic_agent_id">
                    <el-option 
                    v-for="item in base_agent_list"
                    :key="item.id"
                    :label=item.name 
                    :value=item.id>
                    </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="Description">
                    <el-input type="textarea" v-model="form.desc"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">Create</el-button>
                    <el-button @click="goBack">Cancel</el-button>
                </el-form-item>
                </el-form>
            </el-main>
        </el-container>
    </div>
</template>
<script>
  export default {
    name:"InitAgent",
    data() {
      return {
        form: {
          name: '',
          base_agent: '',
          
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        // first
        base_agent_list: [
            {
                "id": "id1",
                "name": "name1"
            },
            {
                "id": "id2",
                "name": "name2"
            },
        ],
        behaviours: [
//type1            
            [
                {
                    "id": "",
                    "name": ""
                },
                {
                    "id": "",
                    "name": ""
                },
                
            ],
            //type2
            [
                {
                    "id": "",
                    "name": ""
                },
                {
                    "id": "",
                    "name": ""
                },
                
            ],
            
        ],
        basic_agent_id: 0
      }
    },
    methods: {
      onSubmit() {
        console.log('submit!');
      },
      goBack() {
        this.$router.go(-1);
      },
    },
    created() {
    var basic_agent_id = this.$route.params.basic_agent_id;
    // this.$store.dispatch("agent/get_basic_agent_info", { basic_agent_id: basic_agent_id }).then((data) => {
    //     this.richMediaData = JSON.parse(JSON.stringify(data["parent_agent"]));
    //     this.agent = data;
    //   })
    //   .catch(() => {
    //     this.loading = false;
    //   });
  },

  }
</script>