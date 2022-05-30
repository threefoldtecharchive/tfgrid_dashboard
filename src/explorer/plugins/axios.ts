import axios from "axios";

export const req = axios.create({
  baseURL: "https://gridproxy.dev.grid.tf",
});
