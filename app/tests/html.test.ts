import { describe, expect, it } from 'vitest';
import { confiavel, escapar, html, textoRico } from '../src/ui/html';

describe('html seguro', () => {
  it('escapa texto interpolado (proteção contra injeção de HTML)', () => {
    const nome = '<img src=x onerror=alert(1)>';
    expect(html`<p>${nome}</p>`.valor).toBe('<p>&lt;img src=x onerror=alert(1)&gt;</p>');
  });
  it('escapa aspas em atributos', () => {
    expect(html`<input value="${'" onfocus="x'}">`.valor).toBe(
      '<input value="&quot; onfocus=&quot;x">',
    );
  });
  it('não escapa de novo o que já é HtmlSeguro e junta listas', () => {
    const itens = ['a', 'b'].map((x) => html`<li>${x}</li>`);
    expect(html`<ul>${itens}</ul>`.valor).toBe('<ul><li>a</li><li>b</li></ul>');
    expect(html`${confiavel('<b>ok</b>')}`.valor).toBe('<b>ok</b>');
  });
  it('omite null, undefined e false', () => {
    expect(html`a${null}${undefined}${false}b`.valor).toBe('ab');
  });
  it('escapar cobre os 5 caracteres especiais', () => {
    expect(escapar(`&<>"'`)).toBe('&amp;&lt;&gt;&quot;&#39;');
  });
});

describe('textoRico', () => {
  it('aceita **negrito** e *itálico*', () => {
    expect(textoRico('um **dois** *três*').valor).toBe('um <b>dois</b> <i>três</i>');
  });
  it('não deixa o conteúdo injetar HTML', () => {
    expect(textoRico('**<script>x</script>**').valor).toBe('<b>&lt;script&gt;x&lt;/script&gt;</b>');
  });
});
