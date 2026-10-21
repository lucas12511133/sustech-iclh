const fs=require('fs'),path=require('path');
for(const entry of ['index.html','en.html']){
const html=fs.readFileSync(path.join('dist',entry),'utf8');
const ids=new Set([...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]));
const refs=[...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(x=>x[1]);
const missing=refs.filter(x=>!x.startsWith('http')&&!x.startsWith('mailto:')&&(x.startsWith('#')?!ids.has(x.slice(1)):!fs.existsSync(path.join('dist',x.split('?')[0]))));
console.log(JSON.stringify({entry,missing,sections:(html.match(/<section/g)||[]).length,localImages:(html.match(/<img/g)||[]).length}));
if(missing.length)process.exit(1);
if(entry==='en.html'){
const untranslated=html.replace(/<script[\s\S]*?<\/script>/g,'').replace(/中文/g,'').match(/[\u4e00-\u9fff]+/g);
if(untranslated)throw Error('Untranslated English content: '+untranslated.join(', '));
if(!html.includes('lang="en"')||!html.includes('english.css'))throw Error('English language or stylesheet missing');
}
}

