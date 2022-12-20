import { GridClient, NetworkEnv } from "grid3_client";
import { HTTPMessageBusClient } from "ts-rmb-http-client";

export function getGrid(mnemonics: string) {
  const grid = new GridClient(
    window.configs.APP_NETWORK as unknown as NetworkEnv,
    mnemonics,
    mnemonics,
    new HTTPMessageBusClient(0, "", "", ""),
  );
  return grid.connect().then(() => grid);
}

export async function isMnemonicsExist(value: string) {
  try {
    const grid = await getGrid(value);
    await grid.disconnect();
    return true;
  } catch {
    return false;
  }
}

const SSH_REGEX =
  /^(sk-)?(ssh-rsa AAAAB3NzaC1yc2|ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNT|ecdsa-sha2-nistp384 AAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAAAIbmlzdHAzOD|ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1Mj|ssh-ed25519 AAAAC3NzaC1lZDI1NTE5|ssh-dss AAAAB3NzaC1kc3)[0-9A-Za-z+/]+[=]{0,3}( .*)?$/;
export function isValidSSH(value: string) {
  return SSH_REGEX.test(value);
}
