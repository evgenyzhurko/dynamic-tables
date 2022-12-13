<template>
  <h1>System Configuration</h1>
  <v-btn @click="initializeSystemConfiguration">Reset Configuration</v-btn>
</template>

<script>
const axios = require("axios").default;

export default {
  methods: {
    initializeSystemConfiguration() {
      axios
        .post("http://127.0.0.1:8000/v1/configuration/initialize", {})
        .then((response) => console.log(response));
    },
  },
};
</script>
