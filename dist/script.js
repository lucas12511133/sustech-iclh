const isEnglish=document.documentElement.lang==='en';
const languageSwitch=document.querySelector('[data-language-switch]');
function updateLanguageLink(){if(languageSwitch)languageSwitch.href=(isEnglish?'index.html':'en.html')+location.hash}
updateLanguageLink();window.addEventListener('hashchange',updateLanguageLink);
const anchors=[...document.querySelectorAll('.section-nav a')];
const sections=anchors.map(a=>document.querySelector(a.getAttribute('href')));
let scheduled=false;function updateNav(){let current=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<=150)current=section}anchors.forEach(a=>{const active=a.hash==='#'+current.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});scheduled=false}
window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateNav)}},{passive:true});updateNav();
const dialog=document.querySelector('#image-dialog');
document.querySelectorAll('.zoom-button').forEach(button=>button.addEventListener('click',()=>{dialog.querySelector('img').src=button.dataset.image;dialog.querySelector('img').alt=button.dataset.title;dialog.querySelector('h2').textContent=button.dataset.title;dialog.showModal()}));
dialog.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
const dutyTabs=[...document.querySelectorAll('[data-duty]')];
let selectedDuty=0;
function selectDuty(index,focus=false){selectedDuty=(index+4)%4;dutyTabs.forEach((tab,i)=>{const active=i===selectedDuty;tab.classList.toggle('is-active',active);tab.setAttribute('aria-selected',String(active));tab.setAttribute('tabindex',active?'0':'-1');document.getElementById('duty-panel-'+i).hidden=!active});if(focus)dutyTabs[selectedDuty].focus()}
dutyTabs.forEach((tab,i)=>{tab.addEventListener('click',()=>selectDuty(i));tab.addEventListener('keydown',event=>{if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End','Enter',' '].includes(event.key)){event.preventDefault();let next=i;if(['ArrowRight','ArrowDown'].includes(event.key))next=i+1;else if(['ArrowLeft','ArrowUp'].includes(event.key))next=i-1;else if(event.key==='Home')next=0;else if(event.key==='End')next=3;selectDuty(next,true)}})});
document.querySelector('.duty-prev').addEventListener('click',()=>selectDuty(selectedDuty-1));document.querySelector('.duty-next').addEventListener('click',()=>selectDuty(selectedDuty+1));
