<template>
  <v-container fluid>
    <div v-for="(item, index) in outputParams" :key="index">
      <v-text-field
        v-if="item['type'] == 'String'"
        :label="item['name']"
        :rules="[rules.required]"
        :placeholder="'Input for ' + item['name']"
        v-model="item['inputValue']"
      />
      <v-text-field
        v-else-if="item['type'] == 'Integer'"
        :label="item['name']"
        :rules="[rules.required, rules.integer_digits]"
        :placeholder="'Input for ' + item['name']"
        v-model.number="item['inputValue']"
        type="number"
      />
      <v-text-field
        v-else-if="item['type'] == 'Float'"
        :label="item['name']"
        :rules="[rules.required, rules.float_digits]"
        :placeholder="'Input for ' + item['name']"
        v-model.number="item['inputValue']"
        type="number"
      />
      <v-checkbox
        v-else-if="item['type'] == 'Bool'"
        :label="item['name']"
        input-value="true"
        v-model="item['inputValue']"
      ></v-checkbox>
      <GenericSelect
        v-else-if="item['type'].match('^Ref<[a-zA-Z0-9]*>')"
        :collectionName="item['type'].substr(4, item['type'].length - 5)"
        @item-selected="(v) => (item['inputValue'] = v['_id'])"
      />
      <DatepickerComponent
        v-else-if="item['type'] == 'Date'"
        v-model="item['inputValue']"
        :enable-time-picker="false"
      />
      <DatepickerComponent
        v-else-if="item['type'] == 'Time'"
        v-model="item['inputValue']"
        time-picker
      />
      <DatepickerComponent
        v-else-if="item['type'] == 'Datetime'"
        v-model="item['inputValue']"
      />
    </div>
  </v-container>
  <v-simple-checkbox label="Checkbox"></v-simple-checkbox>
  <v-btn @click="makeItem">Submit</v-btn>
</template>

<script>
const axios = require("axios").default;

import GenericSelect from "@/components/page/GenericSelect.vue";

export default {
  name: "GenericFormComponent",
  components: {
    GenericSelect,
  },
  props: {
    collectionName: String,
    collectionParams: Array,
  },
  data() {
    return {
      rules: {
        required: (value) => !!value || "Required",
        integer_digits: (value) => {
          const pattern = /^-?\d+$/;
          return pattern.test(value) || "Invalid value";
        },
        float_digits: (value) => {
          const pattern = /^-?\d+.?\d+$/;
          return pattern.test(value) || "Invalid value";
        },
        text: (value) => {
          const pattern = /^[A-Za-z0-9]+$/;
          return pattern.test(value) || "Invalid value";
        },
      },
      outputParams: [],
    };
  },
  methods: {
    async makeItem() {
      const data = {};
      for (const index in this.outputParams) {
        data[this.outputParams[index]["name"]] =
          this.outputParams[index]["inputValue"];
      }
      await axios.post(
        "http://127.0.0.1:8000/v1/data/" + this.collectionName,
        data
      );
      this.$emit("item-created");
    },
  },
  mounted() {
    console.log("mounted:", this.collectionParams, this.collectionName);
    this.outputParams.length = 0;
    for (const index in this.collectionParams) {
      console.log(index);
      this.outputParams.push(this.collectionParams[index]);
      switch (this.outputParams[index]["type"]) {
        case "String":
          this.outputParams[index]["inputValue"] = "";
          break;
        case "Integer":
          this.outputParams[index]["inputValue"] = 0;
          break;
        case "Float":
          this.outputParams[index]["inputValue"] = 0.0;
          break;
        case "Bool":
          this.outputParams[index]["inputValue"] = "false";
          break;
        case "Datetime":
          this.outputParams[index]["inputValue"] = "false";
          break;
        default:
          this.outputParams[index]["inputValue"] = "";
          break;
      }
    }
  },
};
</script>
