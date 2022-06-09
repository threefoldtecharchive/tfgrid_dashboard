import Vue, { VNode } from "vue";

interface AppConfigs {
  gql_url: string;
  polkadot_url: string;
  proxy_url: string;
  version: string;
}

declare global {
  namespace JSX {
    // tslint:disable no-empty-interface
    interface Element extends VNode {}
    // tslint:disable no-empty-interface
    interface ElementClass extends Vue {}
    interface IntrinsicElements {
      [elem: string]: any;
    }
    interface WindowInterface extends Window {
      [url: URL];
    }
  }

  interface Window {
    keplr: any;
    ethereum: any;
    config: any;
    configs: AppConfigs;
  }

  declare module "*.json" {
    let value: any;
    return value;
  }
}
