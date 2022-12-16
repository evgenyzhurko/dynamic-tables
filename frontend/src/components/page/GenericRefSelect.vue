<template>
  <div>
    <v-select 
        v-model="selected" 
        :items="data" 
        :label="collectionName"
        :item-title="(item) => { return item[param_name] }"
        return-object>
    </v-select>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "GenericRefSelect",
  props: {
    collectionName: String,
  },
  data() {
    return {
      data: [],
      param_name: "",
      selected: "",
    };
  },
  watch: {
    selected() {
      this.$emit("item-selected", this.selected);
    },
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/v1/data/" + this.collectionName)
      .then((response) => (this.data = response["data"]["result"]));
    axios
      .get(
        "http://127.0.0.1:8000/v1/configuration/collections?name=" +
          this.collectionName
      )
      .then(
        (response) => (
          (this.param_name = response["data"]["result"][0]["base_param"]),
          console.log(this.param_name)
        )
      );
  },
};
</script>
