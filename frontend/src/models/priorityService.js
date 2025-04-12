import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

// Fetch cities
export const loadCities = () => {
  return axios.get(`${BASE_API_URL}/priorities/cities`);
};

// Fetch districts by city_id
export const loadDistricts = (cityId) => {
  return axios.get(`${BASE_API_URL}/priorities/cities/${cityId}/districts`);
};

// Fetch schools by district_id
export const loadSchools = (districtId) => {
  return axios.get(`${BASE_API_URL}/priorities/districts/${districtId}/schools`);
};

// Global search for schools, cities, districts
export const globalSearch = (query) => {
  return axios.get(`${BASE_API_URL}/priorities/search?q=${encodeURIComponent(query)}`);
};
