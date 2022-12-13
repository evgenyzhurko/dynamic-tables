<template>
  <h1>Create new dashboard</h1>
  <div>
    <label for="collection-name"></label>
    <v-text-field
      label="Dashboard Name"
      :rules="[rules.required, rules.text]"
      v-model="name"
      required
    />
  </div>
  <div>
    <v-select
        label="Collection"
        :items="data"
        v-model="selected"
        item-title="name"
        return-object/>
  </div>
  <div>
    <v-textarea label="Pipeline Code" v-model="pipeline"></v-textarea>
  </div>
  <button @click="createDashboard">Create dashboard</button>
</template>

<script>
const axios = require("axios").default;

export default {
  data() {
    return {
      name: "",
      data: [],
      selected: "",
      pipeline: "",
      rules: {
        required: (value) => !!value || "Required",
        text: (value) => {
          const pattern = /^[A-Za-z0-9]+$/;
          return pattern.test(value) || "Invalid value";
        },
      }
    };
  },
  methods: {
    createDashboard() {
      axios
        .post("http://127.0.0.1:8000/v1/configuration/dashboards", {
            "name": this.name,
            "collection_name": this.selected,
            "pipeline": JSON.parse(this.pipeline)
        })
        .then((response) => console.log(response));
    },
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/v1/configuration/collections")
      .then((response) => (this.data = response["data"]["result"]));
  },
};
</script>
