# -*- coding: utf-8 -*-
import base64
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def b64img(name):
    with open(os.path.join(BASE, name), 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

IMGS = {name: b64img(name) for name in [
    '01_baseline_rfe_curve.png',
    '02_baseline_real_vs_previsto.png',
    '03_matriz_correlacao.png',
    '04_comparacao_modelos.png',
    '05_rfe_ridge_curve.png',
    '06_gridsearch_alpha.png',
    '07_melhorado_real_vs_previsto.png',
    '08_comparacao_final.png',
]}

def img_tag(name, alt):
    return f'<img src="data:image/png;base64,{IMGS[name]}" alt="{alt}" loading="lazy" />'

html = f"""<title>ELT579 — Aula 2: Regressão e Seleção de Features</title>
<style>
  :root {{
    --bg: #f6f7f2;
    --paper: #fbfcf9;
    --ink: #1c231f;
    --muted: #5c6660;
    --line: #dde1d7;
    --accent: #3f6b4f;
    --accent-soft: #e7efe6;
    --baseline: #8b93a6;
    --improved: #3f6b4f;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    background: var(--bg);
    color: var(--ink);
    font-family: Charter, Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    font-size: 17px;
    line-height: 1.65;
    margin: 0;
    padding: 0 24px 96px;
  }}

  .page {{
    max-width: 760px;
    margin: 0 auto;
  }}

  header.masthead {{
    padding: 64px 0 32px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 40px;
  }}

  .eyebrow {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 12px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 600;
    margin: 0 0 14px;
  }}

  h1 {{
    font-size: 32px;
    line-height: 1.2;
    margin: 0 0 10px;
    text-wrap: balance;
    font-weight: 600;
    letter-spacing: -0.01em;
  }}

  .subtitle {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--muted);
    font-size: 15px;
    margin: 0;
  }}

  .meta {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 13px;
    color: var(--muted);
    margin-top: 18px;
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .meta strong {{ color: var(--ink); font-weight: 600; }}

  section {{
    margin: 56px 0;
  }}

  .section-head {{
    display: flex;
    align-items: baseline;
    gap: 14px;
    margin-bottom: 20px;
  }}

  .section-num {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-soft);
    border-radius: 3px;
    padding: 3px 8px;
    letter-spacing: 0.02em;
    flex-shrink: 0;
  }}

  h2 {{
    font-size: 23px;
    margin: 0;
    font-weight: 600;
    text-wrap: balance;
  }}

  h3 {{
    font-size: 17px;
    font-weight: 700;
    margin: 32px 0 10px;
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    letter-spacing: 0.01em;
  }}

  p {{ margin: 0 0 16px; max-width: 68ch; }}

  strong {{ font-weight: 700; }}

  ul, ol {{ margin: 0 0 16px; padding-left: 22px; }}
  li {{ margin-bottom: 6px; max-width: 64ch; }}

  figure {{
    margin: 26px 0;
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 16px;
  }}
  figure img {{
    display: block;
    width: 100%;
    height: auto;
    border-radius: 3px;
  }}
  figcaption {{
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 12.5px;
    color: var(--muted);
    margin-top: 10px;
    letter-spacing: 0.01em;
  }}
  figcaption b {{ color: var(--ink); }}

  .table-wrap {{ overflow-x: auto; margin: 20px 0; }}

  table {{
    border-collapse: collapse;
    width: 100%;
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14.5px;
  }}
  caption {{
    caption-side: top;
    text-align: left;
    font-size: 12.5px;
    color: var(--muted);
    margin-bottom: 8px;
    letter-spacing: 0.01em;
  }}
  th, td {{
    text-align: left;
    padding: 9px 14px;
    border-bottom: 1px solid var(--line);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }}
  th {{
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.06em;
    border-bottom: 2px solid var(--ink);
  }}
  tr:last-child td {{ border-bottom: none; }}
  td.improved {{ color: var(--improved); font-weight: 700; }}
  td.metric-name {{ font-family: Charter, Georgia, serif; font-weight: 600; white-space: normal; }}

  .callout {{
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    border-radius: 0 6px 6px 0;
    padding: 18px 22px;
    margin: 24px 0;
  }}
  .callout p {{ margin: 0; max-width: none; }}
  .callout .stat-row {{
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    margin-top: 12px;
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  }}
  .stat {{ }}
  .stat .label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    display: block;
    margin-bottom: 2px;
  }}
  .stat .value {{
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
    font-variant-numeric: tabular-nums;
  }}
  .stat .value .from {{
    color: var(--muted);
    font-weight: 500;
    font-size: 14px;
  }}

  code, .mono {{
    font-family: ui-monospace, "SF Mono", Consolas, monospace;
    font-size: 0.88em;
    background: var(--accent-soft);
    padding: 1px 5px;
    border-radius: 3px;
  }}

  footer {{
    margin-top: 72px;
    padding-top: 24px;
    border-top: 1px solid var(--line);
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 12.5px;
    color: var(--muted);
  }}
  footer ul {{ padding-left: 18px; margin-top: 8px; }}

  @media print {{
    body {{ background: #fff; padding: 0; font-size: 12.5pt; }}
    figure {{ break-inside: avoid; border-color: #ccc; }}
    section {{ break-inside: avoid-page; margin: 32px 0; }}
    .callout {{ break-inside: avoid; }}
    a {{ color: inherit; text-decoration: none; }}
  }}

  @media (max-width: 600px) {{
    h1 {{ font-size: 26px; }}
    .callout .stat-row {{ gap: 20px; }}
  }}
</style>

<div class="page">

<header class="masthead">
  <p class="eyebrow">ELT579 · Aprendizado de Máquina Aplicado</p>
  <h1>Regressão e Seleção de Features — Severidade de Doença em Tomate</h1>
  <p class="subtitle">Relatório da Semana 2 — reprodução do script original, modificações implementadas e comparação de resultados</p>
  <div class="meta">
    <span><strong>Aluno</strong> 123103</span>
    <span><strong>Dataset</strong> dataset_problema2.csv (132 amostras, 20 features)</span>
    <span><strong>Alvo</strong> Severidade (regressão)</span>
  </div>
</header>

<section id="intro">
  <div class="section-head"><span class="section-num">1</span><h2>Introdução</h2></div>
  <p>O problema da Semana 2 consiste em prever a <strong>severidade de uma doença em plantas de
  tomate</strong> (coluna <code>Severidade</code>, variável contínua) a partir de <strong>índices
  de vegetação</strong> extraídos de imagens de sensoriamento remoto (drone), calculados em quatro
  momentos distintos do ciclo da cultura (dias 1, 4, 8 e 28). Para cada dia estão disponíveis cinco
  índices — <code>NDVI</code>, <code>SAVI</code>, <code>GNDVI</code>, <code>MCARI1</code> e
  <code>SR</code> — totalizando <strong>20 variáveis preditoras</strong> para <strong>132
  amostras</strong>.</p>
  <p>O script fornecido (<code>script_problema2.py</code>) implementa um pipeline que separa os
  dados em treino (80%) e teste (20%), padroniza as features com <code>StandardScaler</code>,
  aplica <strong>Recursive Feature Elimination (RFE)</strong> com <code>LinearRegression</code>
  para encontrar o número ideal de features (1 a 20, validado por 10-fold cross-validation) e
  treina o modelo final com as 10 features escolhidas. Este relatório documenta a reprodução desse
  pipeline (baseline) e as modificações implementadas para melhorar a predição.</p>
</section>

<section id="objetivo">
  <div class="section-head"><span class="section-num">2</span><h2>Objetivo</h2></div>
  <ul>
    <li>Implementar e executar a solução original, reproduzindo os resultados de <code>script_problema2.py</code>.</li>
    <li>Investigar a correlação entre as 20 features para embasar decisões de modelagem.</li>
    <li>Testar modificações no pipeline — outros algoritmos de regressão, outro estimador de base
      no RFE, otimização de hiperparâmetros — buscando <strong>melhorar R², RMSE e MAE</strong>
      em relação ao script original.</li>
    <li>Comparar baseline e modelo melhorado usando <strong>exatamente o mesmo split treino/teste</strong>
      (<code>random_state=0</code>, <code>test_size=0.2</code>) para garantir uma comparação justa.</li>
  </ul>
</section>

<section id="metodologia">
  <div class="section-head"><span class="section-num">3</span><h2>Metodologia</h2></div>

  <h3>3.1 · Reprodução do script original (baseline)</h3>
  <p>O script original foi executado sem alterações. Ele usa <code>train_test_split</code>
  (80/20, <code>random_state=0</code>), <code>StandardScaler</code> e <code>RFE</code> com
  <code>LinearRegression</code> percorrendo de 1 a 20 features, fixando o modelo final em
  10 features.</p>

  <figure>
    {img_tag('01_baseline_rfe_curve.png', 'Curva de R² por número de features via RFE (baseline)')}
    <figcaption><b>Print 1 —</b> Curva de R² (validação cruzada, 10 folds) em função do número de
    features selecionadas pelo RFE original. O pico ocorre em 10 features (R² CV = 0,8656),
    confirmando que o script fornecido já opera no ponto ótimo dessa curva.</figcaption>
  </figure>

  <figure>
    {img_tag('02_baseline_real_vs_previsto.png', 'Gráfico de dispersão real vs previsto do baseline')}
    <figcaption><b>Print 2 —</b> Severidade real vs. prevista no conjunto de teste (Regressão
    Linear, 10 features). Os pontos ficam razoavelmente próximos da reta y = x, mas com dispersão
    visível em severidades mais altas — indício de espaço para melhoria.</figcaption>
  </figure>

  <h3>3.2 · Modificações implementadas</h3>
  <p>Foram implementadas quatro modificações no pipeline, cada uma com uma motivação específica.</p>

  <p><strong>a) Análise de correlação entre features.</strong> Antes de alterar o modelo, foi
  gerada a matriz de correlação das 20 features.</p>

  <figure>
    {img_tag('03_matriz_correlacao.png', 'Matriz de correlação entre as 20 features')}
    <figcaption><b>Print 3 —</b> Matriz de correlação de Pearson entre as 20 features. Foram
    encontrados <strong>64 pares com correlação absoluta acima de 0,9</strong> — esperado, já que
    os cinco índices derivam das mesmas bandas espectrais e os quatro dias de coleta captam o
    mesmo fenômeno em momentos próximos. Essa multicolinearidade motivou a troca do estimador
    usado no RFE por um modelo com regularização.</figcaption>
  </figure>

  <p><strong>b) Comparação sistemática de 8 algoritmos de regressão.</strong> Em vez de assumir
  que a Regressão Linear é o melhor modelo, foi feito um benchmark com validação cruzada
  (10 folds embaralhados) usando as 20 features padronizadas: Regressão Linear, Ridge, Lasso,
  ElasticNet, KNN Regressor, SVR (RBF), Random Forest e Gradient Boosting.</p>

  <figure>
    {img_tag('04_comparacao_modelos.png', 'Comparação de 8 algoritmos de regressão por R² médio')}
    <figcaption><b>Print 4 —</b> R² médio (CV = 10) de cada algoritmo, todas as 20 features. O KNN
    teve o melhor desempenho bruto (0,8228), mas não expõe coeficientes nem
    <code>feature_importances_</code> — não é compatível com o RFE usado na seleção de features.
    Por isso a modificação seguiu com <strong>Ridge</strong>, que mantém compatibilidade com RFE,
    é interpretável e lida melhor com a multicolinearidade identificada no Print 3.</figcaption>
  </figure>

  <p><strong>c) Nova seleção de features — RFE com Ridge em vez de Regressão Linear.</strong>
  Repetiu-se a busca de 1 a 20 features, agora usando <code>Ridge</code> como estimador de base.</p>

  <figure>
    {img_tag('05_rfe_ridge_curve.png', 'Curva de R² por número de features via RFE com Ridge')}
    <figcaption><b>Print 5 —</b> O número ótimo de features passou a ser <strong>12</strong> (em
    vez de 10 no script original), com subconjunto diferente do original — incluindo, por
    exemplo, <code>MCARI1_d28</code>, ausente nas 10 features do script original.</figcaption>
  </figure>

  <p><strong>d) Otimização de hiperparâmetro via GridSearchCV.</strong> Com as 12 features
  selecionadas, foi feita uma busca em grade do parâmetro de regularização <code>alpha</code> do
  Ridge, testando 11 valores em escala logarítmica (0,001 a 100).</p>

  <figure>
    {img_tag('06_gridsearch_alpha.png', 'GridSearchCV do hiperparâmetro alpha do Ridge')}
    <figcaption><b>Print 6 —</b> R² médio (CV = 10) por valor de alpha. O melhor valor encontrado
    foi <strong>alpha = 0,1</strong>: uma regularização leve já é suficiente para estabilizar o
    modelo sem prejudicar seu poder preditivo.</figcaption>
  </figure>

  <h3>3.3 · Modelo final melhorado</h3>
  <p>O modelo final combina as três modificações: <strong>Ridge (alpha = 0,1) + RFE com 12
  features</strong>, avaliado no mesmo split treino/teste do script original para permitir
  comparação direta e justa com o baseline.</p>
</section>

<section id="resultados">
  <div class="section-head"><span class="section-num">4</span><h2>Resultados</h2></div>

  <div class="callout">
    <p>As três métricas de erro melhoraram simultaneamente no conjunto de teste, com o ganho mais
    expressivo no erro médio absoluto.</p>
    <div class="stat-row">
      <div class="stat"><span class="label">R² (teste)</span><span class="value">0,8961 <span class="from">← 0,8876</span></span></div>
      <div class="stat"><span class="label">RMSE (teste)</span><span class="value">7,25 <span class="from">← 7,54</span></span></div>
      <div class="stat"><span class="label">MAE (teste)</span><span class="value">5,52 <span class="from">← 6,34 (−13%)</span></span></div>
    </div>
  </div>

  <h3>4.1 · Tabela comparativa (conjunto de teste, mesmo split random_state=0)</h3>
  <div class="table-wrap">
    <table>
      <caption>Baseline (script original) vs. modelo melhorado (Ridge + RFE + GridSearchCV)</caption>
      <thead>
        <tr><th>Métrica</th><th>Baseline</th><th>Melhorado</th><th>Variação</th></tr>
      </thead>
      <tbody>
        <tr><td class="metric-name">R² (teste)</td><td>0,8876</td><td class="improved">0,8961</td><td>+0,0085 (+0,96%)</td></tr>
        <tr><td class="metric-name">RMSE (teste)</td><td>7,5395</td><td class="improved">7,2492</td><td>−0,2903 (−3,85%)</td></tr>
        <tr><td class="metric-name">MAE (teste)</td><td>6,3441</td><td class="improved">5,5199</td><td>−0,8242 (−12,99%)</td></tr>
        <tr><td class="metric-name">Nº de features</td><td>10</td><td>12</td><td>+2</td></tr>
        <tr><td class="metric-name">Modelo</td><td>Regressão Linear</td><td>Ridge (alpha=0,1)</td><td>—</td></tr>
      </tbody>
    </table>
  </div>

  <h3>4.2 · Gráfico comparativo final</h3>
  <figure>
    {img_tag('08_comparacao_final.png', 'Gráfico de barras comparando baseline e modelo melhorado nas três métricas')}
    <figcaption><b>Print 7 —</b> R², RMSE e MAE lado a lado — baseline vs. modelo melhorado, ambos
    avaliados no mesmo conjunto de teste.</figcaption>
  </figure>

  <h3>4.3 · Real vs. Previsto — modelo melhorado</h3>
  <figure>
    {img_tag('07_melhorado_real_vs_previsto.png', 'Gráfico de dispersão real vs previsto do modelo melhorado')}
    <figcaption><b>Print 8 —</b> Comparado ao Print 2 (baseline), os pontos do modelo melhorado
    ficam mais próximos da reta y = x, especialmente em valores intermediários de severidade —
    refletindo a queda do MAE de 6,34 para 5,52.</figcaption>
  </figure>

  <h3>4.4 · Discussão</h3>
  <p>As três modificações — troca do estimador de base do RFE para Ridge, ajuste do número de
  features para 12 e otimização do hiperparâmetro <code>alpha</code> — resultaram em melhoria
  <strong>consistente nas três métricas</strong> avaliadas no conjunto de teste. O ganho mais
  expressivo foi no MAE (−13%), relevante em um cenário prático de apoio à decisão agronômica
  (ex.: definir limiares para intervenção no campo).</p>
  <p>A análise de correlação (Print 3) explica por que a Regressão Linear pura do script original,
  apesar de já obter um bom resultado, é mais sensível a ruído: com 64 pares de features fortemente
  correlacionadas, pequenas variações nos dados de treino podem gerar coeficientes instáveis — a
  regularização Ridge mitiga esse problema. O benchmark de algoritmos (Print 4) mostrou ainda que
  modelos não lineares como KNN e SVR são competitivos neste problema, e ficam como sugestão de
  trabalho futuro, desde que combinados com um método de seleção de features compatível (ex.:
  <code>SelectKBest</code>, <code>SequentialFeatureSelector</code>), já que o RFE exige um
  estimador com coeficientes ou importância de features.</p>
</section>

<section id="conclusao">
  <div class="section-head"><span class="section-num">5</span><h2>Conclusão</h2></div>
  <p>O script original já apresentava uma boa solução (R² de teste ≈ 0,89). As modificações
  implementadas — análise de multicolinearidade, benchmark de algoritmos, troca do estimador do
  RFE para Ridge e otimização de hiperparâmetro via GridSearchCV — produziram uma melhoria
  mensurável e consistente em todas as métricas de erro avaliadas, mantendo a interpretabilidade
  do modelo linear original.</p>
</section>

<footer>
  <p>Anexos</p>
  <ul>
    <li>Script original executado (baseline): <code>relatorio_outputs/baseline.py</code></li>
    <li>Script com as modificações implementadas: <code>script_problema2_melhorado.py</code></li>
    <li>Saídas numéricas: <code>relatorio_outputs/baseline_resultados.txt</code>,
      <code>relatorio_outputs/melhorado_resultados.txt</code></li>
  </ul>
</footer>

</div>
"""

out_path = os.path.join(BASE, 'elt579-aula2-resposta.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('OK ->', out_path, len(html), 'chars')
