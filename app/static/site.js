// Ortak gezinme ve ana sayfadaki küçük keşif alıştırması.
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) { navigation.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('open')) {
    navigation.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); toggle.focus();
  }
});
const puzzle = document.querySelector('#puzzle');
if (puzzle) {
  let round = 0, solved = false;
  const status = document.querySelector('#puzzle-status');
  function newRound() {
    round += 1; solved = false;
    document.querySelector('#round').textContent = String(round).padStart(2,'0');
    status.textContent = 'Diğerlerinden farklı şekli bul.';
    puzzle.replaceChildren();
    const different = Math.floor(Math.random()*20);
    for (let i=0; i<20; i++) {
      const button = document.createElement('button');
      button.type='button'; button.className='shape-button';
      const special=i===different;
      button.setAttribute('aria-label', (i+1)+'. şekil: '+(special?'ortasında boş halka bulunan göz':'ortasında dolu nokta bulunan göz'));
      // Sabit SVG öğeleri; kullanıcı girdisi HTML'e eklenmez.
      const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('viewBox','0 0 48 32'); svg.setAttribute('aria-hidden','true');
      const outline=document.createElementNS(svg.namespaceURI,'path');
      outline.setAttribute('d','M3 16 Q24 -6 45 16 Q24 38 3 16 Z');
      const center=document.createElementNS(svg.namespaceURI,'circle');
      center.setAttribute('cx','24');center.setAttribute('cy','16');center.setAttribute('r','5');
      if (!special) center.style.fill='currentColor';
      svg.append(outline,center);button.append(svg);
      button.addEventListener('click',()=>{
        if(solved) return;
        if(special){ solved=true;button.classList.add('found');status.textContent='Buldun! Küçük bir detay, yeni bir bakış. Yeni bir tur deneyebilirsin.'; }
        else {button.classList.add('missed');status.textContent='Bir kez daha bak. İpucu: şekillerin merkezine dikkat et.';}
      });
      puzzle.append(button);
    }
  }
  document.querySelector('#new-puzzle').addEventListener('click',newRound);
  newRound();
}
