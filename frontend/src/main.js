import { createApp } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import App from "./App.vue";

import '@mdi/font/css/materialdesignicons.css'
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from 'vuetify/iconsets/mdi';

import HomeComponent from "@/components/HomeComponent.vue";
import AboutComponent from "@/components/AboutComponent.vue";
import GenericPageComponent from "@/components/page/GenericPageComponent.vue";
import GenericDashboardComponent from "@/components/dashboard/GenericDashboardComponent.vue";
import MainConfigurationComponent from "@/components/configuration/MainConfigurationComponent.vue";
import CollectionsTemplateComponent from "@/components/configuration/CollectionsTemplateComponent.vue";
import ActionsComponent from "@/components/configuration/ActionsComponent.vue";
import DashboardsComponent from "@/components/configuration/DashboardsComponent.vue";

const routes = [
  { path: "/", component: HomeComponent },
  { path: "/configuration", component: MainConfigurationComponent },
  {
    path: "/configuration/collections",
    component: CollectionsTemplateComponent,
  },
  { path: "/configuration/actions", component: ActionsComponent },
  { path: "/configuration/dashboards", component: DashboardsComponent },
  { path: "/about", component: AboutComponent },
  { path: "/pages/:page", component: GenericPageComponent },
  { path: "/dashboard/:dashboardId", component: GenericDashboardComponent },
];

const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
});

const app = createApp(App);
app.use(router);
app.use(vuetify);
app.mount("#app");
