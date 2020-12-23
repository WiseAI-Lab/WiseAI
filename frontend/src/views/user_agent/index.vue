<template>
  <div>
    <el-container style="height: 100%; border-radius: 10px;background-color: rgb(255, 255, 255)">
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "UserAgentIndex",
};
</script>
