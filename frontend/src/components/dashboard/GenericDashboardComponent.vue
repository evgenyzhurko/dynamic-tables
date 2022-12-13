<template>
  <h1>{{ dashboardId }}</h1>
  <TableViewComponent
    :dashboardId="dashboardId"
  />
</template>

<script>
import TableViewComponent from "@/components/dashboard/TableViewComponent.vue";

// const axios = require("axios").default;

export default {
  components: {
    TableViewComponent,
  },
  computed: {
    dashboardId() {
      return this.$route.params.dashboardId;
    },
  }
};
</script>
