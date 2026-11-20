// Tabela de rotas do app (ADR 0008). Fica fora do main.ts para os testes conferirem a ordem: a primeira
// que casa vence, então "/sessao/registrar" precisa vir antes de "/sessao/:id" (#11).
import type { FabricaPagina } from './ui/app';
import { paginaInicio } from './pages/inicio';
import { paginaFamilia } from './pages/familia';
import { paginaCrianca } from './pages/crianca';
import { paginaJornada } from './pages/jornada';
import { paginaSessaoNova } from './pages/sessao-nova';
import { paginaRegistrarBusca } from './pages/registrar-busca';
import { paginaSessaoRegistrar } from './pages/sessao-registrar';
import { paginaSessao } from './pages/sessao';
import { paginaConfig } from './pages/config';
import { paginaBiblioteca } from './pages/biblioteca';
import { paginaConteudo } from './pages/conteudo';
import { paginaAcervo } from './pages/acervo';
import { paginaSondagem } from './pages/sondagem';
import { paginaAtividades } from './pages/atividades';
import { paginaSemana } from './pages/semana';
import { paginaGuia } from './pages/guia';
import { paginaPrivacidade } from './pages/privacidade';
import { paginaNovidades } from './pages/novidades';

export const ROTAS: Record<string, FabricaPagina> = {
  '/': paginaInicio,
  '/familia': paginaFamilia,
  '/crianca/:id': paginaCrianca,
  '/jornada/:id': paginaJornada,
  '/sessao/nova': paginaSessaoNova,
  '/sessao/registrar': paginaRegistrarBusca,
  '/sessao/:id/registrar': paginaSessaoRegistrar,
  '/sessao/:id': paginaSessao,
  '/config': paginaConfig,
  '/biblioteca': paginaBiblioteca,
  '/acervo': paginaAcervo,
  '/sondagem/:id': paginaSondagem,
  '/atividades': paginaAtividades,
  '/semana/:id': paginaSemana,
  '/guia': paginaGuia,
  '/privacidade': paginaPrivacidade,
  '/conteudo': paginaConteudo,
  '/novidades': paginaNovidades,
};
