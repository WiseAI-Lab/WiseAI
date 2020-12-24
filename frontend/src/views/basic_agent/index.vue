<template>
  <div>
    <full-page-loader v-if="loading" />
      <el-container>
      <br>
      <el-header style="background-color: transparent;text-align: center;">
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
import FullPageLoader from '@/components/FullPageLoader';

export default {
  name: 'browse',
  components: { FullPageLoader },
  data() {
    return {
      loading: true,
    };
  },
  methods: {
    fetchTopCharts() {
      setTimeout( function () {
              this.loading = false
      }, 2)
    },
  },
  created() {
    this.fetchTopCharts();
  },
};
</script>
