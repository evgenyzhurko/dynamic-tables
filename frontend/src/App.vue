<template>
  <v-layout>
    <v-app-bar color="grey-lighten-2">
      <p>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn color="primary" v-bind="props"> Menu </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <router-link to="/">Home</router-link>
            </v-list-item>
            <v-list-item v-for="(item, index) in availablePages" :key="index">
              <router-link v-bind:to="'/pages/' + item">{{ item }}</router-link>
              <!-- <v-list-item-title>{{ item.title }}</v-list-item-title> -->
            </v-list-item>
          </v-list>
        </v-menu>

        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn color="primary" v-bind="props"> Configuration </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <router-link to="/configuration">Setup</router-link>
            </v-list-item>
            <v-list-item>
              <router-link to="/configuration/collections">Collections</router-link>
            </v-list-item>
            <!-- <v-list-item>
                <router-link to="/configuration/actions">Actions</router-link>
            </v-list-item>
            <v-list-item>
                <router-link to="/configuration/dashboards">Dashboards</router-link>
            </v-list-item> -->
          </v-list>
        </v-menu>

        <!-- <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn color="primary" v-bind="props"> Dashboards </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in availableDashboards" :key="index">
              <router-link v-bind:to="'/pages/' + item['id']">{{
                item["name"]
              }}</router-link>
            </v-list-item>
          </v-list>
        </v-menu> -->
      </p>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-layout>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "App",
  data() {
    return {
      pages: null,
      dashboards: null,
    };
  },
  computed: {
    availablePages() {
      if (this.pages === null) {
        return [];
      }
      var pages = [];
      for (const index in this.pages) {
        pages.push(this.pages[index]["name"]);
      }
      return pages;
    },
    availableDashboards() {
      if (this.dashboards === null) {
        return [];
      }
      var dashboards = [];
      for (const index in this.dashboards) {
        dashboards.push({
          name: this.dashboards[index]["name"],
          id: this.dashboards[index]["_id"],
        });
      }
      return dashboards;
    },
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/v1/configuration/collections")
      .then((response) => (this.pages = response["data"]["result"]));
    axios
      .get("http://127.0.0.1:8000/v1/configuration/dashboards")
      .then((response) => (this.dashboards = response["data"]["result"]));
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
