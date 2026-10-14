// Versão do app embutida no build (vite.config.ts, `define`). Ver #38.
declare const __VERSAO__: string;
declare const __DATA_BUILD__: string;
declare const __COMMIT__: string;

export interface InfoVersao {
  /** ex.: "0.2.0", do package.json */
  numero: string;
  /** data e hora do build, em ISO */
  data: string;
  /** código curto do commit publicado, ou "local" */
  commit: string;
}

export const VERSAO: InfoVersao = { numero: __VERSAO__, data: __DATA_BUILD__, commit: __COMMIT__ };
