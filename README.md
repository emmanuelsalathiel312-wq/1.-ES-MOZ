# ZAYAMARA — O caminho que nos liga / The Path That Connects Us

Site de turismo bilingue (PT/EN), estático, sem dependências. Pronto para Vercel.

## Estrutura
```
zayamara/
├── build.py            # gerador: edite CONFIG e conteúdo, corra `python3 build.py`
├── vercel.json         # configuração de deploy (serve a pasta public/)
├── public/             # site final (o que o Vercel publica)
│   ├── index.html      # escolhe PT/EN pelo idioma do browser
│   ├── pt/  en/        # páginas: início, destinos, experiências, sobre, colaborar, contacto
│   ├── assets/css  assets/js  assets/img
│   ├── favicon.svg  robots.txt  sitemap.xml
└── docs/LAUNCH-CHECKLIST.md
```

## Deploy no Vercel
**Pelo site:** vercel.com → Add New → Project → importe este repositório (ou arraste a pasta) → Framework Preset "Other" → Deploy. Não precisa de build command.
**Pela CLI:** `npm i -g vercel` e, na pasta do projeto, `vercel --prod`.

## Antes de publicar
1. Abra `build.py` e preencha `CONFIG` (domínio, email, telefone, WhatsApp, redes sociais, endpoint do formulário).
2. Corra `python3 build.py` (precisa só de Python 3) e faça deploy novamente.
3. Siga `docs/LAUNCH-CHECKLIST.md`.

## Pré-visualizar localmente
```
cd public && python3 -m http.server 8000   # http://localhost:8000
```

## Formulário de contacto
- Com `form_endpoint` (ex.: Formspree), envia a mensagem diretamente.
- Só com `email`, abre o programa de email do visitante.
- Sem nenhum dos dois, mostra erro: preencha um deles antes de publicar.

## Editar conteúdo
Todo o texto está em `build.py`, em duas línguas lado a lado: `_("português", "english")`.
