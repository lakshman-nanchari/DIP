import axios from "axios";
import NProgress from "nprogress";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

API.interceptors.request.use((config) => {

  NProgress.start();

  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;

}, (error) => {

  NProgress.done();
  return Promise.reject(error);

});


API.interceptors.response.use((response) => {

  NProgress.done();
  return response;

}, (error) => {

  NProgress.done();
  return Promise.reject(error);

});

export default API;