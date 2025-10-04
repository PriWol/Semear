// export.js - Exportar/Importar dados
const Exporter = {
  // Exportar JSON
  exportJSON(data, filename = 'semear-backup.json') {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    this.downloadBlob(blob, filename);
  },

  // Exportar CSV de métricas
  exportMetricsCSV(metrics, filename = 'semear-metrics.csv') {
    if (!metrics || metrics.length === 0) {
      alert('Nenhuma métrica para exportar');
      return;
    }

    const headers = ['Timestamp', 'Tipo', 'Dados'];
    const rows = metrics.map(m => [
      m.ts,
      m.type,
      JSON.stringify(m.payload)
    ]);

    const csv = [
      headers.join(','),
      ...rows.map(r => r.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    this.downloadBlob(blob, filename);
  },

  // Download de blob
  downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  // Importar JSON
  async importJSON(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          resolve(data);
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }
};

export default Exporter;
