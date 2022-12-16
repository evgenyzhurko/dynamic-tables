<template>
  <v-container fluid>
    <v-form ref="form">
      <v-row align-content="center" justify="center">
        <v-text-field
          :label="paramName"
          :rules="[rules.required, rules.text]"
          v-model="optionName"
          required
        />
        <v-btn @click="appendOption">Append Option</v-btn><br />
      </v-row>
      <v-container fluid>
        <v-chip v-for="(option, index) in options" :key="index"
          >{{ option }}
          <!-- <v-btn icon  color="transparent"> -->
          <v-icon size="x-small" @click="removeOption(option)">mdi-close-circle</v-icon>
          <!-- </v-btn> -->
        </v-chip>
        {{ options }}
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: "SelectCreatorComponent",
  props: {
    paramName: String,
  },
  data() {
    return {
      optionName: "",
      options: [],
      rules: {
        required: (value) => !!value || "Required",
        text: (value) => {
          const pattern = /^[A-Za-z0-9]+$/;
          return pattern.test(value) || "Invalid value";
        },
      },
    };
  },
  methods: {
    async appendOption() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.options.push(this.optionName);
      this.optionName = "";
      this.$refs.form.reset();
      this.$refs.form.resetValidation();
      this.notify();
    },
    removeOption(item) {
      this.options.splice(this.options.indexOf(item), 1);
      this.notify();
    },
    notify() {
      this.$emit("optionsChanged", this.options);
    },
  },
};
</script>
