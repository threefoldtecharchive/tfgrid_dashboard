import axios from "axios";
import config from "../config";

export async function getNodeUsedResources(nodeId: any) {
    const res = await axios.get(`${config.gridproxyUrl}nodes/${nodeId}`, {
      timeout: 1000,
    });
  
    if (res.status === 200) {
      if (res.data == "likely down") {
        throw Error("likely down");
      } else {
        return res.data.capacity.used_resources;
      }
    }
  }