<template>
  <h1>Table</h1>
  <v-table>
    <thead>
      <tr>
        <th>Index</th>
        <th v-for="(item, index) in collectionParams" :key="index">
          {{ item["name"] }}
        </th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(rowItem, rowIndex) in data" :key="rowIndex">
        <td>
          {{ rowIndex }}
        </td>
        <td
          v-for="(headerItem, columnIndex) in collectionParams"
          :key="columnIndex"
        >
          {{ rowItem[headerItem["name"]] }}
        </td>
        <td>
          <v-btn @click="deleteObject(rowItem['_id'])">
            Delete
          </v-btn>
          <v-btn
            v-for="(item, buttonIndex) in actions"
            :key="buttonIndex"
            @click="executeActionForObject(rowItem['_id'], item['_id'])"
          >
            {{ item["name"] }}
          </v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
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
    };
  },
  watch: {
    pageInfo() {
      if ("_id" in this.pageInfo) {
        axios
          .get(
            "http://127.0.0.1:8000/v1/configuration/actions?collection_id=" + this.pageInfo["_id"]
          )
          .then((response) => (this.actions = response["data"]["result"]));
      }
    },
    collectionName() {
      this.update();
    },
  },
  methods: {
    update() {
      axios
        .get("http://127.0.0.1:8000/v1/data/" + this.collectionName)
        .then((response) => (this.data = response["data"]["result"]));
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
    deleteObject(id) {
      axios
        .delete("http://127.0.0.1:8000/v1/data/" + this.collectionName + "?_id="+id)
        .then((response) => (console.log('success delete:' + response)));
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
