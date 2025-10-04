// storage.js - Abstração para localStorage com fallback
const Storage = {
  // Prefixo para todas as chaves
  prefix: 'semear_',

  // Salvar dados
  set(key, value) {
    try {
      const serialized = JSON.stringify(value);
      localStorage.setItem(this.prefix + key, serialized);
      return true;
    } catch (e) {
      console.error('Erro ao salvar no localStorage:', e);
      return false;
    }
  },

  // Recuperar dados
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(this.prefix + key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
      console.error('Erro ao ler do localStorage:', e);
      return defaultValue;
    }
  },

  // Remover dados
  remove(key) {
    try {
      localStorage.removeItem(this.prefix + key);
      return true;
    } catch (e) {
      console.error('Erro ao remover do localStorage:', e);
      return false;
    }
  },

  // Limpar tudo
  clear() {
    try {
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.startsWith(this.prefix)) {
          localStorage.removeItem(key);
        }
      });
      return true;
    } catch (e) {
      console.error('Erro ao limpar localStorage:', e);
      return false;
    }
  },

  // Exportar todos os dados
  exportAll() {
    const data = {};
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(this.prefix)) {
        const cleanKey = key.replace(this.prefix, '');
        data[cleanKey] = this.get(cleanKey);
      }
    });
    return data;
  },

  // Importar dados
  importAll(data) {
    try {
      Object.keys(data).forEach(key => {
        this.set(key, data[key]);
      });
      return true;
    } catch (e) {
      console.error('Erro ao importar dados:', e);
      return false;
    }
  }
};

// API específica para o app
const AppStorage = {
  // Profile
  getProfile() {
    return Storage.get('profile');
  },
  
  setProfile(profile) {
    return Storage.set('profile', profile);
  },

  // Weekly Plans
  getWeeklyPlans() {
    return Storage.get('weeklyPlans', []);
  },

  setWeeklyPlans(plans) {
    return Storage.set('weeklyPlans', plans);
  },

  getCurrentWeekPlan(childId) {
    const plans = this.getWeeklyPlans();
    const weekStart = this.getWeekStart();
    return plans.find(p => p.childId === childId && p.weekStartISO === weekStart);
  },

  saveWeeklyPlan(plan) {
    const plans = this.getWeeklyPlans();
    const index = plans.findIndex(p => p.id === plan.id);
    if (index >= 0) {
      plans[index] = plan;
    } else {
      plans.push(plan);
    }
    return this.setWeeklyPlans(plans);
  },

  // Diary
  getDiaries() {
    return Storage.get('diaries', []);
  },

  setDiaries(diaries) {
    return Storage.set('diaries', diaries);
  },

  getCurrentWeekDiary(childId) {
    const diaries = this.getDiaries();
    const weekStart = this.getWeekStart();
    return diaries.find(d => d.childId === childId && d.weekStartISO === weekStart);
  },

  saveDiary(diary) {
    const diaries = this.getDiaries();
    const index = diaries.findIndex(d => d.id === diary.id);
    if (index >= 0) {
      diaries[index] = diary;
    } else {
      diaries.push(diary);
    }
    return this.setDiaries(diaries);
  },

  // Metrics
  getMetrics() {
    return Storage.get('metrics', []);
  },

  logMetric(type, payload) {
    const metrics = this.getMetrics();
    metrics.push({
      ts: new Date().toISOString(),
      type,
      payload
    });
    return Storage.set('metrics', metrics);
  },

  // Helpers
  getWeekStart(date = new Date()) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Segunda-feira
    const monday = new Date(d.setDate(diff));
    monday.setHours(0, 0, 0, 0);
    return monday.toISOString().split('T')[0];
  },

  generateId(prefix = 'item') {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
};

export { Storage, AppStorage };
