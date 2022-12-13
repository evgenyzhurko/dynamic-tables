<template>
  <h1>Create new action</h1>
  <div>
    <v-text-field
      label="Action Name"
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
    <v-textarea label="Action Code" v-model="code"></v-textarea>
  </div>
  <button @click="createDataCollectionTemplate">Create action</button>
</template>

<script>
const axios = require("axios").default;

export default {
  data() {
    return {
      name: "",
      data: [],
      selected: "",
      code: "def handler(db, document):\n    //code here",
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
    createDataCollectionTemplate() {
      axios
        .post("http://127.0.0.1:8000/v1/configuration/actions", {
          name: this.name,
          collection_id: this.selected['_id'],
          code: this.code,
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
