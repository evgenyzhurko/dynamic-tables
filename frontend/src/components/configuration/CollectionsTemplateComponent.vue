<template>
  <h1>Create new data collection template</h1>
  <div>
    <v-text-field
      label="Collection Name"
      :rules="[rules.required, rules.text]"
      v-model="name"
      required
    />
  </div>
  <div v-for="(item, index) in params" :key="index">
    <div>
      <v-text-field
        label="Param Name"
        :rules="[rules.required, rules.text]"
        v-model="item.name"
        required
      />
    </div>
    <div>
      <v-select
        label="Data type"
        :items="dtypes"
        v-model="item.type"
        required
      >
      </v-select>
    </div>
    <v-btn @click="removeCollectionParam(index)">Delete Param</v-btn><br />
  </div>
  <v-btn @click="addCollectionParam">+ param</v-btn><br />
  <v-btn @click="createDataCollectionTemplate">Create template</v-btn>
</template>

<script>
const axios = require("axios").default;

export default {
  data() {
    return {
      name: "",
      params: [],
      dtypes: ['String', 'Integer', 'Float', 'Bool', 'Datetime', 'Date', 'Time'],
      rules: {
        required: (value) => !!value || "Required",
        text: (value) => {
          const pattern = /^[A-Za-z0-9]+$/;
          return pattern.test(value) || "Invalid value";
        },
      }
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/v1/configuration/collections")
      .then((response) => (this.updateReferenceDtypes(response["data"]["result"])));
  },
  methods: {
    createDataCollectionTemplate() {
      axios
        .post("http://127.0.0.1:8000/v1/configuration/collections", {
          name: this.name,
          params: this.params,
        })
        .then((response) => console.log(response));
    },
    addCollectionParam() {
      this.params.push({
        name: "",
        type: "",
      });
    },
    removeCollectionParam(index) {
      this.params.splice(index, 1);
    },
    updateReferenceDtypes(data) {
        for(var index in data) {
            this.dtypes.push('Ref<'+data[index]['name']+'>')
        }
    }
  },
};
</script>
