export declare type TwinType = {
  id: string;
  relay: string;
  pk: string;
};

export declare type UserCredentials = {
  accountAddress: string;
  accountName: string;
  twinID: number;
  balanceFree: number;
  balanceReserved: number;
  relayAddress: string;
  publicKey: string;
  twin: TwinType;
  initialized: boolean;
};
