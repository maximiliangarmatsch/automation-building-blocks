import axios from "axios";

export const BASE_API = "http://127.0.0.1:8000";

export const API_ENDPOINTS = {
  AUTH: "/auth",
  GET_PROFILE: "/get_profile",
  ATTRACTIVENESS: "/attractiveness_score",
  EXTRACT_FEATURES: "/extract_features",
  CREATE_PROFILE: "/create_profile",
  DELETE_PROFILE: "/delete_user",
};

export default axios.create({
  baseURL: BASE_API,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});
