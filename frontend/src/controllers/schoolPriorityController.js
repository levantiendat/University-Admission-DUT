// src/controllers/SchoolPriorityController.js
import * as PriorityService from '@/models/priorityService';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import debounce from 'lodash/debounce';

export default function useSchoolPriorityController() {
  const router = useRouter();
  
  // State variables
  const cities = ref([]);
  const districts = ref([]);
  const schools = ref([]);
  const selectedCity = ref('');
  const selectedDistrict = ref('');
  const selectedSchool = ref('');
  const globalQuery = ref('');
  const suggestions = ref([]);
  const isLoading = ref(false);
  
  // Initialize by loading cities on component mount
  const initialize = async () => {
    await fetchCities();
  };
  
  // Fetch all cities
  const fetchCities = async () => {
    try {
      isLoading.value = true;
      const response = await PriorityService.loadCities();
      cities.value = response.data;
      console.log('Cities:', cities.value);
    } catch (error) {
      console.error('Error fetching cities:', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch districts based on selected city
  const fetchDistricts = async () => {
    selectedDistrict.value = '';
    schools.value = [];
    
    if (!selectedCity.value) {
      districts.value = [];
      return;
    }
    
    try {
      isLoading.value = true;
      const response = await PriorityService.loadDistricts(selectedCity.value);
      districts.value = response.data;
    } catch (error) {
      console.error('Error fetching districts:', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch schools based on selected district
  const fetchSchools = async () => {
    selectedSchool.value = '';
    
    if (!selectedDistrict.value) {
      schools.value = [];
      return;
    }
    
    try {
      isLoading.value = true;
      const response = await PriorityService.loadSchools(selectedDistrict.value);
      schools.value = response.data;
    } catch (error) {
      console.error('Error fetching schools:', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  // Global search functionality
  const performGlobalSearch = debounce(async () => {
    if (globalQuery.value.length < 2) {
      suggestions.value = [];
      return;
    }
    
    try {
      const response = await PriorityService.globalSearch(globalQuery.value);
      suggestions.value = response.data;
    } catch (error) {
      console.error('Error performing global search:', error);
    }
  }, 300);
  
  // Watch for changes to globalQuery to trigger search
  watch(globalQuery, () => {
    performGlobalSearch();
  });
  
  // Navigate to detail page based on selection
  const navigateToDetail = (item) => {
    if (item.type === 'city') {
      router.push(`/city/${item.id}`);
    } else if (item.type === 'district') {
      router.push(`/district/${item.id}`);
    } else if (item.type === 'school') {
      router.push(`/school/${item.id}`);
    }
  };
  
  // Submit search form
  const submitSearchForm = () => {
    if (selectedSchool.value) {
      router.push(`/school/${selectedSchool.value}`);
    }
  };
  
  return {
    // State
    cities,
    districts,
    schools,
    selectedCity,
    selectedDistrict,
    selectedSchool,
    globalQuery,
    suggestions,
    isLoading,
    
    // Methods
    initialize,
    fetchDistricts,
    fetchSchools,
    navigateToDetail,
    submitSearchForm,
  };
}