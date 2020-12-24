<template>
  <div class="sidebar">
    <nav class="scrollWrapper">
      <div class="padding-div" v-for="(category, index) in categories" :key="index">
        <h2 class="sidebar__category svg-container">
          <font-awesome-icon
              class="icon"
              v-if="category.icon === 'music'"
              icon="apple-alt"
              size="1x"
          />
          <font-awesome-icon class="icon" v-else icon="headphones" size="1x"/>
          {{ category.category }}
        </h2>
        <ul class="sidebar__ul">
          <li
              v-for="(label, index) in category.labels"
              :key="index"
              class="sidebar__li"
              :class="{
              sidebar__li__isActive: isActive(label.routeName),
            }"
          >
            <router-link :to="label.routeName">
              <div>{{ label.name }}</div>
            </router-link>
            <!--            <div @click="routeTo(label.routeName)">{{ label.name }}</div>-->
          </li>
        </ul>
      </div>

      <div class="padding-div">
        <h2 class="sidebar__category svg-container">
          <font-awesome-icon class="icon" icon="cat" size="1x"/>
          Develop
        </h2>
        <ul class="sidebar__ul">
          <router-link v-if="token" to="/agent/user">
            <li class="sidebar__li link develop_button">My Agents </li>
          </router-link>
          <router-link to="/agent/basic/initial">
            <li class="sidebar__li link develop_button">Launch Agent </li>
          </router-link>
          <router-link to="/index">
            <li class="sidebar__li link develop_button">Index </li>
          </router-link>
        </ul>
      </div>
    </nav>

    <div class="player">
      <el-card v-if="token" style="margin: 5px">
        <div class="block">
          <el-avatar size="large" :src="avatar">{{ this.username }}</el-avatar>
        </div>
      </el-card>

      <router-link v-if="!token" to="/wise">
        <el-avatar
            shape="square"
            size="large"
            alt="index"
            fit="contain"
            :src="index_image_url"></el-avatar>
      </router-link>
    </div>
  </div>
</template>

<script>
import routerConstants from '../router/routerConstants';
import {getToken} from "@/utils/auth";

var wise_logo_url = require("@/../public/wise_logo.png");

export default {
  name: 'sidebar',
  data() {
    return {
      categories: routerConstants,
      token: "",
      username: this.$store.getters.username,
      avatar: this.$store.getters.avatar,
      index_image_url: wise_logo_url

    };
  },
  created() {
    this.token = getToken();
  },
  methods: {
    routeTo(name) {
      console.log(name)
      if (this.$route.name === name) return;
      this.$router.push({name});
    },
    isActive(name) {
      return this.$route.name === name;
    },
  },
};
</script>
