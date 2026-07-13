import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Add error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const analyzeText = async (data: { text: string; context?: string }) => {
  try {
    const response = await api.post('/scam/analyze', data);
    return response.data;  // ← THIS IS THE FIX! Return just the data, not the whole response
  } catch (error) {
    console.error('Scam analysis failed:', error);
    throw error;
  }
};

export const analyzeJob = async (data: { job_text: string; company_name?: string }) => {
  try {
    const response = await api.post('/jobs/analyze', data);
    return response.data;
  } catch (error) {
    console.error('Job analysis failed:', error);
    throw error;
  }
};

export const checkURL = async (data: { url: string }) => {
  try {
    const response = await api.post('/url/check', data);
    return response.data;
  } catch (error) {
    console.error('URL check failed:', error);
    throw error;
  }
};

export const analyzeImage = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append('image', file);
    const response = await api.post('/image/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Image analysis failed:', error);
    throw error;
  }
};

export default api;