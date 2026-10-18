# Crea le due pagine dei quiz, una per corso, da quiz.html: link separati da mettere nei gruppi Telegram,
# ognuna con la sua anteprima (immagine e titolo). Si rilancia dopo ogni modifica a quiz.html:
#   python3 nuovo/riskly/quiz_pagine.py
import os
QUI = os.path.dirname(os.path.abspath(__file__))
base = open(os.path.join(QUI, 'quiz.html'), encoding='utf-8').read()
CORSI = {
  'rischio': ('Gestione del rischio', 'Quiz di fine modulo del corso Riskly di gestione del rischio: 5 domande per modulo e attestato finale.'),
  'fondamentale': ('Analisi fondamentale', 'Quiz di fine modulo del corso Riskly di analisi fondamentale: 5 domande per modulo e attestato finale.'),
}
for k, (nome, descr) in CORSI.items():
  s = base.replace('<title>Riskly — Quiz e attestato</title>', f'''<title>Quiz · {nome} · Riskly</title>
<meta name="description" content="{descr}">
<meta property="og:type" content="website">
<meta property="og:title" content="Quiz e attestato · {nome}">
<meta property="og:description" content="{descr}">
<meta property="og:url" content="https://riskly.trade/quiz-{k}">
<meta property="og:image" content="https://riskly.trade/img/quiz-{k}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>window.QUIZ_CORSO = '{k}';</script>''', 1)
  s = s.replace('<span class="kick">QUIZ E ATTESTATO</span>', f'<span class="kick">QUIZ · {nome.upper()}</span>', 1)
  assert 'window.QUIZ_CORSO' in s
  open(os.path.join(QUI, f'quiz-{k}.html'), 'w', encoding='utf-8').write(s)
  print('scritto quiz-%s.html' % k)
