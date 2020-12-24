<template>
  <div>
    <full-page-loader v-if="loading" />
    <el-container style="height: 100%; border-radius: 10px;background-color: rgb(255, 255, 255)">
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import FullPageLoader from '@/components/FullPageLoader';

export default {
  name: "UserAgentIndex",
  components: { FullPageLoader },
  data() {
    return {
      loading: true,
    };
  },
  methods: {
    fetchTopCharts() {
      // fake load time
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
