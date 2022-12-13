<template>
  <h1>Dashboard</h1>
  <h2>{{dashboardName}}</h2>
  <table>
    <tr>
      <th v-for="(item, index) in collectionParams" :key="index">{{ item }}</th>
    </tr>
    <tr v-for="(rowItem, rowIndex) in data" :key="rowIndex">
      <td v-for="(headerItem, columnIndex) in collectionParams" :key="columnIndex">
        {{ data[rowIndex][headerItem] }}
      </td>
    </tr>
  </table>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "TableViewComponent",
  props: {
    dashboardId: String
  },
  data() {
    return {
      data: [],
      config: {}
    };
  },
  computed: {
      collectionParams() {
          if (this.data.length > 0) {
              console.log(this.data)
              console.log(Object.keys(this.data.at(0)))
              return Object.keys(this.data.at(0))
          }
          return this.config['params']
      },
      dashboardName() {
          return this.config['name']
      }
  },
  watch: {
    dashboardId() {
      this.update();
    },
  },
  methods: {
    update() {
      axios
        .get("http://127.0.0.1:8000/v1/dashboard/" + this.dashboardId)
        .then((response) => (this.data = response["data"]["result"], console.log(response)));
      axios
        .get("http://127.0.0.1:8000/v1/configuration/dashboards/" + this.dashboardId)
        .then((response) => (this.config = response["data"]["result"][0], console.log(response)));
    }
  },
  mounted() {
    this.update();
  },
};
</script>

<style>
table,
th,
td {
  border: 1px solid black;
}
</style>
