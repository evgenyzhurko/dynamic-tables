<template>
  <h1>Table</h1>
  <v-table>
    <thead>
      <tr>
        <th v-for="(item, index) in collectionParams" :key="index">
          {{ item["name"] }}
        </th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(rowItem, rowIndex) in data" :key="rowIndex">
        <td v-for="(headerItem, columnIndex) in collectionParams" :key="columnIndex">
          <v-container
            v-if="
              headerItem['type'] == 'Date' ||
              headerItem['type'] == 'Time' ||
              headerItem['type'] == 'Datetime'
            "
          >
            {{ Date(rowItem[headerItem["name"]]).toLocaleString() }}
          </v-container>
          <v-container v-else-if="headerItem['type'] == 'Multiselect'">
            <v-chip v-for="(option, index) in rowItem[headerItem['name']]" :key="index">
              {{ option }}
            </v-chip>
          </v-container>
          <v-container v-else>
            {{ rowItem[headerItem["name"]] }}
          </v-container>
        </td>
        <td>
          <v-menu open-on-hover>
            <template v-slot:activator="{ props }">
              <v-icon v-bind="props" size="x-large"
                >mdi-dots-vertical-circle-outline</v-icon
              ></template
            >
            <v-list>
              <v-list-item @click="deleteObject(rowItem['_id'])">
                <v-list-item-title>Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </td>
        <!-- <td>
          <v-btn @click="deleteObject(rowItem['_id'])"> Delete </v-btn>
          <v-btn
            v-for="(item, buttonIndex) in actions"
            :key="buttonIndex"
            @click="executeActionForObject(rowItem['_id'], item['_id'])"
          >
            {{ item["name"] }}
          </v-btn>
        </td> -->
      </tr>
    </tbody>
  </v-table>
  <v-pagination v-model="page" :length="pageCount"></v-pagination>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "TableViewComponent",
  props: {
    pageInfo: Object,
    collectionName: String,
    collectionParams: Array,
  },
  data() {
    return {
      data: [],
      actions: [],
      page: 0,
      limit: 10,
      count: 0,
    };
  },
  computed: {
    pageCount() {
      return this.count / this.limit;
    },
  },
  watch: {
    pageInfo() {
      if ("_id" in this.pageInfo) {
        axios
          .get(
            "http://127.0.0.1:8000/v1/configuration/actions?collection_id=" +
              this.pageInfo["_id"]
          )
          .then((response) => (this.actions = response["data"]["result"]));
      }
    },
    collectionName() {
      this.update();
    },
    page() {
      this.update();
    },
  },
  methods: {
    update() {
      axios
        .get(
          `http://127.0.0.1:8000/v1/data/${this.collectionName}?skip=${
            this.page * this.limit
          }&limit=${this.limit}`
        )
        .then((response) => (this.data = response["data"]["result"]));
      axios
        .get(`http://127.0.0.1:8000/v1/data/${this.collectionName}/count`)
        .then((response) => (this.count = response["data"]["result"]));
    },
    executeActionForObject(objectId, actionId) {
      console.log(objectId, actionId);
      axios
        .post(
          "http://127.0.0.1:8000/v1/data/" +
            this.collectionName +
            "/" +
            objectId +
            "/" +
            actionId,
          {}
        )
        .then((response) => console.log(response), this.update());
    },
    async deleteObject(id) {
      await axios
        .delete("http://127.0.0.1:8000/v1/data/" + this.collectionName + "?_id=" + id);
        this.update()
    },
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
