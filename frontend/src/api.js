import axios from 'axios';

const api = axios.create({
  baseURL: 'https://turnover-dashboard-production-2a7a.up.railway.app/api',
});

export default api;
