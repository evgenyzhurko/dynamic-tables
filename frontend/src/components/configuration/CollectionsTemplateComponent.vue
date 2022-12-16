<template>
  <h1>Create new data collection template</h1>
  <v-form ref="form">
    <div>
      <v-text-field
        label="Collection Name"
        :rules="[rules.required, rules.text]"
        v-model="name"
        required
      />
    </div>
    <div v-for="(item, index) in params" :key="index">
      <v-row>
        <v-text-field
          class="pa-2 ma-2"
          label="Param Name"
          :rules="[rules.required, rules.text]"
          v-model="item.name"
          required
        />

        <v-col class="pa-2 ma-2">
          <v-select
            label="Data type"
            :items="dtypes"
            v-model="item.type"
            required
          >
          </v-select>
          <div v-if="item.type == 'Select' || item.type == 'Multiselect'">
            <SelectCreatorComponent
              :paramName="Option"
              @optionsChanged="(opt) => (item.options = opt)"
            />
          </div>
        </v-col>
      </v-row>
      <v-btn @click="removeCollectionParam(index)">Delete Param</v-btn><br />
    </div>
    <v-btn @click="addCollectionParam">+ param</v-btn><br />
    <v-btn @click="createDataCollectionTemplate">Create template</v-btn>
  </v-form>
</template>

<script>
import SelectCreatorComponent from "@/components/configuration/SelectCreatorComponent.vue";

const axios = require("axios").default;

export default {
  components: {
    SelectCreatorComponent,
  },
  data() {
    return {
      name: "",
      params: [],
      dtypes: [
        "String",
        "Integer",
        "Float",
        "Bool",
        "Datetime",
        "Date",
        "Time",
        "Select",
        "Multiselect",
      ],
      rules: {
        required: (value) => !!value || "Required",
        text: (value) => {
          const pattern = /^[A-Za-z0-9]+$/;
          return pattern.test(value) || "Invalid value";
        },
      },
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/v1/configuration/collections")
      .then((response) =>
        this.updateReferenceDtypes(response["data"]["result"])
      );
  },
  methods: {
    async createDataCollectionTemplate() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      await axios.post("http://127.0.0.1:8000/v1/configuration/collections", {
        name: this.name,
        params: this.params,
      });

      this.$refs.form.reset();
      this.$refs.form.resetValidation();
    },
    addCollectionParam() {
      this.params.push({
        name: "",
        type: "",
        options: [],
      });
    },
    removeCollectionParam(index) {
      this.params.splice(index, 1);
    },
    updateReferenceDtypes(data) {
      for (var index in data) {
        this.dtypes.push("Ref<" + data[index]["name"] + ">");
      }
    },
  },
};
</script>
