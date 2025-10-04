// data-loader.js - Carrega dados JSON estáticos
class DataLoader {
  constructor() {
    this.cache = {};
  }

  async load(path) {
    if (this.cache[path]) {
      return this.cache[path];
    }

    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      this.cache[path] = data;
      return data;
    } catch (e) {
      console.error(`Erro ao carregar ${path}:`, e);
      return null;
    }
  }

  async getValues() {
    return await this.load('/data/values.json');
  }

  async getResources() {
    return await this.load('/data/resources.json');
  }

  getValueById(values, id) {
    return values.find(v => v.id === id);
  }

  getResourceById(resources, id) {
    return resources.find(r => r.id === id);
  }

  filterResources(resources, filters = {}) {
    let filtered = [...resources];

    if (filters.type) {
      filtered = filtered.filter(r => r.type === filters.type);
    }

    if (filters.ageRange) {
      filtered = filtered.filter(r => r.ageRange === filters.ageRange);
    }

    if (filters.values && filters.values.length > 0) {
      filtered = filtered.filter(r => 
        r.values.some(v => filters.values.includes(v))
      );
    }

    if (filters.styles && filters.styles.length > 0) {
      filtered = filtered.filter(r => 
        r.styles.some(s => filters.styles.includes(s))
      );
    }

    if (filters.format) {
      filtered = filtered.filter(r => r.format === filters.format);
    }

    return filtered;
  }

  // Calcular idade a partir da data de nascimento
  calculateAge(birthdate) {
    const today = new Date();
    const birth = new Date(birthdate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  }

  // Determinar faixa etária
  getAgeRange(age) {
    if (age >= 0 && age <= 2) return '0-2';
    if (age >= 3 && age <= 6) return '3-6';
    if (age >= 7 && age <= 10) return '7-10';
    return '10+';
  }
}

export default DataLoader;
