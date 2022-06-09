import { BigNumber } from "ethers";
import { parseUnits } from "ethers/lib/utils";

export interface Config {
  gravity_contract_address: string;
  tft_token_contract_address: string;
  bridge_fees: BigNumber;
  tft_decimals: number;
  tft_denom: string;

  cosmos_rest: string;
  tendermint_rpc: string;
  proposal_denom: string;
  gas_price: string;
  chain_id: string;
}

async function validateConfig(config: { [key: string]: any }) {
  const props = [
    "BRIDGE_FEES",
    "TFT_TOKEN_CONTRACT_ADDRESS",
    "GRAVITY_CONTRACT_ADDRESS",
    "TFT_DECIMALS",
    "TFT_DENOM",
    "COSMOS_REST",
    "TENDERMINT_RPC",
    "PROPOSAL_DENOM",
    "GAS_PRICE",
    "CHAIN_ID",
  ];
  const numbers = ["BRIDGE_FEES", "TFT_DECIMALS"];
  for (const prop of props) {
    if (config[prop] === undefined) {
      throw new Error(prop + " is required and not present in the env vars");
    }
  }
  for (const prop of numbers) {
    if (isNaN(+config[prop])) {
      throw new Error(
        ((prop + "=" + config[prop]) as string) + " is not a valid number"
      );
    }
  }
}

export function loadConfig(): Config {
  const config = window.config;
  validateConfig(config);
  const tft_decimals = +(config["TFT_DECIMALS"] as string);
  return {
    bridge_fees: parseUnits(config["BRIDGE_FEES"], tft_decimals),
    tft_token_contract_address: config["TFT_TOKEN_CONTRACT_ADDRESS"],
    gravity_contract_address: config["GRAVITY_CONTRACT_ADDRESS"],
    tft_decimals: tft_decimals,
    tft_denom: config["TFT_DENOM"],
    cosmos_rest: config["COSMOS_REST"] as string,
    tendermint_rpc: config["TENDERMINT_RPC"] as string,
    proposal_denom: config["PROPOSAL_DENOM"] as string,
    gas_price: config["GAS_PRICE"] as string,
    chain_id: config["CHAIN_ID"] as string,
  };
}
