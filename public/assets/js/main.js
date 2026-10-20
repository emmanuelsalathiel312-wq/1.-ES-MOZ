(function(){
  var cfg = window.ZAYAMARA || {};
  var btn=document.querySelector('.menu-btn'), nav=document.getElementById('nav');
  if(btn&&nav){btn.addEventListener('click',function(){
    var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o);});}
  var fb=document.querySelectorAll('.filters button');
  fb.forEach(function(b){b.addEventListener('click',function(){
    fb.forEach(function(x){x.setAttribute('aria-pressed','false')});
    b.setAttribute('aria-pressed','true');
    var f=b.dataset.filter;
    document.querySelectorAll('[data-cat]').forEach(function(c){
      c.hidden = !(f==='all'||c.dataset.cat===f);});
  });});
  var form=document.getElementById('contact-form');
  if(form){form.addEventListener('submit',function(e){
    e.preventDefault();
    if(form.querySelector('.hp input').value) return;
    var msg=document.getElementById('form-msg');
    var en=document.documentElement.lang==='en';
    var T=en?{ok:'Message sent. Thank you, we will be in touch soon.',err:'We could not send your message. Please try again or email us.',mail:'Opening your email app to send the message…'}
            :{ok:'Mensagem enviada. Obrigado, voltamos a falar consigo em breve.',err:'Não foi possível enviar. Tente novamente ou escreva-nos por email.',mail:'A abrir o seu programa de email para enviar a mensagem…'};
    var d=new FormData(form);
    if(cfg.formEndpoint){
      fetch(cfg.formEndpoint,{method:'POST',body:d,headers:{Accept:'application/json'}})
        .then(function(r){if(!r.ok)throw 0;form.reset();msg.hidden=false;msg.textContent=T.ok;})
        .catch(function(){msg.hidden=false;msg.textContent=T.err;});
    } else if(cfg.email){
      var body=['name','email','country','interest','message'].map(function(k){return k+': '+(d.get(k)||'')}).join('\n');
      msg.hidden=false;msg.textContent=T.mail;
      location.href='mailto:'+cfg.email+'?subject='+encodeURIComponent('Zayamara - '+(d.get('interest')||''))+'&body='+encodeURIComponent(body);
    } else { msg.hidden=false;msg.textContent=T.err; }
  });}
})();
