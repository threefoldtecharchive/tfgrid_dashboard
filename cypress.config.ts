import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    
    baseUrl: 'https://dashboard.qa.grid.tf',
    
    setupNodeEvents(on, config) {

    },
  },
});
