<template>
  <h1>{{ pageName }}</h1>
  <!-- <div>{{ pageInfo }}</div> -->
  <GenericFormComponent
    v-if="loaded"
    :collectionName="pageName"
    :collectionParams="pageParams"
    @item-created="update"
  />
  <TableViewComponent
    ref="tableview"
    v-if="loaded"
    :collectionName="pageName"
    :collectionParams="pageParams"
    :pageInfo="pageInfo"
  />
</template>

<script>
import GenericFormComponent from "@/components/page/GenericFormComponent.vue";
import TableViewComponent from "@/components/page/TableViewComponent.vue";

const axios = require("axios").default;

export default {
  name: "GenericPageComponent",
  components: {
    GenericFormComponent,
    TableViewComponent,
  },
  data() {
    return {
      pageInfo: null,
      pageParams: null,
      loaded: false,
    };
  },
  computed: {
    pageName() {
      return this.$route.params.page;
    },
  },
  methods: {
    update() {
      this.loaded = false;
      if (!this.pageName) {
        return;
      }
      axios
        .get(
          "http://127.0.0.1:8000/v1/configuration/collections?name=" +
            this.pageName
        )
        .then(
          (response) => (
            (this.pageInfo = response["data"]["result"][0]),
            (this.pageParams = this.pageInfo["params"]),
            (this.loaded = true)
          )
        );
    },
  },
  watch: {
    $route() {
      this.update();
    },
  },
  mounted() {
    this.update();
  },
};
</script>
