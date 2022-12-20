import { GridClient, NetworkEnv } from "grid3_client";
import { HTTPMessageBusClient } from "ts-rmb-http-client";

export async function isMnemonicsExist(value: string) {
  const grid = new GridClient(
    window.configs.APP_NETWORK as unknown as NetworkEnv,
    value,
    value,
    new HTTPMessageBusClient(0, "", "", ""),
  );

  try {
    await grid.connect();
    await grid.disconnect();
    return true;
  } catch {
    return false;
  }
}
