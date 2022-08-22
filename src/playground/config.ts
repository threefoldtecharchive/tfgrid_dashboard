import * as client from "ts-rmb-http-client";
import * as grid3_client from "grid3_client";
import * as buffer from "buffer";
import * as bip39 from "bip39";

(window as any).configs = (window as any).configs || {};
(window as any).configs = {
  ...(window as any).configs,
  client,
  grid3_client,
  buffer,
  bip39,
};
