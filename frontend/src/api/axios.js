import axios from "axios";
import NProgress from "nprogress";

let activeRequests = 0;

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000,
});

// REQUEST INTERCEPTOR
API.interceptors.request.use(
  (config) => {
    activeRequests++;
    if (activeRequests === 1) NProgress.start();

    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    activeRequests--;
    if (activeRequests === 0) NProgress.done();
    return Promise.reject(error);
  }
);

// RESPONSE INTERCEPTOR
API.interceptors.response.use(
  (response) => {
    activeRequests--;
    if (activeRequests === 0) NProgress.done();
    return response;
  },
  (error) => {
    activeRequests--;
    if (activeRequests === 0) NProgress.done();

    const status = error.response?.status;

    // 🔥 HANDLE 401 (important)
    if (status === 401) {
      localStorage.removeItem("token");

      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }
    }

    return Promise.reject(error);
  }
);

export default API;