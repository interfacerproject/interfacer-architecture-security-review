/* Mermaid vendorizzato: nessuna dipendenza runtime da CDN. */
(function () {
  async function renderDiagrams() {
    const blocks = document.querySelectorAll('pre.diagram:not([data-rendered])');
    if (!blocks.length || !window.mermaid) return;
    const dark = document.body.getAttribute('data-md-color-scheme') === 'slate';
    mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: dark ? 'dark' : 'neutral' });
    for (const [index, block] of Array.from(blocks).entries()) {
      try {
        const { svg } = await mermaid.render('review-diagram-' + index, block.textContent);
        const figure = document.createElement('figure');
        figure.className = 'review-diagram';
        figure.setAttribute('aria-label', 'Diagramma architetturale');
        figure.innerHTML = svg;
        block.dataset.rendered = 'true';
        block.replaceWith(figure);
      } catch (error) {
        block.dataset.diagramError = 'true';
        console.error('Diagramma Mermaid non valido', error);
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', renderDiagrams);
  else renderDiagrams();
})();
