<template>
  <div class="home">
    <sidebar/>
    <div class="main-view ">
      <full-page-loader v-if="loading" />
      <div class="scrollWrapper">
        <router-view id="main-body"/>
      </div>
    </div>
  </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import FullPageLoader from '@/components/FullPageLoader';

export default {
  name: "agent",
  components: {Sidebar, FullPageLoader},
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
}
</script>

<style scoped>

</style>