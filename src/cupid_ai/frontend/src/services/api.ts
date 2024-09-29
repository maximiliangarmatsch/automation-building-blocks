import axios from "axios";

const BASE_API = "http://3.87.57.146:8000";

export const API_ENDPOINTS = {
  AUTH: "/auth",
};

export default axios.create({
  baseURL: BASE_API,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});
