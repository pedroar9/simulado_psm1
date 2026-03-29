import streamlit as st
import random
import time
import re
import json
import os
import pandas as pd
from datetime import date, datetime
import pytz

# --- Configuracoes de hora     ---  
fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora = datetime.now(fuso_brasilia)
data_atual = agora.today().strftime("%d/%m/%Y")

# --- Data de build (data de modificação do arquivo) ---
data_build = datetime.fromtimestamp(os.path.getmtime(__file__), fuso_brasilia).strftime("%d/%m/%Y")


# --- Questoes ---
questions_data = [
  {
    "question": "Quais são os três pilares do Scrum?",
    "options": ["Transparência, Inspeção, Adaptação", "Planejamento, Execução, Entrega", "Comunicação, Colaboração, Comprometimento", "Análise, Design, Implementação"],
    "answer": "Transparência, Inspeção, Adaptação",
    "explanation": "Segundo o Scrum Guide 2020, os três pilares empíricos do Scrum são: Transparência, Inspeção e Adaptação. Eles sustentam toda a estrutura do framework.",
    "difficulty": "easy"
  },
  {
    "question": "Quais são os cinco valores do Scrum?",
    "options": ["Comprometimento, Coragem, Foco, Abertura, Respeito", "Confiança, Transparência, Colaboração, Entrega, Melhoria", "Honestidade, Integridade, Responsabilidade, Disciplina, Qualidade", "Velocidade, Qualidade, Comunicação, Inovação, Flexibilidade"],
    "answer": "Comprometimento, Coragem, Foco, Abertura, Respeito",
    "explanation": "O Scrum Guide define cinco valores: Comprometimento, Coragem, Foco, Abertura e Respeito. Esses valores direcionam o trabalho, ações e comportamento do Scrum Team.",
    "difficulty": "easy"
  },
  {
    "question": "O Scrum é um framework ou uma metodologia?",
    "options": ["Um framework", "Uma metodologia", "Um processo", "Uma técnica de gerenciamento"],
    "answer": "Um framework",
    "explanation": "O Scrum Guide define o Scrum como um framework leve que ajuda pessoas, times e organizações a gerar valor por meio de soluções adaptativas para problemas complexos. Não é uma metodologia.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum pode ser usado apenas para desenvolvimento de software.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide 2020 afirma que o Scrum foi inicialmente desenvolvido para software, mas é aplicável a qualquer trabalho complexo em diversos domínios.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é o tamanho máximo recomendado para um Scrum Team?",
    "options": ["10 ou menos pessoas", "7 pessoas", "15 pessoas", "Não há limite definido"],
    "answer": "10 ou menos pessoas",
    "explanation": "Segundo o Scrum Guide, o Scrum Team é tipicamente composto por 10 ou menos pessoas. Times menores se comunicam melhor e são mais produtivos.",
    "difficulty": "easy"
  },
  {
    "question": "Quem é responsável por maximizar o valor do produto resultante do trabalho do Scrum Team?",
    "options": ["O Product Owner", "O Scrum Master", "Os Developers", "O Stakeholder principal"],
    "answer": "O Product Owner",
    "explanation": "O Scrum Guide define que o Product Owner é responsável por maximizar o valor do produto resultante do trabalho do Scrum Team.",
    "difficulty": "easy"
  },
  {
    "question": "Quem compõe o Scrum Team?",
    "options": ["Scrum Master, Product Owner e Developers", "Scrum Master, Product Owner, Developers e Stakeholders", "Product Owner, Developers e Testers", "Scrum Master e Developers apenas"],
    "answer": "Scrum Master, Product Owner e Developers",
    "explanation": "O Scrum Team consiste em um Scrum Master, um Product Owner e Developers. Não há sub-times ou hierarquias dentro do Scrum Team.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é a duração máxima de uma Sprint?",
    "options": ["Um mês (4 semanas)", "2 semanas", "3 meses", "Não há limite definido"],
    "answer": "Um mês (4 semanas)",
    "explanation": "O Scrum Guide estabelece que Sprints têm duração fixa de um mês ou menos. Sprints mais curtas podem ser usadas para reduzir riscos.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Master é o líder/chefe do Scrum Team.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Master é um líder servidor (servant-leader) que serve ao Scrum Team. O Scrum Team é auto-gerenciável e não possui hierarquia interna.",
    "difficulty": "easy"
  },
  {
    "question": "O que é o Product Backlog?",
    "options": ["Uma lista ordenada e emergente do que é necessário para melhorar o produto", "Uma lista fixa de requisitos do projeto", "O plano de trabalho definido pelo gerente de projetos", "O documento de escopo do produto"],
    "answer": "Uma lista ordenada e emergente do que é necessário para melhorar o produto",
    "explanation": "O Product Backlog é uma lista ordenada e emergente do que é necessário para melhorar o produto. É a única fonte de trabalho realizado pelo Scrum Team.",
    "difficulty": "easy"
  },
  {
    "question": "Quem é responsável por gerenciar o Product Backlog?",
    "options": ["O Product Owner", "O Scrum Master", "Os Developers", "Todo o Scrum Team"],
    "answer": "O Product Owner",
    "explanation": "O Product Owner é o responsável por gerenciar o Product Backlog, incluindo sua ordenação, clareza e transparência.",
    "difficulty": "easy"
  },
  {
    "question": "O que é o Sprint Backlog?",
    "options": ["A Meta da Sprint, os itens do Product Backlog selecionados para a Sprint, e o plano para entregá-los", "Uma lista de bugs encontrados na Sprint", "O relatório de progresso da Sprint", "As tarefas atribuídas pelo Scrum Master"],
    "answer": "A Meta da Sprint, os itens do Product Backlog selecionados para a Sprint, e o plano para entregá-los",
    "explanation": "O Sprint Backlog é composto pela Meta da Sprint (por quê), o conjunto de itens do Product Backlog selecionados (o quê) e um plano acionável para entregar o Incremento (como).",
    "difficulty": "medium"
  },
  {
    "question": "O que é um Incremento no Scrum?",
    "options": ["Um passo concreto em direção à Meta do Produto que atende à Definição de Pronto", "Qualquer trabalho feito durante a Sprint", "O relatório de entrega da Sprint", "Uma nova versão do Product Backlog"],
    "answer": "Um passo concreto em direção à Meta do Produto que atende à Definição de Pronto",
    "explanation": "Um Incremento é um passo concreto em direção à Meta do Produto. Cada Incremento é adicionado a todos os Incrementos anteriores e deve atender à Definição de Pronto.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Múltiplos Incrementos podem ser criados dentro de uma Sprint.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que múltiplos Incrementos podem ser criados dentro de uma Sprint. A soma dos Incrementos é apresentada na Sprint Review.",
    "difficulty": "medium"
  },
  {
    "question": "O que é a Definição de Pronto (Definition of Done)?",
    "options": ["Uma descrição formal do estado do Incremento quando atende às medidas de qualidade exigidas", "Uma lista de tarefas criada pelo Product Owner", "Os critérios de aceitação de cada item do Product Backlog", "O checklist de testes do QA"],
    "answer": "Uma descrição formal do estado do Incremento quando atende às medidas de qualidade exigidas",
    "explanation": "A Definição de Pronto é uma descrição formal do estado do Incremento quando atende às medidas de qualidade exigidas para o produto. Cria transparência sobre o que foi completado.",
    "difficulty": "medium"
  },
  {
    "question": "Quem cria a Definição de Pronto?",
    "options": ["Se não for um padrão organizacional, o Scrum Team deve criar uma apropriada", "Apenas o Product Owner", "Apenas o Scrum Master", "Os Stakeholders"],
    "answer": "Se não for um padrão organizacional, o Scrum Team deve criar uma apropriada",
    "explanation": "Se a Definição de Pronto para um Incremento não for um padrão da organização, o Scrum Team deve criar uma Definição de Pronto apropriada para o produto.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o propósito da Daily Scrum?",
    "options": ["Inspecionar o progresso em direção à Meta da Sprint e adaptar o Sprint Backlog conforme necessário", "Reportar o status para o Scrum Master", "Atribuir tarefas aos Developers", "Revisar o Product Backlog"],
    "answer": "Inspecionar o progresso em direção à Meta da Sprint e adaptar o Sprint Backlog conforme necessário",
    "explanation": "O propósito da Daily Scrum é inspecionar o progresso em direção à Meta da Sprint e adaptar o Sprint Backlog conforme necessário, ajustando o trabalho planejado.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é a duração máxima (time-box) da Daily Scrum?",
    "options": ["15 minutos", "30 minutos", "1 hora", "Não há time-box definido"],
    "answer": "15 minutos",
    "explanation": "A Daily Scrum é um evento de 15 minutos para os Developers do Scrum Team.",
    "difficulty": "easy"
  },
  {
    "question": "Quem participa da Daily Scrum?",
    "options": ["Os Developers", "Todo o Scrum Team obrigatoriamente", "Developers e Scrum Master obrigatoriamente", "Developers, Product Owner e Stakeholders"],
    "answer": "Os Developers",
    "explanation": "A Daily Scrum é um evento para os Developers. Se o Product Owner ou Scrum Master estão trabalhando ativamente em itens do Sprint Backlog, eles participam como Developers.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o propósito da Sprint Review?",
    "options": ["Inspecionar o resultado da Sprint e determinar adaptações futuras", "Avaliar o desempenho individual dos Developers", "Planejar a próxima Sprint", "Aprovar ou rejeitar o trabalho feito"],
    "answer": "Inspecionar o resultado da Sprint e determinar adaptações futuras",
    "explanation": "O propósito da Sprint Review é inspecionar o resultado da Sprint e determinar adaptações futuras. O Scrum Team apresenta os resultados do trabalho para stakeholders-chave.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é a duração máxima da Sprint Review para uma Sprint de um mês?",
    "options": ["4 horas", "2 horas", "8 horas", "1 hora"],
    "answer": "4 horas",
    "explanation": "A Sprint Review tem time-box de no máximo 4 horas para uma Sprint de um mês. Para Sprints mais curtas, o evento é geralmente menor.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o propósito da Sprint Retrospective?",
    "options": ["Planejar maneiras de aumentar a qualidade e a eficácia", "Revisar os itens entregues na Sprint", "Definir o Product Backlog da próxima Sprint", "Avaliar os stakeholders"],
    "answer": "Planejar maneiras de aumentar a qualidade e a eficácia",
    "explanation": "O propósito da Sprint Retrospective é planejar maneiras de aumentar a qualidade e a eficácia. O Scrum Team inspeciona como foi a última Sprint em relação a pessoas, interações, processos e ferramentas.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é a duração máxima da Sprint Retrospective para uma Sprint de um mês?",
    "options": ["3 horas", "4 horas", "2 horas", "1 hora"],
    "answer": "3 horas",
    "explanation": "A Sprint Retrospective tem time-box de no máximo 3 horas para uma Sprint de um mês.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é a duração máxima da Sprint Planning para uma Sprint de um mês?",
    "options": ["8 horas", "4 horas", "2 horas", "1 dia"],
    "answer": "8 horas",
    "explanation": "A Sprint Planning tem time-box de no máximo 8 horas para uma Sprint de um mês. Para Sprints mais curtas, o evento é geralmente mais curto.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Planning aborda três tópicos: Por que esta Sprint é valiosa? O que pode ser feito? Como o trabalho será realizado?",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Sprint Planning aborda: 1) Por que esta Sprint é valiosa? (Meta da Sprint), 2) O que pode ser feito nesta Sprint? (seleção de itens), 3) Como o trabalho escolhido será realizado? (plano de entrega).",
    "difficulty": "medium"
  },
  {
    "question": "O que acontece quando a Sprint é cancelada?",
    "options": ["Quaisquer itens 'Prontos' são revisados; se parte do trabalho for potencialmente liberável, o PO tipicamente o aceita", "Todo o trabalho é descartado", "A Sprint continua até o final com escopo reduzido", "Os Developers decidem o que manter"],
    "answer": "Quaisquer itens 'Prontos' são revisados; se parte do trabalho for potencialmente liberável, o PO tipicamente o aceita",
    "explanation": "Se uma Sprint for cancelada, quaisquer itens do Product Backlog completados e 'Prontos' são revisados. Se parte do trabalho for potencialmente liberável, o Product Owner tipicamente o aceita.",
    "difficulty": "hard"
  },
  {
    "question": "Quem pode cancelar uma Sprint?",
    "options": ["Apenas o Product Owner", "O Scrum Master", "Os Developers", "Qualquer membro do Scrum Team"],
    "answer": "Apenas o Product Owner",
    "explanation": "Apenas o Product Owner tem autoridade para cancelar a Sprint. Uma Sprint pode ser cancelada se a Meta da Sprint se tornar obsoleta.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o compromisso (commitment) associado ao Product Backlog?",
    "options": ["Meta do Produto (Product Goal)", "Meta da Sprint (Sprint Goal)", "Definição de Pronto (Definition of Done)", "Visão do Produto"],
    "answer": "Meta do Produto (Product Goal)",
    "explanation": "A Meta do Produto é o compromisso associado ao Product Backlog. Ela descreve o estado futuro do produto e serve como alvo para o Scrum Team planejar.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o compromisso associado ao Sprint Backlog?",
    "options": ["Meta da Sprint (Sprint Goal)", "Meta do Produto (Product Goal)", "Definição de Pronto (Definition of Done)", "Plano de Release"],
    "answer": "Meta da Sprint (Sprint Goal)",
    "explanation": "A Meta da Sprint é o compromisso associado ao Sprint Backlog. Ela é o único objetivo da Sprint e dá flexibilidade em relação ao trabalho exato necessário.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é o compromisso associado ao Incremento?",
    "options": ["Definição de Pronto (Definition of Done)", "Meta da Sprint (Sprint Goal)", "Meta do Produto (Product Goal)", "Critérios de Aceitação"],
    "answer": "Definição de Pronto (Definition of Done)",
    "explanation": "A Definição de Pronto é o compromisso associado ao Incremento. Um item do Product Backlog que não atende à Definição de Pronto não pode ser considerado um Incremento.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Master é responsável pela eficácia do Scrum Team.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que o Scrum Master é responsável (accountable) pela eficácia do Scrum Team, ajudando-o a melhorar suas práticas dentro do framework Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "Qual das seguintes NÃO é uma responsabilidade do Scrum Master?",
    "options": ["Atribuir tarefas aos Developers", "Facilitar eventos Scrum conforme solicitado ou necessário", "Remover impedimentos ao progresso dos Developers", "Ajudar todos a entender a teoria e prática do Scrum"],
    "answer": "Atribuir tarefas aos Developers",
    "explanation": "O Scrum Master nunca atribui tarefas. Os Developers são auto-gerenciáveis e decidem internamente quem faz o quê, quando e como.",
    "difficulty": "easy"
  },
  {
    "question": "Como o Scrum Master serve ao Product Owner?",
    "options": ["Todas as alternativas estão corretas", "Ajudando a encontrar técnicas para definição eficaz de Meta do Produto e gerenciamento do Product Backlog", "Facilitando a colaboração dos stakeholders conforme solicitado ou necessário", "Ajudando a estabelecer planejamento empírico do produto para um ambiente complexo"],
    "answer": "Todas as alternativas estão corretas",
    "explanation": "O Scrum Guide lista várias formas pelas quais o Scrum Master serve ao PO, incluindo técnicas de gerenciamento do Product Backlog, planejamento empírico e facilitação da colaboração com stakeholders.",
    "difficulty": "medium"
  },
  {
    "question": "Como o Scrum Master serve à organização?",
    "options": ["Todas as alternativas estão corretas", "Liderando, treinando e orientando a organização na adoção do Scrum", "Planejando e aconselhando implementações de Scrum dentro da organização", "Removendo barreiras entre stakeholders e Scrum Teams"],
    "answer": "Todas as alternativas estão corretas",
    "explanation": "O Scrum Master serve à organização de diversas formas, incluindo liderar a adoção do Scrum, planejar implementações e remover barreiras entre stakeholders e Scrum Teams.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner pode delegar a responsabilidade de gerenciar o Product Backlog para os Developers.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Product Owner pode delegar o trabalho de gerenciamento do Product Backlog para outros, porém o Product Owner permanece como o responsável (accountable) final.",
    "difficulty": "hard"
  },
  {
    "question": "O Product Owner é uma pessoa ou um comitê?",
    "options": ["Uma pessoa", "Um comitê", "Depende do tamanho da organização", "Pode ser um comitê de até 3 pessoas"],
    "answer": "Uma pessoa",
    "explanation": "O Scrum Guide é claro: o Product Owner é uma pessoa, não um comitê. O PO pode representar as necessidades de muitos stakeholders no Product Backlog.",
    "difficulty": "easy"
  },
  {
    "question": "Quem é responsável por criar o plano de como entregar o Incremento durante a Sprint?",
    "options": ["Os Developers", "O Scrum Master", "O Product Owner", "O Scrum Team inteiro"],
    "answer": "Os Developers",
    "explanation": "Os Developers são responsáveis por criar o plano de como transformar os itens selecionados do Product Backlog em um Incremento de valor durante a Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers são responsáveis por toda a estimativa de tamanho/esforço dos itens do Product Backlog.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "As pessoas que realizam o trabalho são as responsáveis pela estimativa. Os Developers são responsáveis por dimensionar os itens do Product Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Qual das seguintes afirmações sobre o Scrum Team é VERDADEIRA?",
    "options": ["É auto-gerenciável e multifuncional", "É gerenciado pelo Scrum Master", "Possui sub-times dedicados (ex: QA, UX)", "Reporta ao Product Owner"],
    "answer": "É auto-gerenciável e multifuncional",
    "explanation": "O Scrum Guide 2020 define que os Scrum Teams são multifuncionais e auto-gerenciáveis (self-managing), o que significa que decidem internamente quem faz o quê, quando e como.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Dentro de um Scrum Team, existem sub-times ou hierarquias.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide afirma explicitamente que não existem sub-times ou hierarquias dentro de um Scrum Team. É uma unidade coesa de profissionais focados em um objetivo de cada vez.",
    "difficulty": "easy"
  },
  {
    "question": "O Scrum Team deve ter um papel de 'testador' ou 'analista de negócios' dedicado?",
    "options": ["Não, o Scrum não reconhece títulos além de Developer, PO e SM", "Sim, é recomendado ter papéis especializados", "Sim, o Scrum Master define os sub-papéis", "Depende da organização"],
    "answer": "Não, o Scrum não reconhece títulos além de Developer, PO e SM",
    "explanation": "O Scrum não reconhece títulos para os Developers além de Developer, independentemente do trabalho realizado. Não há exceções a essa regra.",
    "difficulty": "medium"
  },
  {
    "question": "Se alguém deseja alterar um item no Product Backlog, quem deve convencer?",
    "options": ["O Product Owner", "O Scrum Master", "Os Developers", "Os Stakeholders"],
    "answer": "O Product Owner",
    "explanation": "Para que o Product Backlog seja alterado, o Product Owner precisa ser convencido. Ele é a única pessoa responsável por gerenciar o Product Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Master pode também ser um Developer no Scrum Team.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide não proíbe isso. Na prática, o Scrum Master pode contribuir com trabalho técnico se necessário, embora deva priorizar suas responsabilidades como SM.",
    "difficulty": "hard"
  },
  {
    "question": "Quem decide quantos itens do Product Backlog são selecionados para a Sprint?",
    "options": ["Os Developers", "O Product Owner", "O Scrum Master", "O cliente"],
    "answer": "Os Developers",
    "explanation": "Somente os Developers podem avaliar o que é possível realizar na Sprint e, portanto, são eles que selecionam quantos itens do Product Backlog entram no Sprint Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "O que o Scrum Master faz quando um impedimento é identificado?",
    "options": ["Trabalha para remover o impedimento ou ajuda o time a resolvê-lo", "Escala imediatamente para a gerência", "Adiciona ao Product Backlog", "Ignora se não for crítico"],
    "answer": "Trabalha para remover o impedimento ou ajuda o time a resolvê-lo",
    "explanation": "O Scrum Master causa a remoção de impedimentos ao progresso do Scrum Team. Isso pode envolver resolver diretamente ou facilitar que outros resolvam.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner pode participar da Daily Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Daily Scrum é para os Developers. Porém, se o Product Owner está trabalhando ativamente em itens do Sprint Backlog, ele participa como Developer nesse contexto.",
    "difficulty": "hard"
  },
  {
    "question": "Qual é a principal responsabilidade dos Developers no Scrum?",
    "options": ["Criar qualquer aspecto de um Incremento utilizável a cada Sprint", "Seguir as instruções do Scrum Master", "Documentar os requisitos", "Reportar progresso ao Product Owner diariamente"],
    "answer": "Criar qualquer aspecto de um Incremento utilizável a cada Sprint",
    "explanation": "Os Developers são as pessoas do Scrum Team comprometidas em criar qualquer aspecto de um Incremento utilizável a cada Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "The Scrum Master serve ao Scrum Team de qual forma?",
    "options": ["Todas as alternativas", "Orientando os membros em auto-gerenciamento e multifuncionalidade", "Ajudando o Scrum Team a se concentrar na criação de Incrementos de alto valor que atendem à Definição de Pronto", "Causando a remoção de impedimentos ao progresso do Scrum Team"],
    "answer": "Todas as alternativas",
    "explanation": "O Scrum Master serve ao Scrum Team de diversas maneiras conforme listado no Scrum Guide, incluindo orientação, facilitação e remoção de impedimentos.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner deve estar presente em todas as Daily Scrums.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "A Daily Scrum é um evento para os Developers. O Product Owner não precisa estar presente, a menos que esteja atuando como Developer em itens do Sprint Backlog.",
    "difficulty": "easy"
  },
  {
    "question": "Quem é responsável por garantir que os eventos Scrum ocorram e sejam positivos, produtivos e dentro do time-box?",
    "options": ["O Scrum Master", "O Product Owner", "Os Developers", "O gerente funcional"],
    "answer": "O Scrum Master",
    "explanation": "O Scrum Master garante que todos os eventos Scrum ocorram e sejam positivos, produtivos e dentro do time-box estabelecido.",
    "difficulty": "easy"
  },
  {
    "question": "Qual afirmação sobre o Product Owner e stakeholders é VERDADEIRA?",
    "options": ["O PO pode representar as necessidades de muitos stakeholders no Product Backlog", "Os stakeholders definem a prioridade do Product Backlog", "Os stakeholders participam da Sprint Planning", "Os stakeholders aprovam os itens do Sprint Backlog"],
    "answer": "O PO pode representar as necessidades de muitos stakeholders no Product Backlog",
    "explanation": "O Product Owner pode representar as necessidades de muitos stakeholders no Product Backlog. Quem deseja alterar o Backlog deve tentar convencer o Product Owner.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers devem ser multifuncionais, possuindo todas as habilidades necessárias para criar um Incremento.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide 2020 define que o Scrum Team é multifuncional, significando que os membros possuem todas as habilidades necessárias para criar valor a cada Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "Se um Developer não consegue completar seu trabalho na Sprint, quem decide o que fazer?",
    "options": ["Os Developers se auto-gerenciam para resolver a situação", "O Scrum Master reatribui as tarefas", "O Product Owner remove itens do Sprint Backlog", "O trabalho é automaticamente movido para a próxima Sprint"],
    "answer": "Os Developers se auto-gerenciam para resolver a situação",
    "explanation": "Os Developers são auto-gerenciáveis. Se problemas surgem durante a Sprint, os Developers negociam o escopo do Sprint Backlog com o Product Owner.",
    "difficulty": "medium"
  },
  {
    "question": "O Scrum Master é um gerente de projetos no Scrum?",
    "options": ["Não, o papel de gerente de projetos não existe no Scrum", "Sim, o Scrum Master substitui o gerente de projetos", "Depende da organização", "Sim, mas com responsabilidades limitadas"],
    "answer": "Não, o papel de gerente de projetos não existe no Scrum",
    "explanation": "O Scrum não possui o papel de gerente de projetos. O Scrum Master é um líder servidor que ajuda todos a entender a teoria e a prática do Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner é a única pessoa que pode ordenar o Product Backlog.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Product Owner é a única pessoa responsável pela ordenação do Product Backlog. Embora possa delegar o trabalho, a responsabilidade final permanece com o PO.",
    "difficulty": "easy"
  },
  {
    "question": "O que significa 'auto-gerenciável' (self-managing) no contexto do Scrum?",
    "options": ["O Scrum Team decide internamente quem faz o quê, quando e como", "O time não precisa de um Scrum Master", "Cada membro trabalha de forma independente", "O time define seus próprios salários"],
    "answer": "O Scrum Team decide internamente quem faz o quê, quando e como",
    "explanation": "Auto-gerenciável significa que o Scrum Team escolhe internamente quem faz o quê, quando e como. Ninguém de fora diz ao Scrum Team como transformar itens do Product Backlog em Incrementos de valor.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Master deve fazer coaching tanto ao Scrum Team quanto à organização.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide descreve que o Scrum Master serve ao Scrum Team, ao Product Owner e à organização, fazendo coaching e facilitando a adoção do Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "O que acontece se o Product Owner e os Developers não conseguirem chegar a um acordo sobre o que incluir na Sprint?",
    "options": ["Os Developers selecionam o que acham possível fazer e a Sprint inicia", "O Scrum Master decide o conteúdo da Sprint", "A Sprint é cancelada", "O conflito é escalado para a gerência"],
    "answer": "Os Developers selecionam o que acham possível fazer e a Sprint inicia",
    "explanation": "Os Developers são os únicos que podem avaliar o que é possível realizar. Se houver desacordo, eles selecionam o que acreditam ser factível na Sprint.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: Um Scrum Team pode ter mais de um Product Owner.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide define que o Product Owner é uma pessoa, não um comitê. Cada Scrum Team tem exatamente um Product Owner.",
    "difficulty": "easy"
  },
  {
    "question": "Quais são os cinco eventos do Scrum?",
    "options": ["Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective", "Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective, Refinamento", "Kickoff, Daily Standup, Demo, Retrospectiva, Planning", "Sprint, Planning, Standup, Review, Release"],
    "answer": "Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective",
    "explanation": "Os cinco eventos formais do Scrum são: a Sprint (que contém todos os outros), Sprint Planning, Daily Scrum, Sprint Review e Sprint Retrospective.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint é um contêiner para todos os outros eventos do Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Sprint é um contêiner para todos os outros eventos. Cada evento no Scrum é uma oportunidade formal para inspecionar e adaptar os artefatos Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "O que acontece com o trabalho não concluído ao final de uma Sprint?",
    "options": ["Retorna ao Product Backlog para repriorização pelo Product Owner", "É automaticamente incluído na próxima Sprint", "É descartado", "É entregue como está"],
    "answer": "Retorna ao Product Backlog para repriorização pelo Product Owner",
    "explanation": "Itens não concluídos retornam ao Product Backlog. O Product Owner decide sua prioridade para futuras Sprints.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Uma nova Sprint começa imediatamente após a conclusão da Sprint anterior.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que uma nova Sprint começa imediatamente após a conclusão da Sprint anterior. Não há intervalos entre Sprints.",
    "difficulty": "easy"
  },
  {
    "question": "Durante a Sprint, o que NÃO deve acontecer?",
    "options": ["Mudanças que coloquem em risco a Meta da Sprint", "Refinamento do Product Backlog", "Comunicação com stakeholders", "Adaptação do plano de trabalho"],
    "answer": "Mudanças que coloquem em risco a Meta da Sprint",
    "explanation": "O Scrum Guide afirma que durante a Sprint: nenhuma mudança é feita que coloque em risco a Meta da Sprint; a qualidade não diminui; e o Product Backlog é refinado conforme necessário.",
    "difficulty": "medium"
  },
  {
    "question": "Qual dos seguintes é um formato válido para a Daily Scrum?",
    "options": ["Qualquer formato que os Developers escolherem, desde que foque no progresso em direção à Meta da Sprint", "Obrigatoriamente: O que fiz ontem? O que farei hoje? Quais impedimentos?", "Cada Developer lê seu relatório de status", "O Scrum Master conduz uma reunião de status"],
    "answer": "Qualquer formato que os Developers escolherem, desde que foque no progresso em direção à Meta da Sprint",
    "explanation": "Os Developers podem selecionar qualquer estrutura e técnicas que quiserem para a Daily Scrum, desde que foque no progresso em direção à Meta da Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A Daily Scrum deve sempre seguir o formato de três perguntas (O que fiz? O que farei? Impedimentos?).",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide 2020 não prescreve um formato específico para a Daily Scrum. Os Developers escolhem qualquer estrutura e técnica, desde que foque no progresso em direção à Meta da Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Onde a Daily Scrum deve ser realizada?",
    "options": ["No mesmo horário e local todos os dias úteis da Sprint para reduzir complexidade", "Em uma sala de reunião formal", "Apenas presencialmente", "Apenas virtualmente"],
    "answer": "No mesmo horário e local todos os dias úteis da Sprint para reduzir complexidade",
    "explanation": "A Daily Scrum é realizada no mesmo horário e local todos os dias úteis da Sprint para reduzir a complexidade.",
    "difficulty": "easy"
  },
  {
    "question": "Quem participa da Sprint Review?",
    "options": ["O Scrum Team e stakeholders-chave convidados pelo Product Owner", "Apenas os Developers", "Apenas o Scrum Team", "Todo mundo da organização"],
    "answer": "O Scrum Team e stakeholders-chave convidados pelo Product Owner",
    "explanation": "Na Sprint Review, o Scrum Team apresenta os resultados do trabalho para stakeholders-chave e o progresso em direção à Meta do Produto é discutido.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Review é apenas uma apresentação/demonstração do trabalho feito.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "A Sprint Review é uma sessão de trabalho, não uma mera apresentação. O Scrum Team e stakeholders revisam o que foi realizado e discutem o que fazer a seguir. O Product Backlog pode ser ajustado.",
    "difficulty": "medium"
  },
  {
    "question": "O que é discutido na Sprint Retrospective?",
    "options": ["Como a Sprint foi em relação a pessoas, interações, processos, ferramentas e Definição de Pronto", "Apenas os bugs encontrados na Sprint", "O desempenho individual de cada Developer", "Os requisitos da próxima Sprint"],
    "answer": "Como a Sprint foi em relação a pessoas, interações, processos, ferramentas e Definição de Pronto",
    "explanation": "O Scrum Team inspeciona como a última Sprint foi em relação a indivíduos, interações, processos, ferramentas e sua Definição de Pronto.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Retrospective é o último evento da Sprint.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Sprint Retrospective conclui a Sprint. É o último evento antes de uma nova Sprint começar.",
    "difficulty": "easy"
  },
  {
    "question": "Qual evento Scrum resulta na criação da Meta da Sprint?",
    "options": ["Sprint Planning", "Daily Scrum", "Sprint Review", "Sprint Retrospective"],
    "answer": "Sprint Planning",
    "explanation": "A Meta da Sprint é definida durante a Sprint Planning. Ela é o único objetivo da Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O refinamento do Product Backlog é um evento formal do Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O refinamento do Product Backlog é uma atividade contínua, não um evento formal do Scrum. É o ato de decompor e definir melhor os itens do Product Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Durante a Sprint Planning, quem define a Meta da Sprint?",
    "options": ["O Scrum Team inteiro", "O Product Owner sozinho", "O Scrum Master", "Os Developers"],
    "answer": "O Scrum Team inteiro",
    "explanation": "A Meta da Sprint é criada durante a Sprint Planning e depois adicionada ao Sprint Backlog. Todo o Scrum Team colabora para definir por que a Sprint é valiosa.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers podem convidar outras pessoas para a Daily Scrum para obter conselhos técnicos.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Embora a Daily Scrum seja para os Developers, eles podem convidar outras pessoas se acharem útil, desde que o evento continue focado e dentro do time-box.",
    "difficulty": "hard"
  },
  {
    "question": "Qual é o resultado da Sprint Review?",
    "options": ["Um Product Backlog possivelmente revisado que define prováveis itens para a próxima Sprint", "Um relatório de status aprovado pela gerência", "Uma lista de bugs para corrigir", "A aprovação formal do Incremento"],
    "answer": "Um Product Backlog possivelmente revisado que define prováveis itens para a próxima Sprint",
    "explanation": "O resultado da Sprint Review é um Product Backlog revisado que define os prováveis itens do Product Backlog para a próxima Sprint Planning.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: É possível ter Sprints de durações diferentes dentro do mesmo projeto.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que Sprints têm duração fixa de um mês ou menos, mas não exige que todas as Sprints tenham a mesma duração. Na prática, manter consistência é recomendado.",
    "difficulty": "hard"
  },
  {
    "question": "O que deve ser feito com melhorias identificadas na Sprint Retrospective?",
    "options": ["As mais impactantes são abordadas o mais rapidamente possível, podendo ser adicionadas ao Sprint Backlog da próxima Sprint", "São documentadas e esquecidas", "São adicionadas ao Product Backlog automaticamente", "São reportadas à gerência"],
    "answer": "As mais impactantes são abordadas o mais rapidamente possível, podendo ser adicionadas ao Sprint Backlog da próxima Sprint",
    "explanation": "O Scrum Team identifica as melhorias mais úteis e as mais impactantes são abordadas o mais rápido possível. Podem até ser adicionadas ao Sprint Backlog da próxima Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O escopo de uma Sprint pode ser renegociado entre PO e Developers durante a Sprint.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "À medida que mais é aprendido durante a Sprint, o escopo pode ser esclarecido e renegociado entre o Product Owner e os Developers. A Meta da Sprint, porém, não muda.",
    "difficulty": "medium"
  },
  {
    "question": "Qual afirmação sobre a Meta da Sprint é CORRETA?",
    "options": ["É definida na Sprint Planning e não pode ser alterada durante a Sprint", "Pode ser mudada a qualquer momento pelo Product Owner", "É opcional e pode não existir", "É definida pelo Scrum Master"],
    "answer": "É definida na Sprint Planning e não pode ser alterada durante a Sprint",
    "explanation": "A Meta da Sprint é criada durante a Sprint Planning e é fixa durante a Sprint. Se a Meta da Sprint se tornar obsoleta, a Sprint pode ser cancelada pelo Product Owner.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Cada evento Scrum é uma oportunidade formal para inspecionar e adaptar artefatos Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que cada evento é uma oportunidade formal para inspecionar e adaptar artefatos. Esses eventos são projetados para provocar mudanças.",
    "difficulty": "easy"
  },
  {
    "question": "Se a Daily Scrum determina que ajustes são necessários, quando os Developers devem se adaptar?",
    "options": ["O mais rapidamente possível, idealmente no mesmo dia", "Na próxima Sprint Planning", "Na Sprint Retrospective", "No final da Sprint"],
    "answer": "O mais rapidamente possível, idealmente no mesmo dia",
    "explanation": "Se a Daily Scrum identifica que o plano precisa de ajustes, os Developers devem adaptar o mais rápido possível, não esperando por outros eventos.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Review acontece antes da Sprint Retrospective.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A ordem dos eventos dentro da Sprint é: Sprint Planning → Daily Scrums → Sprint Review → Sprint Retrospective.",
    "difficulty": "easy"
  },
  {
    "question": "Qual evento fornece a principal oportunidade para o Scrum Team inspecionar a si mesmo e crear um plano de melhorias?",
    "options": ["Sprint Retrospective", "Sprint Review", "Daily Scrum", "Sprint Planning"],
    "answer": "Sprint Retrospective",
    "explanation": "A Sprint Retrospective é onde o Scrum Team planeja maneiras de aumentar a qualidade e a eficácia, inspecionando a si mesmo.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Planning é limitada a 8 horas para uma Sprint de um mês, mas pode ser mais curta para Sprints mais curtas.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Sprint Planning tem time-box de no máximo 8 horas para uma Sprint de um mês. Para Sprints mais curtas, o evento é geralmente mais curto proporcionalmente.",
    "difficulty": "easy"
  },
  {
    "question": "Quem participa da Sprint Retrospective?",
    "options": ["O Scrum Team inteiro (Developers, PO e SM)", "Apenas os Developers", "Developers e Scrum Master apenas", "Developers e Product Owner apenas"],
    "answer": "O Scrum Team inteiro (Developers, PO e SM)",
    "explanation": "A Sprint Retrospective é para o Scrum Team inteiro, incluindo Developers, Product Owner e Scrum Master.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Durante a Sprint, nenhuma mudança que afete a Meta da Sprint deve ser feita.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma: 'Nenhuma mudança é feita que coloque em risco a Meta da Sprint'. A qualidade não diminui e o Product Backlog é refinado conforme necessário.",
    "difficulty": "medium"
  },
  {
    "question": "Em que situação uma Sprint pode ser cancelada?",
    "options": ["Quando a Meta da Sprint se torna obsoleta", "Quando os Developers não conseguem completar o trabalho", "Quando os stakeholders mudam de ideia", "Sprints nunca podem ser canceladas"],
    "answer": "Quando a Meta da Sprint se torna obsoleta",
    "explanation": "Uma Sprint pode ser cancelada se a Meta da Sprint se tornar obsoleta. Apenas o Product Owner tem autoridade para cancelar a Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Quais são os três artefatos do Scrum?",
    "options": ["Product Backlog, Sprint Backlog e Incremento", "Product Backlog, Burndown Chart e Release Plan", "Sprint Backlog, Kanban Board e Velocity Chart", "Backlog, Board e Relatório"],
    "answer": "Product Backlog, Sprint Backlog e Incremento",
    "explanation": "Os três artefatos do Scrum são: Product Backlog, Sprint Backlog e Incremento. Cada artefato contém um compromisso para garantir transparência e foco.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Burndown Chart é um artefato oficial do Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Burndown Chart NÃO é mencionado no Scrum Guide. É uma ferramenta complementar útil, mas não faz parte dos artefatos formais do Scrum.",
    "difficulty": "medium"
  },
  {
    "question": "O que é a Meta do Produto (Product Goal)?",
    "options": ["O estado futuro do produto que serve como alvo para o Scrum Team planejar", "O escopo total do projeto", "A visão de negócio da empresa", "O plano de release do produto"],
    "answer": "O estado futuro do produto que serve como alvo para o Scrum Team planejar",
    "explanation": "A Meta do Produto descreve um estado futuro do produto e serve como alvo para o Scrum Team planejar. Está no Product Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Um Scrum Team pode perseguir múltiplas Metas de Produto simultaneamente.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide afirma que um Scrum Team deve perseguir um objetivo de cada vez. Antes de assumir um próximo, o Scrum Team deve completar ou abandonar o atual.",
    "difficulty": "medium"
  },
  {
    "question": "Quem é o dono do Sprint Backlog?",
    "options": ["Os Developers", "O Product Owner", "O Scrum Master", "O Scrum Team inteiro"],
    "answer": "Os Developers",
    "explanation": "O Sprint Backlog é um plano feito por e para os Developers. É uma imagem altamente visível e em tempo real do trabalho que os Developers planejam realizar.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Sprint Backlog é atualizado ao longo da Sprint conforme mais é aprendido.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Sprint Backlog é atualizado ao longo da Sprint conforme mais é aprendido. Deve ter detalhes suficientes para que os Developers possam inspecionar seu progresso na Daily Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "O que NÃO faz parte do Sprint Backlog?",
    "options": ["As métricas de velocidade do time", "A Meta da Sprint", "Os itens do Product Backlog selecionados para a Sprint", "O plano para entregar o Incremento"],
    "answer": "As métricas de velocidade do time",
    "explanation": "O Sprint Backlog é composto pela Meta da Sprint (por quê), os itens selecionados do PB (o quê) e o plano de entrega (como). Velocity não faz parte.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A Definição de Pronto pode ser diferente para diferentes Scrum Teams dentro da mesma organização.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Se a organização não tem um padrão, cada Scrum Team cria sua própria Definição de Pronto. Se for padrão organizacional, todos os times devem segui-lo como mínimo.",
    "difficulty": "hard"
  },
  {
    "question": "Se um item do Product Backlog não atende à Definição de Pronto, o que acontece?",
    "options": ["Não pode ser liberado nem apresentado na Sprint Review como concluído", "É liberado parcialmente", "O Product Owner decide se pode ser entregue", "É movido automaticamente para a próxima Sprint"],
    "answer": "Não pode ser liberado nem apresentado na Sprint Review como concluído",
    "explanation": "Se um item do Product Backlog não atende à Definição de Pronto, ele não pode ser liberado nem apresentado na Sprint Review. Ele retorna ao Product Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Backlog é uma lista fixa que não muda depois do início do projeto.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Product Backlog é uma lista emergente e ordenada. Ele evolui continuamente, sendo refinado à medida que o produto e o ambiente mudam.",
    "difficulty": "easy"
  },
  {
    "question": "O que significa dizer que o Product Backlog é 'emergente'?",
    "options": ["Ele evolui e muda continuamente à medida que mais é aprendido sobre o produto", "Ele surge apenas em emergências", "Ele é criado apenas uma vez no início do projeto", "Ele é visível apenas para o Scrum Team"],
    "answer": "Ele evolui e muda continuamente à medida que mais é aprendido sobre o produto",
    "explanation": "O Product Backlog é emergente, o que significa que nunca está completo. À medida que o produto é usado e ganha valor, o ambiente muda, e o backlog evolui.",
    "difficulty": "easy"
  },
  {
    "question": "O que é refinamento do Product Backlog?",
    "options": ["O ato de decompor e definir melhor os itens do Product Backlog", "Uma cerimônia formal de duas horas", "A priorização feita pelo Scrum Master", "A aprovação dos itens pelos stakeholders"],
    "answer": "O ato de decompor e definir melhor os itens do Product Backlog",
    "explanation": "O refinamento do Product Backlog é o ato de decompor e definir melhor os itens. É uma atividade contínua para adicionar detalhes como descrição, ordem e tamanho.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A Definição de Pronto pode ser modificada pela Sprint Retrospective.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A Sprint Retrospective é o evento onde o Scrum Team pode discutir e adaptar a Definição de Pronto para aumentar a qualidade.",
    "difficulty": "medium"
  },
  {
    "question": "Se múltiplos Scrum Teams trabalham no mesmo produto, quantos Product Backlogs existem?",
    "options": ["Apenas um Product Backlog", "Um por Scrum Team", "Depende da organização", "Um por Sprint"],
    "answer": "Apenas um Product Backlog",
    "explanation": "Existe apenas um Product Backlog por produto, independentemente de quantos Scrum Teams trabalham nele.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Incremento deve ser utilizável, mesmo que o Product Owner decida não liberá-lo.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Incremento deve ser utilizável e atender à Definição de Pronto. A decisão de liberar ou não é separada — o Incremento deve estar pronto independentemente.",
    "difficulty": "medium"
  },
  {
    "question": "Quando um Incremento é entregue aos stakeholders?",
    "options": ["A qualquer momento durante a Sprint, não apenas na Sprint Review", "Apenas na Sprint Review", "Apenas quando toda a Meta do Produto é alcançada", "Apenas com aprovação do Scrum Master"],
    "answer": "A qualquer momento durante a Sprint, não apenas na Sprint Review",
    "explanation": "O Scrum Guide afirma que um Incremento pode ser entregue aos stakeholders antes do final da Sprint. A Sprint Review não deve ser considerada um portão de liberação.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Backlog pode ter itens que nunca serão implementados.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Product Backlog pode conter itens que nunca serão implementados. Como é emergente, itens podem ser removidos ou perder relevância ao longo do tempo.",
    "difficulty": "easy"
  },
  {
    "question": "Quem adiciona itens ao Product Backlog?",
    "options": ["Qualquer pessoa pode sugerir, mas o Product Owner decide o que entra e sua ordem", "Apenas o Product Owner", "Apenas os Developers", "Apenas os stakeholders"],
    "answer": "Qualquer pessoa pode sugerir, mas o Product Owner decide o que entra e sua ordem",
    "explanation": "Qualquer pessoa pode sugerir itens para o Product Backlog. Porém, o Product Owner é o responsável por decidir o que entra e como é ordenado.",
    "difficulty": "medium"
  },
  {
    "question": "A Meta da Sprint pode mudar durante a Sprint?",
    "options": ["Não, a Meta da Sprint é fixa durante toda a Sprint", "Sim, o PO pode alterá-la a qualquer momento", "Sim, se os Developers concordarem", "Sim, na Daily Scrum"],
    "answer": "Não, a Meta da Sprint é fixa durante toda a Sprint",
    "explanation": "A Meta da Sprint não muda durante a Sprint. Se ela se tornar obsoleta, o PO pode cancelar a Sprint, mas não pode alterar a meta vigente.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers se comprometem com a Meta da Sprint, não com os itens específicos do Sprint Backlog.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Os Developers se comprometem com a Meta da Sprint. Os itens específicos podem mudar (escopo negociado), mas a meta permanece fixa como objetivo.",
    "difficulty": "hard"
  },
  {
    "question": "O que deve conter o Product Backlog?",
    "options": ["Tudo que é necessário para melhorar o produto, incluindo funcionalidades, correções, melhorias técnicas e conhecimento a adquirir", "Apenas funcionalidades solicitadas pelo cliente", "Apenas histórias de usuário", "Apenas requisitos aprovados pelo comitê de mudança"],
    "answer": "Tudo que é necessário para melhorar o produto, incluindo funcionalidades, correções, melhorias técnicas e conhecimento a adquirir",
    "explanation": "O Product Backlog é uma lista ordenada e emergente de tudo que é necessário para melhorar o produto. É a única fonte de trabalho do Scrum Team.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers devem aderir à Definição de Pronto ao entregar um Incremento.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Os Developers devem seguir a Definição de Pronto. Se um item não atende à DoD, ele não pode ser considerado um Incremento nem liberado.",
    "difficulty": "easy"
  },
  {
    "question": "Qual artefato fornece transparência e oportunidade de inspeção e adaptação no nível macro do produto?",
    "options": ["O Product Backlog com a Meta do Produto", "O Sprint Backlog", "O Incremento", "O Burndown Chart"],
    "answer": "O Product Backlog com a Meta do Produto",
    "explanation": "O Product Backlog, com seu compromisso de Meta do Produto, oferece transparência sobre a direção futura do produto a nível macro.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: A soma dos Incrementos é apresentada na Sprint Review, apoiando o empirismo.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A soma dos Incrementos é apresentada na Sprint Review, apoiando assim o empirismo. O trabalho não pode ser considerado parte de um Incremento a menos que atenda à Definição de Pronto.",
    "difficulty": "medium"
  },
  {
    "question": "Se a organização tem um padrão de Definição de Pronto, o que o Scrum Team deve fazer?",
    "options": ["Seguir o padrão organizacional como mínimo, podendo adicionar critérios mais rigorosos", "Ignorar e criar sua própria DoD", "Usar apenas para o primeiro produto", "Negociar um acordo intermediário com a gerência"],
    "answer": "Seguir o padrão organizacional como mínimo, podendo adicionar critérios mais rigorosos",
    "explanation": "Se a DoD para um Incremento faz parte dos padrões da organização, todos os Scrum Teams devem segui-la como mínimo. Se não existir, o ST cria uma apropriada.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: Itens do Product Backlog que podem ser 'Prontos' pelos Developers dentro de uma Sprint são considerados prontos para seleção na Sprint Planning.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Itens do Product Backlog que podem ser realizados pelo Scrum Team dentro de uma Sprint são considerados prontos para seleção em um evento de Sprint Planning.",
    "difficulty": "medium"
  },
  {
    "question": "Como o Product Backlog deve ser ordenado?",
    "options": ["O Product Owner decide a ordenação com base no que entrega mais valor", "Por tamanho do item, do menor ao maior", "Por ordem cronológica de criação", "Alfabeticamente"],
    "answer": "O Product Owner decide a ordenação com base no que entrega mais valor",
    "explanation": "O Product Owner ordena o Product Backlog para maximizar o valor entregue pelo Scrum Team. A forma de ordenação é responsabilidade exclusiva do PO.",
    "difficulty": "medium"
  },
  {
    "question": "O que são critérios de aceitação em relação à Definição de Pronto?",
    "options": ["São coisas diferentes: critérios de aceitação são específicos de cada item, a DoD se aplica a todos os Incrementos", "São a mesma coisa", "Critérios de aceitação substituem a DoD", "A DoD contém os critérios de aceitação de cada item"],
    "answer": "São coisas diferentes: critérios de aceitação são específicos de cada item, a DoD se aplica a todos os Incrementos",
    "explanation": "Critérios de aceitação definem quando um item específico do PB está pronto. A Definição de Pronto se aplica ao Incremento como um todo e é um padrão de qualidade universal.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: O Sprint Backlog pertence ao Product Owner.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Sprint Backlog pertence aos Developers. É um plano feito por e para os Developers que fornece uma imagem em tempo real do trabalho da Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "Um stakeholder pede a um Developer para adicionar uma funcionalidade urgente durante a Sprint. O que o Developer deve fazer?",
    "options": ["Direcionar o stakeholder ao Product Owner", "Adicionar imediatamente ao Sprint Backlog", "Consultar o Scrum Master primeiro", "Ignorar a solicitação"],
    "answer": "Direcionar o stakeholder ao Product Owner",
    "explanation": "Qualquer mudança no Product Backlog deve passar pelo Product Owner. Os Developers devem direcionar solicitações de stakeholders ao PO.",
    "difficulty": "medium"
  },
  {
    "question": "O Scrum Master percebe que o time não está seguindo as práticas do Scrum. Qual é a melhor abordagem?",
    "options": ["Fazer coaching e ajudar o time a entender por que as práticas Scrum são importantes", "Reportar o time à gerência", "Forçar o time a seguir o Scrum", "Ignorar e deixar o time se auto-organizar"],
    "answer": "Fazer coaching e ajudar o time a entender por que as práticas Scrum são importantes",
    "explanation": "O Scrum Master é responsável pela eficácia do Scrum Team e deve ajudar todos a entender a teoria e a prática do Scrum, tanto dentro do time quanto na organização.",
    "difficulty": "medium"
  },
  {
    "question": "A Daily Scrum frequentemente ultrapassa 15 minutos. O que o Scrum Master deve fazer?",
    "options": ["Orientar os Developers sobre o propósito da Daily Scrum e ajudá-los a manter o time-box", "Cancelar a Daily Scrum", "Estender o time-box para 30 minutos", "Assumir a condução da reunião"],
    "answer": "Orientar os Developers sobre o propósito da Daily Scrum e ajudá-los a manter o time-box",
    "explanation": "O Scrum Master deve ajudar o time a entender o propósito da Daily Scrum e manter o time-box. Discussões detalhadas podem ocorrer após a Daily Scrum.",
    "difficulty": "medium"
  },
  {
    "question": "No meio da Sprint, os Developers percebem que não conseguirão entregar todos os itens selecionados. O que fazer?",
    "options": ["Os Developers comunicam ao PO e renegociam o escopo do Sprint Backlog, mantendo a Meta da Sprint", "Estendem a Sprint em uma semana", "Entregam tudo incompleto", "Cancelam a Sprint"],
    "answer": "Os Developers comunicam ao PO e renegociam o escopo do Sprint Backlog, mantendo a Meta da Sprint",
    "explanation": "O escopo pode ser renegociado entre Developers e PO durante a Sprint. A Meta da Sprint não muda, mas os itens específicos podem ser ajustados.",
    "difficulty": "medium"
  },
  {
    "question": "A gerência quer adicionar mais dois membros ao Scrum Team de 8 pessoas. Qual deve ser a preocupação?",
    "options": ["O time ficaria com mais de 10 pessoas, o que o Scrum Guide recomenda evitar", "Não há preocupação, quanto mais pessoas melhor", "O Scrum Master deve impedir a entrada", "O Product Owner deve aprovar"],
    "answer": "O time ficaria com mais de 10 pessoas, o que o Scrum Guide recomenda evitar",
    "explanation": "O Scrum Guide recomenda que o Scrum Team tenha 10 ou menos pessoas. Times maiores devem considerar reorganizar-se em múltiplos Scrum Teams coesos.",
    "difficulty": "medium"
  },
  {
    "question": "Um Product Owner está ocupado demais e raramente comparece aos eventos Scrum. O que o Scrum Master deve fazer?",
    "options": ["Fazer coaching com o PO sobre a importância de sua participação e responsabilidades no Scrum", "Substituir o PO nos eventos", "Pedir aos Developers para assumirem as responsabilidades do PO", "Reportar o PO à gerência"],
    "answer": "Fazer coaching com o PO sobre a importância de sua participação e responsabilidades no Scrum",
    "explanation": "O Scrum Master serve ao PO ajudando-o a entender suas responsabilidades. A participação do PO nos eventos Scrum é fundamental para o sucesso do time.",
    "difficulty": "medium"
  },
  {
    "question": "Os Developers querem mudar a duração da Sprint de 2 semanas para 3 semanas. Quem decide isso?",
    "options": ["O Scrum Team, pois é uma decisão coletiva sobre como trabalham", "Apenas o Scrum Master", "Apenas o Product Owner", "A gerência"],
    "answer": "O Scrum Team, pois é uma decisão coletiva sobre como trabalham",
    "explanation": "A duração da Sprint é uma decisão do Scrum Team. O Scrum Guide diz que Sprints mais curtas geram ciclos de feedback mais frequentes.",
    "difficulty": "medium"
  },
  {
    "question": "Um Developer terminou todo o seu trabalho antes do fim da Sprint. O que ele deve fazer?",
    "options": ["Ajudar outros Developers ou pegar mais trabalho do Sprint Backlog", "Esperar a Sprint terminar", "Começar a trabalhar em itens da próxima Sprint", "Pedir folga ao Scrum Master"],
    "answer": "Ajudar outros Developers ou pegar mais trabalho do Sprint Backlog",
    "explanation": "Os Developers são auto-gerenciáveis. Se um Developer termina seu trabalho, ele deve colaborar com outros ou pegar mais itens do Sprint Backlog para atingir a Meta da Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "Os stakeholders reclamam que não sabem no que o Scrum Team está trabalhando. Qual evento resolve isso?",
    "options": ["Sprint Review", "Daily Scrum", "Sprint Retrospective", "Sprint Planning"],
    "answer": "Sprint Review",
    "explanation": "A Sprint Review é o evento onde o Scrum Team apresenta resultados aos stakeholders e discute progresso e próximos passos. Promove transparência.",
    "difficulty": "easy"
  },
  {
    "question": "O Product Owner quer liberar o Incremento para produção no meio da Sprint. Isso é permitido?",
    "options": ["Sim, um Incremento pode ser liberado a qualquer momento, não apenas na Sprint Review", "Não, só pode ser liberado na Sprint Review", "Não, só pode ser liberado ao final da Sprint", "Apenas se o Scrum Master aprovar"],
    "answer": "Sim, um Incremento pode ser liberado a qualquer momento, não apenas na Sprint Review",
    "explanation": "O Scrum Guide afirma que a Sprint Review não é um portão de liberação (release gate). Incrementos podem ser entregues a qualquer momento durante a Sprint.",
    "difficulty": "hard"
  },
  {
    "question": "O que o Scrum Master deve fazer quando a organização não entende o Scrum?",
    "options": ["Liderar, treinar e orientar a organização na adoção do Scrum", "Focar apenas no Scrum Team e ignorar a organização", "Pedir que a gerência faça a adoção", "Escalar para um coach externo"],
    "answer": "Liderar, treinar e orientar a organização na adoção do Scrum",
    "explanation": "O Scrum Master serve à organização liderando, treinando e orientando na adoção do Scrum, ajudando a entender a abordagem empírica.",
    "difficulty": "easy"
  },
  {
    "question": "Os Developers querem usar uma nova ferramenta para melhorar a qualidade. Quando devem discutir isso?",
    "options": ["Na Sprint Retrospective", "Na Sprint Planning", "Na Daily Scrum", "Na Sprint Review"],
    "answer": "Na Sprint Retrospective",
    "explanation": "A Sprint Retrospective é o evento onde o Scrum Team discute melhorias em processos, ferramentas e práticas para aumentar qualidade e eficácia.",
    "difficulty": "easy"
  },
  {
    "question": "Um gerente funcional quer atribuir tarefas específicas aos Developers. O Scrum Master deve:",
    "options": ["Explicar que os Developers são auto-gerenciáveis e decidem internamente quem faz o quê", "Permitir que o gerente atribua tarefas", "Mediar entre o gerente e os Developers", "Ignorar a situação"],
    "answer": "Explicar que os Developers são auto-gerenciáveis e decidem internamente quem faz o quê",
    "explanation": "No Scrum, os Developers são auto-gerenciáveis. Ninguém de fora do Scrum Team diz aos Developers como transformar itens do PB em Incrementos de valor.",
    "difficulty": "medium"
  },
  {
    "question": "O PO quer adicionar novos itens ao Sprint Backlog no meio da Sprint. Isso é correto?",
    "options": ["Os Developers podem aceitar trabalho adicional se acreditarem que podem completá-lo sem comprometer a Meta da Sprint", "Sim, o PO pode adicionar o que quiser a qualquer momento", "Não, o Sprint Backlog é imutável", "Apenas o Scrum Master pode aprovar mudanças"],
    "answer": "Os Developers podem aceitar trabalho adicional se acreditarem que podem completá-lo sem comprometer a Meta da Sprint",
    "explanation": "O escopo pode ser renegociado entre PO e Developers durante a Sprint. Mudanças não devem comprometer a Meta da Sprint.",
    "difficulty": "hard"
  },
  {
    "question": "Dois Scrum Teams trabalham no mesmo produto. Cada um tem seu próprio Product Backlog?",
    "options": ["Não, existe apenas um Product Backlog por produto", "Sim, cada time deve ter seu próprio backlog", "Depende do tamanho do produto", "O Scrum Master decide"],
    "answer": "Não, existe apenas um Product Backlog por produto",
    "explanation": "Há apenas um Product Backlog por produto, compartilhado por todos os Scrum Teams. Cada um pode ter um Product Owner ou compartilhar.",
    "difficulty": "medium"
  },
  {
    "question": "O time está insatisfeito com a Definição de Pronto atual. Quando podem alterá-la?",
    "options": ["Durante a Sprint Retrospective", "A qualquer momento durante a Sprint", "Apenas no início de um novo projeto", "Nunca, é definida uma única vez"],
    "answer": "Durante a Sprint Retrospective",
    "explanation": "A Sprint Retrospective é o evento apropriado para discutir e adaptar a Definição de Pronto. O time pode torná-la mais rigorosa para aumentar a qualidade.",
    "difficulty": "medium"
  },
  {
    "question": "Um Developer está consistentemente atrasando entregas. Quem é responsável por resolver isso?",
    "options": ["Os Developers como um grupo auto-gerenciável", "O Scrum Master diretamente", "O Product Owner", "O gerente de RH"],
    "answer": "Os Developers como um grupo auto-gerenciável",
    "explanation": "Como o Scrum Team é auto-gerenciável, os Developers são coletivamente responsáveis por gerenciar seu próprio trabalho e resolver questões internas.",
    "difficulty": "medium"
  },
  {
    "question": "O Product Owner está insatisfeito com a qualidade do Incremento entregue. Qual é a melhor ação?",
    "options": ["Revisar e potencialmente fortalecer a Definição de Pronto na Sprint Retrospective", "Culpar os Developers", "Contratar testadores adicionais", "Estender a Sprint para melhorar a qualidade"],
    "answer": "Revisar e potencialmente fortalecer a Definição de Pronto na Sprint Retrospective",
    "explanation": "A Definição de Pronto pode ser fortalecida na Sprint Retrospective para garantir maior qualidade. Isso é uma adaptação legítima dentro do Scrum.",
    "difficulty": "hard"
  },
  {
    "question": "A Sprint Retrospective acontece e nenhum problema significativo é identificado. Isso é normal?",
    "options": ["O time deve buscar melhorias continuamente, mesmo quando as coisas vão bem", "Sim, não há necessidade de mudanças", "A Retrospective pode ser cancelada neste caso", "O Scrum Master deve inventar problemas"],
    "answer": "O time deve buscar melhorias continuamente, mesmo quando as coisas vão bem",
    "explanation": "Mesmo quando as coisas vão bem, sempre há espaço para melhorar. O Scrum é baseado em melhoria contínua (kaizen). O time deve sempre buscar evoluir.",
    "difficulty": "medium"
  },
  {
    "question": "O Scrum Team entregou o Incremento, mas os stakeholders não compareceram à Sprint Review. O que fazer?",
    "options": ["Realizar a Sprint Review mesmo assim com o Scrum Team e buscar feedback dos stakeholders de outra forma", "Cancelar a Sprint Review", "Adiar para quando os stakeholders puderem vir", "Pular diretamente para a Sprint Retrospective"],
    "answer": "Realizar a Sprint Review mesmo assim com o Scrum Team e buscar feedback dos stakeholders de outra forma",
    "explanation": "A Sprint Review deve ocorrer como evento formal da Sprint. O Scrum Team pode buscar feedback dos stakeholders por outros meios se necessário.",
    "difficulty": "hard"
  },
  {
    "question": "Uma empresa quer implementar Scrum, mas sem Daily Scrums para 'economizar tempo'. O que o SM deve explicar?",
    "options": ["Todos os eventos Scrum são obrigatórios e servem aos pilares empíricos de Transparência, Inspeção e Adaptação", "A Daily Scrum é opcional e pode ser removida", "É possível substituir por relatórios de status por email", "Pode-se fazer a Daily Scrum apenas 3 vezes por semana"],
    "answer": "Todos os eventos Scrum são obrigatórios e servem aos pilares empíricos de Transparência, Inspeção e Adaptação",
    "explanation": "O Scrum Guide afirma que os eventos existem para criar regularidade e minimizar a necessidade de reuniões não definidas no Scrum. Remover eventos enfraquece o empirismo.",
    "difficulty": "medium"
  },
  {
    "question": "Na Sprint Planning, o PO apresenta itens prioritários, mas os Developers dizem que não têm capacidade. O que acontece?",
    "options": ["Os Developers selecionam apenas o que consideram possível fazer na Sprint", "O PO força mais itens no Sprint Backlog", "A Sprint é cancelada", "O Scrum Master decide a quantidade"],
    "answer": "Os Developers selecionam apenas o que consideram possível fazer na Sprint",
    "explanation": "Somente os Developers avaliam o que é possível realizar na Sprint. Se não há capacidade para todos os itens desejados pelo PO, o escopo é ajustado.",
    "difficulty": "medium"
  },
  {
    "question": "O CEO da empresa quer participar da Daily Scrum todos os dias. Isso é permitido?",
    "options": ["A Daily Scrum é para os Developers; outras pessoas podem estar presentes mas não devem perturbar o evento", "Sim, qualquer pessoa pode participar ativamente", "Não, é proibido qualquer pessoa de fora", "Apenas com aprovação do Scrum Master"],
    "answer": "A Daily Scrum é para os Developers; outras pessoas podem estar presentes mas não devem perturbar o evento",
    "explanation": "A Daily Scrum é para os Developers. Embora outros possam estar presentes, eles não devem transformar o evento em uma reunião de status ou perturbar seu foco.",
    "difficulty": "hard"
  },
  {
    "question": "Os Developers querem convidar um expert técnico externo para a Sprint Planning. Isso é possível?",
    "options": ["Sim, o Scrum Team pode convidar pessoas para dar conselhos conforme necessário", "Não, apenas o Scrum Team pode participar", "Apenas com aprovação do PO", "Apenas se o SM facilitar"],
    "answer": "Sim, o Scrum Team pode convidar pessoas para dar conselhos conforme necessário",
    "explanation": "O Scrum Guide permite que o Scrum Team convide pessoas para fornecer conselhos durante a Sprint Planning, como experts técnicos ou stakeholders relevantes.",
    "difficulty": "medium"
  },
  {
    "question": "O Scrum Team recebe uma reclamação de um cliente em produção durante a Sprint. Quem decide a prioridade da correção?",
    "options": ["O Product Owner decide a prioridade no Product Backlog", "Os Developers imediatamente corrigem", "O Scrum Master escala para a gerência", "O cliente define a prioridade"],
    "answer": "O Product Owner decide a prioridade no Product Backlog",
    "explanation": "O Product Owner é responsável pela ordenação do Product Backlog e decide a prioridade de qualquer item, incluindo correções urgentes.",
    "difficulty": "medium"
  },
  {
    "question": "A Sprint terminou e há funcionalidades 90% completas. Elas podem ser apresentadas na Sprint Review?",
    "options": ["Não como trabalho concluído — apenas Incrementos que atendem à Definição de Pronto podem ser apresentados como prontos", "Sim, qualquer trabalho feito pode ser apresentado como concluído", "Sim, 90% é bom o suficiente", "O PO decide se é apresentável"],
    "answer": "Não como trabalho concluído — apenas Incrementos que atendem à Definição de Pronto podem ser apresentados como prontos",
    "explanation": "Itens que não atendem à Definição de Pronto não podem ser considerados como Incremento concluído. O progresso pode ser discutido, mas não apresentado como pronto.",
    "difficulty": "hard"
  },
  {
    "question": "O Scrum Master nota que os Developers têm medo de levantar problemas nas Retrospectives. O que fazer?",
    "options": ["Criar um ambiente seguro e de confiança onde todos se sintam confortáveis para falar", "Ignorar, pois é problema dos Developers", "Cancelar as Retrospectives", "Fazer as Retrospectives individualmente"],
    "answer": "Criar um ambiente seguro e de confiança onde todos se sintam confortáveis para falar",
    "explanation": "O Scrum Master deve promover um ambiente seguro (psicologicamente seguro) baseado nos valores do Scrum (abertura, respeito, coragem) para que o time melhore continuamente.",
    "difficulty": "medium"
  },
  {
    "question": "A organização quer que o Scrum Team use Sprints de 3 meses para reduzir overhead. O Scrum Master deve:",
    "options": ["Explicar que o máximo é um mês e que Sprints mais curtas são recomendadas para feedback mais rápido", "Aceitar, pois a organização decide", "Sugerir Sprints de 2 meses como compromisso", "Implementar e ver se funciona"],
    "answer": "Explicar que o máximo é um mês e que Sprints mais curtas são recomendadas para feedback mais rápido",
    "explanation": "O Scrum Guide define que Sprints têm duração máxima de um mês. Sprints mais longas podem significar riscos maiores e feedback tardio.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum requer o uso de story points para estimar o trabalho.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não menciona story points nem prescreve técnicas de estimativa. O time pode usar qualquer técnica que considere apropriada.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum requer o uso de User Stories.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não menciona User Stories. É uma prática complementar comum, mas não obrigatória no Scrum.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O velocity (velocidade) é uma métrica oficial do Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não menciona velocity. É uma métrica complementar útil para planejamento, mas não faz parte do framework oficial.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Um Scrum Team deve ter um Scrum Master dedicado em tempo integral.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não exige que o SM seja dedicado em tempo integral. Em muitas organizações, o SM pode atuar em mais de um time, embora dedicação total seja ideal.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Guide prescreve que o Product Backlog deve estar no formato de User Stories.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não prescreve nenhum formato para os itens do Product Backlog. User Stories são uma prática popular, mas não obrigatória.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O controle empírico de processos se baseia em três pilares: transparência, inspeção e adaptação.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum é fundamentado no empirismo e no lean thinking. O controle empírico se apoia em transparência, inspeção e adaptação.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Team pode decidir não realizar a Sprint Retrospective se a Sprint foi bem-sucedida.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "Todos os eventos Scrum são obrigatórios. A Sprint Retrospective é essencial para melhoria contínua, mesmo quando a Sprint foi boa.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é um anti-pattern comum da Daily Scrum?",
    "options": ["Transformá-la em uma reunião de status para o Scrum Master", "Focar no progresso em direção à Meta da Sprint", "Os Developers escolherem o formato", "Manter o time-box de 15 minutos"],
    "answer": "Transformá-la em uma reunião de status para o Scrum Master",
    "explanation": "Um anti-pattern comum é tratar a Daily Scrum como relatório de status. Ela deve ser um evento de planejamento dos Developers, não uma prestação de contas.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: No Scrum, o Product Owner pode ser um comitê de pessoas que compartilham a responsabilidade.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide é claro: o Product Owner é uma pessoa, não um comitê. O PO pode representar as necessidades de muitos stakeholders.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Lean thinking é uma das bases do Scrum, junto com o empirismo.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide 2020 afirma que o Scrum é fundamentado no empirismo e no lean thinking. Lean thinking reduz o desperdício e foca no essencial.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é um anti-pattern do Product Owner?",
    "options": ["Delegar todas as decisões sobre o Product Backlog ao time sem fornecer direção", "Comunicar claramente a Meta do Produto", "Ordenar o Product Backlog baseado em valor", "Participar da Sprint Planning"],
    "answer": "Delegar todas as decisões sobre o Product Backlog ao time sem fornecer direção",
    "explanation": "Embora o PO possa delegar trabalho de gerenciamento do PB, abandonar a responsabilidade é um anti-pattern. O PO permanece accountable.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum define que o time deve ter uma fase de teste separada ao final da Sprint.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum não define fases separadas. Os Developers são multifuncionais e o teste é parte integrante da entrega do Incremento conforme a Definição de Pronto.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: É aceitável que a Sprint tenha escopo variável, mas duração fixa (time-boxed).",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "No Scrum, a Sprint tem duração fixa. O escopo pode ser renegociado durante a Sprint conforme mais é aprendido, mas o time-box não muda.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers podem recusar trabalho que não entendem completamente durante a Sprint Planning.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Os Developers selecionam o trabalho que acreditam poder completar. Se um item não é bem compreendido, ele precisa de mais refinamento antes de ser selecionado.",
    "difficulty": "medium"
  },
  {
    "question": "Qual das afirmações sobre Scrum é FALSA?",
    "options": ["O Scrum é um processo completo e comprovado que funciona em todos os cenários", "O Scrum é um framework propositalmente incompleto", "O Scrum é baseado em empirismo", "O Scrum é baseado em lean thinking"],
    "answer": "O Scrum é um processo completo e comprovado que funciona em todos os cenários",
    "explanation": "O Scrum Guide afirma que o Scrum é propositalmente incompleto, definindo apenas as partes necessárias para implementar a teoria Scrum.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Team é responsável por todas as atividades relacionadas ao produto.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Team é responsável por todas as atividades relacionadas ao produto: colaboração com stakeholders, verificação, manutenção, operação, experimentação, pesquisa e desenvolvimento.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum impõe que o time use um quadro Kanban para visualizar o trabalho.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum não impõe ferramentas ou práticas específicas. Kanban boards são complementares e úteis, mas não são exigidos pelo Scrum Guide.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A transparência permite a inspeção, e a inspeção permite a adaptação.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Os pilares se apoiam mutuamente: a transparência torna possível a inspeção, que por sua vez permite a adaptação. Sem transparência, a inspeção é enganosas.",
    "difficulty": "easy"
  },
  {
    "question": "Qual anti-pattern do Scrum Master compromete a auto-gestão do time?",
    "options": ["Atribuir tarefas e tomar decisões técnicas pelos Developers", "Facilitar eventos Scrum", "Remover impedimentos", "Fazer coaching sobre Scrum"],
    "answer": "Atribuir tarefas e tomar decisões técnicas pelos Developers",
    "explanation": "O SM que atribui tarefas ou toma decisões que deveriam ser dos Developers está comprometendo a auto-gestão, que é princípio fundamental do Scrum.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Segundo o Scrum Guide, cada Sprint deve produzir um Incremento liberável (releasable).",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide 2020 afirma que os Developers devem criar um Incremento utilizável a cada Sprint. Mesmo que não seja liberado, deve estar em condição de ser.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A inspeção sem adaptação é considerada inútil no Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A inspeção sem adaptação é considerada inútil. Os eventos Scrum são projetados para provocar mudanças, não apenas para observar.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: É papel do Scrum Master garantir que o Product Backlog esteja refinado antes da Sprint Planning.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O refinamento do Product Backlog é responsabilidade do Scrum Team. O SM pode facilitar, mas não é o responsável direto pelo refinamento.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers podem mudar a composição do Scrum Team durante a Sprint.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "Mudar a composição do Scrum Team durante a Sprint pode impactar negativamente a produtividade e a coesão do time. O Scrum Guide recomenda estabilidade.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner pode decidir não liberar um Incremento mesmo que ele atenda à Definição de Pronto.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Embora o Incremento deva atender à DoD, a decisão de quando e como liberar para os usuários finais é uma decisão de negócios do Product Owner.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Guide recomenda que os Developers se sentem juntos fisicamente.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide 2020 não faz essa recomendação. O Scrum pode ser aplicado em times co-localizados ou distribuídos.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Alterar partes do Scrum sem aplicar todas as suas regras pode mascarar problemas e limitar os benefícios do framework.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que, embora implementar apenas partes do Scrum seja possível, o resultado não é Scrum. Cada elemento serve a um propósito específico.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Master pode remover Developers do Scrum Team que não apresentam bom desempenho.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Master não é gerente de pessoas. Decisões de pessoal cabem à organização. O SM faz coaching e facilita, mas não contrata nem demite.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Uma Sprint sem uma Meta da Sprint definida é aceitável no Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "A Meta da Sprint é obrigatória. Ela é o único objetivo da Sprint e é criada durante a Sprint Planning. Sem ela, o time perde foco e direção.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum pode ser usado em conjunto com outras práticas como XP, Kanban ou DevOps.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum é um framework leve e propositalmente incompleto. Diversas técnicas, metodologias e práticas podem ser utilizadas dentro dele.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: Os Developers devem seguir as decisões técnicas do Scrum Master.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Master não toma decisões técnicas para os Developers. O time é auto-gerenciável e decide internamente como realizar o trabalho.",
    "difficulty": "easy"
  },
  {
    "question": "O Scrum Guide 2020 usa o termo 'auto-organizado' (self-organizing) ou 'auto-gerenciável' (self-managing)?",
    "options": ["Auto-gerenciável (self-managing)", "Auto-organizado (self-organizing)", "Ambos", "Nenhum dos dois"],
    "answer": "Auto-gerenciável (self-managing)",
    "explanation": "O Scrum Guide 2020 mudou de 'self-organizing' para 'self-managing', ampliando o conceito: o time decide não só como organizar o trabalho, mas também quem faz o quê e quando.",
    "difficulty": "hard"
  },
  {
    "question": "Quantas Metas de Produto um Scrum Team persegue simultaneamente?",
    "options": ["Uma", "No máximo duas", "Quantas forem necessárias", "Depende do tamanho do time"],
    "answer": "Uma",
    "explanation": "Um Scrum Team persegue um objetivo (Meta de Produto) de cada vez. Antes de assumir o próximo, deve completar ou abandonar o atual.",
    "difficulty": "medium"
  },
  {
    "question": "Qual é a relação entre Scrum e agilidade (Agile)?",
    "options": ["Scrum é um framework ágil, mas Agile é um conceito mais amplo baseado no Manifesto Ágil", "Scrum e Agile são a mesma coisa", "Scrum é anterior ao Manifesto Ágil e não é considerado ágil", "Agile é parte do Scrum"],
    "answer": "Scrum é um framework ágil, mas Agile é um conceito mais amplo baseado no Manifesto Ágil",
    "explanation": "Scrum é um dos frameworks ágeis mais populares. Agile é uma filosofia mais ampla definida pelo Manifesto Ágil de 2001.",
    "difficulty": "easy"
  },
  {
    "question": "Se os Developers não sabem como fazer algo tecnicamente durante a Sprint, o que devem fazer?",
    "options": ["Criar um 'spike' (pesquisa/exploração) como parte do Sprint Backlog para aprender", "Esperar a próxima Sprint para começar", "Pedir ao Scrum Master para resolver", "Remover o item do Sprint Backlog imediatamente"],
    "answer": "Criar um 'spike' (pesquisa/exploração) como parte do Sprint Backlog para aprender",
    "explanation": "Os Developers podem incluir atividades de pesquisa e aprendizado no plano da Sprint. O Sprint Backlog é um plano vivo que se adapta conforme mais é aprendido.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Guide 2020 removeu a referência 'servant-leader' para o Scrum Master, usando 'true leader' em vez disso.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide 2020 descreve o SM como um 'true leader who serves the Scrum Team and the larger organization', removendo a menção explícita a 'servant-leader'.",
    "difficulty": "hard"
  },
  {
    "question": "Qual das opções descreve melhor o que é empirismo?",
    "options": ["Tomar decisões com base na observação e experiência, utilizando ciclos frequentes de inspeção e adaptação", "Seguir um plano detalhado criado no início", "Usar métricas preditivas para planejar o futuro", "Basear decisões apenas em dados históricos"],
    "answer": "Tomar decisões com base na observação e experiência, utilizando ciclos frequentes de inspeção e adaptação",
    "explanation": "Empirismo significa que o conhecimento vem da experiência e da observação. No Scrum, decisões são baseadas no que é observado, não no que é previsto.",
    "difficulty": "medium"
  },
  {
    "question": "O que significa o princípio lean de 'reduzir desperdício' aplicado ao Scrum?",
    "options": ["Focar no essencial e eliminar atividades que não geram valor", "Reduzir o número de Developers", "Eliminar a documentação completamente", "Cortar custos em todas as áreas"],
    "answer": "Focar no essencial e eliminar atividades que não geram valor",
    "explanation": "Lean thinking no Scrum significa focar no que é essencial para gerar valor e eliminar desperdícios como trabalho desnecessário, esperas e retrabalho.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Múltiplos Scrum Teams trabalhando no mesmo produto devem ter a mesma Definição de Pronto.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Se múltiplos Scrum Teams trabalham no mesmo produto, devem criar e mutuamente definir e estar em conformidade com a mesma Definição de Pronto.",
    "difficulty": "hard"
  },
  {
    "question": "A Meta da Sprint dá flexibilidade em relação a quê?",
    "options": ["Em relação ao trabalho exato necessário para alcançá-la", "Em relação ao prazo da Sprint", "Em relação à Definição de Pronto", "Em relação ao Product Backlog"],
    "answer": "Em relação ao trabalho exato necessário para alcançá-la",
    "explanation": "A Meta da Sprint é o único objetivo da Sprint. Ela cria coerência e foco, mas permite flexibilidade quanto ao trabalho exato necessário para atingi-la.",
    "difficulty": "medium"
  },
  {
    "question": "Em que teoria o Scrum se fundamenta?",
    "options": ["Empirismo e lean thinking", "Gerenciamento de projetos tradicional (waterfall)", "PMBOK e Prince2", "Six Sigma e CMMI"],
    "answer": "Empirismo e lean thinking",
    "explanation": "O Scrum Guide afirma: 'Scrum is founded on empiricism and lean thinking.' Empirismo garante aprendizado por experiência; lean thinking reduz desperdício.",
    "difficulty": "easy"
  },
  {
    "question": "Qual valor do Scrum está relacionado a admitir erros e discutir problemas abertamente?",
    "options": ["Abertura (Openness)", "Coragem (Courage)", "Respeito (Respect)", "Comprometimento (Commitment)"],
    "answer": "Abertura (Openness)",
    "explanation": "Abertura significa que o Scrum Team e stakeholders são transparentes sobre o trabalho e os desafios. Admitir erros e compartilhar problemas reflete esse valor.",
    "difficulty": "medium"
  },
  {
    "question": "Qual valor do Scrum está relacionado a fazer a coisa certa e trabalhar em problemas difíceis?",
    "options": ["Coragem (Courage)", "Foco (Focus)", "Comprometimento (Commitment)", "Respeito (Respect)"],
    "answer": "Coragem (Courage)",
    "explanation": "Coragem significa ter a disposição de fazer a coisa certa e trabalhar em problemas difíceis. Os membros do Scrum Team devem ter coragem para enfrentar desafios.",
    "difficulty": "medium"
  },
  {
    "question": "Qual valor do Scrum se relaciona com o fato de o time se concentrar no trabalho da Sprint e na Meta da Sprint?",
    "options": ["Foco (Focus)", "Comprometimento (Commitment)", "Coragem (Courage)", "Abertura (Openness)"],
    "answer": "Foco (Focus)",
    "explanation": "Foco significa que o Scrum Team se concentra no trabalho da Sprint para fazer o melhor progresso possível em direção à Meta da Sprint.",
    "difficulty": "easy"
  },
  {
    "question": "Quando surgem aspectos de trabalho inesperados durante a Sprint, quem avalia o impacto?",
    "options": ["Os Developers em colaboração com o Product Owner", "O Scrum Master sozinho", "Os stakeholders", "O gerente do projeto"],
    "answer": "Os Developers em colaboração com o Product Owner",
    "explanation": "Quando surge trabalho inesperado, os Developers avaliam o impacto e colaboram com o PO para renegociar o escopo do Sprint Backlog.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Guide prescreve práticas específicas para Engineering Practices (como TDD, pair programming, CI/CD).",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não prescreve práticas de engenharia. O Scrum é propositalmente incompleto e deixa que práticas complementares sejam escolhidas pelo time.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: No Scrum, existe o conceito de 'Sprint 0' para preparação inicial.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide não reconhece 'Sprint 0'. Cada Sprint deve produzir um Incremento. Atividades de setup podem fazer parte da primeira Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: No Scrum Guide 2020, os Developers são chamados de 'Development Team'.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O Scrum Guide 2020 removeu 'Development Team' e usa apenas 'Developers' para eliminar o conceito de 'time dentro de um time' e reforçar que há apenas um Scrum Team.",
    "difficulty": "hard"
  },
  {
    "question": "Quem foi que criou o Scrum?",
    "options": ["Ken Schwaber e Jeff Sutherland", "Martin Fowler e Robert C. Martin", "Mike Cohn e Kent Beck", "Alistair Cockburn e Jim Highsmith"],
    "answer": "Ken Schwaber e Jeff Sutherland",
    "explanation": "O Scrum foi criado por Ken Schwaber e Jeff Sutherland no início dos anos 1990. Ambos são co-autores do Scrum Guide.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: A Sprint Review é um momento de avaliação de desempenho individual.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "A Sprint Review é para inspecionar o resultado da Sprint e determinar adaptações futuras, não para avaliar desempenho individual de membros do time.",
    "difficulty": "easy"
  },
  {
    "question": "Verdadeiro ou Falso: O conceito de 'pronto para desenvolvimento' (ready) é obrigatório no Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Falso",
    "explanation": "O conceito de 'Definition of Ready' não é mencionado no Scrum Guide. É uma prática complementar que alguns times adotam, mas não é obrigatória.",
    "difficulty": "hard"
  },
  {
    "question": "Qual das seguintes opções melhor descreve o papel do Scrum no gerenciamento de risco?",
    "options": ["As Sprints curtas limitam o risco ao custo de no máximo um mês de trabalho", "O Scrum elimina todos os riscos do projeto", "O Scrum não lida com gerenciamento de risco", "Os riscos são gerenciados pelo Scrum Master em um registro de riscos"],
    "answer": "As Sprints curtas limitam o risco ao custo de no máximo um mês de trabalho",
    "explanation": "Sprints curtas permitem feedback frequente e limitam o risco financeiro e de tempo. Se algo der errado, perde-se no máximo o investimento de uma Sprint.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: O Product Owner pode delegar a ordenação do Product Backlog a outra pessoa.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O PO pode delegar o trabalho de gerenciamento do Product Backlog (incluindo ordenação) a outros, mas permanece como o responsável (accountable) final.",
    "difficulty": "hard"
  },
  {
    "question": "O que o Scrum Guide diz sobre o tamanho mínimo de um Scrum Team?",
    "options": ["Não define um tamanho mínimo específico, apenas que deve ser pequeno o suficiente para ser ágil", "Mínimo de 3 Developers", "Mínimo de 5 pessoas", "Mínimo de 7 pessoas"],
    "answer": "Não define um tamanho mínimo específico, apenas que deve ser pequeno o suficiente para ser ágil",
    "explanation": "O Scrum Guide diz que o Scrum Team é tipicamente 10 ou menos pessoas e deve ser pequeno o suficiente para permanecer ágil e grande o suficiente para completar trabalho significativo.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: O Scrum Guide 2020 introduziu o conceito de compromissos (commitments) para cada artefato.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide 2020 introduziu compromissos: Meta do Produto (para o Product Backlog), Meta da Sprint (para o Sprint Backlog) e Definição de Pronto (para o Incremento).",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: A adaptação deve ocorrer o mais rápido possível quando a inspeção revela algo fora dos limites aceitáveis.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "O Scrum Guide afirma que, se qualquer aspecto de um processo desvia para fora dos limites aceitáveis, o processo deve ser ajustado o mais rápido possível.",
    "difficulty": "easy"
  },
  {
    "question": "Qual é a melhor descrição do Scrum Team?",
    "options": ["Uma unidade coesa de profissionais focados em um objetivo de cada vez, a Meta do Produto", "Um grupo de pessoas com papéis hierárquicos", "Uma equipe gerenciada pelo Scrum Master", "Um time de desenvolvimento que reporta ao Product Owner"],
    "answer": "Uma unidade coesa de profissionais focados em um objetivo de cada vez, a Meta do Produto",
    "explanation": "O Scrum Guide define o Scrum Team como a unidade fundamental do Scrum — uma unidade coesa de profissionais focados em um objetivo de cada vez.",
    "difficulty": "medium"
  },
  {
    "question": "Verdadeiro ou Falso: Os eventos Scrum criam regularidade e minimizam a necessidade de reuniões não definidas no Scrum.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "Todos os eventos são time-boxed e criam regularidade, minimizando a necessidade de reuniões adicionais não previstas no framework.",
    "difficulty": "easy"
  },
  {
    "question": "Se o Scrum Team identifica que a Definição de Pronto precisa ser mais rigorosa, quando essa mudança entra em vigor?",
    "options": ["A partir do próximo Incremento", "Retroativamente, incluindo Incrementos anteriores", "Apenas na próxima Sprint", "Somente após a aprovação da gerência"],
    "answer": "A partir do próximo Incremento",
    "explanation": "Uma Definição de Pronto mais rigorosa se aplica aos próximos Incrementos. Não é retroativa para trabalho já completado e aceito como Incremento.",
    "difficulty": "hard"
  },
  {
    "question": "Verdadeiro ou Falso: No Scrum, 'done' e 'undone' work devem ser transparentes.",
    "options": ["Verdadeiro", "Falso"],
    "answer": "Verdadeiro",
    "explanation": "A transparência é um pilar do Scrum. Todo o trabalho, seja concluído ou não concluído, deve ser visível e compreensível para promover decisões informadas.",
    "difficulty": "medium"
  },
]


# --- Configuracoes da aplicacao ---
st.set_page_config(
    page_title="Simulado PSM I - Professional Scrum Master",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Definição das cores do tema ---
primary_color = "#662D91"
secondary_color = "#9B6FC0"
background_color = "#F5F0FA"
text_color = "#333333"

# --- CSS para o tema roxo (Scrum.org) ---
custom_css = f"""
<style>
    /* ----------------------------- TIPOGRAFIA ----------------------------- */
    section.main h1, .block-container h1 {{
        font-size: 2.2em;
    }}
    section.main h2, .block-container h2 {{
        font-size: 1.6em;
    }}
    section.main h3, .block-container h3 {{
        font-size: 1.3em;
    }}

    /* ----------------------------- BOTÕES ----------------------------- */
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        border-radius: 10px; /* Aumentado para um look mais rebuscado */
        border: none;
        padding: 12px 24px; /* Padding maior para destaque */
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
        transition: all 0.3s ease; /* Transição suave */
        font-size: 1em;
    }}

    .stButton>button:hover {{
        background-color: {secondary_color};
        transform: translateY(-2px); /* Efeito de elevação */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}
    .stButton>button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .stButton>button[kind="secondary"], 
    .stButton>button[kind="secondary"]:focus {{
        background-color: #D3D3D3;
        color: #333333;
    }}
    .stButton>button[kind="secondary"]:hover {{
        background-color: #BEBEBE;
        color: #333333;
    }}

    /* Tema Dark */
    .st-emotion-cache-13k62yr .stButton>button,
    body[color-scheme="dark"] .stButton>button {{
        background-color: #4A90E2; /* Tom mais escuro de azul para contraste */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    .st-emotion-cache-13k62yr .stButton>button:hover,
    body[color-scheme="dark"] .stButton>button:hover {{
        background-color: #63A4FF;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"],
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:focus {{
        background-color: #555555;
        color: #E0E0E0;
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"]:hover,
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:hover {{
        background-color: #6E6E6E;
        color: #E0E0E0;
    }}

    .stButton {{
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}
    /* Alinha os botões quando aparecem juntos */
    .stButton + .stButton {{
    margin-top: 0 !important;
    }}

    /* ----------------------------- FORMULÁRIO DE CADASTRO ----------------------------- */
    div[data-testid="stForm"] {{
        border: 1px solid {secondary_color};
        border-radius: 10px;
        padding: 1rem 1rem 0.5rem 1rem;
    }}
    body[data-theme="dark"] div[data-testid="stForm"] {{
        border-color: #4A5464 !important;
    }}

    /* ----------------------------- DATAFRAME (RANKING) ----------------------------- */
    /* Cor de fundo da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #E7F1FF !important;
    }}
    /* Cor do texto da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #000000 !important;
    }}
    /* Tema Dark para o DataFrame */
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #2C3440 !important;
    }}
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RADIO ----------------------------- */
    .stRadio > label p {{
        font-size: 1.05em !important;
    }}
    body[data-theme="dark"] .stRadio > label p,
    body.dark .stRadio > label p {{
        color: #FAFAFA !important;
    }}
    body[data-theme="light"] .stRadio > label p,
    body.light .stRadio > label p {{
        color: #333333 !important;
    }}
    div[data-baseweb="radio"] > label {{
    margin-bottom: 6px !important;
    }}

    /* ----------------------------- TEXTOS DAS QUESTÕES ----------------------------- */
    .quiz-question-text {{
        font-size: 1.2em;
        color: inherit;
        margin-bottom: 10px !important; 
        line-height: 1.1;
    }}
    body[data-theme="dark"] .quiz-question-text, 
    body.dark .quiz-question-text,
    body[data-theme="dark"] .quiz-question-text strong, 
    body.dark .quiz-question-text strong {{
        color: #FAFAFA !important; 
    }}

    /* ----------------------------- CAIXA DE EXPLICAÇÃO ----------------------------- */
    .explanation-box {{
        border: 1px solid {secondary_color};
        background-color: #E7F1FF;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px !important';
        line-height: 1.6;
        color: {text_color};
    }}
    body[data-theme="dark"] .explanation-box,
    body.dark .explanation-box {{
        background-color: #2C3440 !important;
        border-color: #4A5464 !important;
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RESULTADO ----------------------------- */
    .score-display {{
        font-size: 1.5em;
        font-weight: bold;
        color: {primary_color};
        text-align: center;
        margin-top: 10px !important;
    }}

    .timer-display {{
        font-size: 1.1em;
        font-weight: bold;
        color: {primary_color};
        padding: 10px;
        border: 1px solid {secondary_color};
        border-radius: 5px;
        background-color: #E7F1FF;
        text-align: center;
    }}

    /* ----------------------------- BLOCOS DE CÓDIGO ----------------------------- */
    .quiz-question-text pre,
    .explanation-box pre {{
        background-color: #282c34 !important;
        color: #abb2bf !important;
        padding: 0.6em !important;
        margin: 0.5em !important;
        border-radius: 5px !important;
        overflow-x: auto !important;
        white-space: pre !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.95em !important;
        line-height: 1.6 !important;
        border: 1px solid #3e4451;
    }}

    .quiz-question-text pre code,
    .explanation-box pre code {{
        display: block !important;
        padding: 0 !important;
        margin: 0 !important;
        white-space: pre !important;
        border: none !important;
    }}

    .quiz-question-text p > code,
    .quiz-question-text li > code,
    .explanation-box p > code,
    .explanation-box li > code {{
        padding: 0.1em 0.4em !important;
        margin: 0 0.2em !important;
        display: inline-block !important;
        white-space: pre-wrap !important;
        vertical-align: baseline !important;
    }}

    /* ----------------------------- SYNTAX HIGHLIGHTING ----------------------------- */
    .quiz-question-text pre .c1, .explanation-box pre .c1,
    .quiz-question-text pre .cm, .explanation-box pre .cm {{
        color: #5c6370 !important; font-style: italic !important;
    }}
    .quiz-question-text pre .k, .explanation-box pre .k,
    .quiz-question-text pre .kn, .explanation-box pre .kn {{
        color: #c678dd !important;
    }}
    .quiz-question-text pre .nb, .explanation-box pre .nb,
    .quiz-question-text pre .nc, .explanation-box pre .nc {{
        color: #e5c07b !important;
    }}
    .quiz-question-text pre .nf, .explanation-box pre .nf {{
        color: #61afef !important;
    }}
    .quiz-question-text pre .s1, .explanation-box pre .s1,
    .quiz-question-text pre .s2, .explanation-box pre .s2 {{
        color: #98c379 !important;
    }}
    .quiz-question-text pre .mi, .explanation-box pre .mi,
    .quiz-question-text pre .mf, .explanation-box pre .mf {{
        color: #d19a66 !important;
    }}
    .quiz-question-text pre .bp, .explanation-box pre .bp,
    .quiz-question-text pre .o, .explanation-box pre .o {{
        color: #56b6c2 !important;
    }}
    .quiz-question-text pre .p, .explanation-box pre .p,
    .quiz-question-text pre .n, .explanation-box pre .n {{
        color: #abb2bf !important;
    }}

    /* ----------------------------- RODAPÉ ----------------------------- */
    .rodape-container {{
        position: static;
        width: 100%;
        margin-top: 2rem;
        padding: 0;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }}
    body[data-theme="dark"] .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}

    /* Forçar herança do tema dark do contêiner pai */
    .st-emotion-cache-13k62yr .rodape-container,
    body[color-scheme="dark"] .rodape-container,
    body[data-theme="dark"] .rodape-container,
    body.dark .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}
    .st-emotion-cache-13k62yr .rodape-container *,
    body[color-scheme="dark"] .rodape-container *,
    body[data-theme="dark"] .rodape-container *,
    body.dark .rodape-container *,
    body.st-dark .rodape-container * {{
        background-color: #1a1c23 !important;
    }}
    .rodape {{
        margin: 0 auto;
        max-width: 900px;
        text-align: center;
        font-size: 0.7em;
        padding: 10px 1.5rem;
        color: #333333;
        box-sizing: border-box;
    }}
    body[data-theme="dark"] .rodape,
    body.st-dark .rodape {{
        background-color: transparent !important;
        color: #FAFAFA !important;
    }}
    .st-emotion-cache-13k62yr .rodape,
    body[color-scheme="dark"] .rodape,
    body[data-theme="dark"] .rodape,
    body.dark .rodape,
    body.st-dark .rodape {{
        color: #abb2bf !important;
    }}
    .rodape .linha {{
        margin: 5px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .rodape .links {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 5px;
    }}
    .rodape .links a {{
        text-decoration: none;
        transition: transform 0.3s ease;
    }}
    .rodape .links a:hover {{
        transform: scale(1.1);
    }}
    @media (max-width: 768px) {{
        .rodape-container {{
            margin-top: 2rem;
        }}
        section.main h1, .block-container h1 {{
            font-size: 1.2em !important;
        }}
        .main h2 {{
            font-size: 1.2em !important;
        }}
        .main h3 {{
            font-size: 1em !important;
        }}
        .rodape {{
            font-size: 0.75em;
        }}
        .rodape .links {{
            flex-direction: row;  /* mantém horizontal no mobile */
        }}
        /* Remove espaçamento excessivo entre os botões */
        .st-emotion-cache-ocqkz7 {{
        margin-top: 0 !important;
        gap: 0.2rem !important; /* ou 0.2rem se quiser ainda mais próximo */
        }}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- Aqui ficam as variáveis globais do SIMULADO como numeros de perguntas, limite de tempo e porcetagem de aprovado ---
NUM_QUESTIONS_PER_QUIZ = 80
QUIZ_TIME_LIMIT_MINUTES = 60
PASSING_PERCENTAGE = 85

RANKING_FILE = 'ranking.json'

# --- Funções ---
def initialize_quiz_session():
    # Garante uma nova semente aleatória a cada inicialização para máxima variedade das perguntas
    random.seed(time.time_ns())

    if len(questions_data) >= NUM_QUESTIONS_PER_QUIZ:
        selected_questions = random.sample(questions_data, NUM_QUESTIONS_PER_QUIZ)
    else:
        selected_questions = random.sample(questions_data, len(questions_data))
    
    st.session_state.questions_to_ask = selected_questions
    st.session_state.total_quiz_questions = len(selected_questions)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = [None] * len(selected_questions)
    st.session_state.answer_submitted = False
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.quiz_start_time = 0.0
    st.session_state.time_up = False
    st.session_state.ranking_updated = False
    # Não limpa o user_info para que o usuário continue logado para novas tentativas
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}

def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_ranking(ranking_data):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(ranking_data, f, indent=4, ensure_ascii=False)

def add_to_ranking(user_data, score, time_seconds, total_questions_quiz, questions_answered):
    ranking = load_ranking()
    new_entry = {
        "name": user_data.get("name", "Fantasma"),
        "email": user_data.get("email", ""),
        "city": user_data.get("city", ""),
        "country": user_data.get("country", ""),
        "score": score,
        "questions_answered": questions_answered,
        "time_seconds": int(time_seconds),
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "total_questions": total_questions_quiz 
    }
    ranking.append(new_entry)
    # Ordena por pontos (desc) e depois por tempo (asc)
    ranking.sort(key=lambda x: (-x['score'], x['time_seconds']))
    top_10 = ranking[:10]
    save_ranking(top_10)

def display_question(question_data, current_idx, total_questions):
    # Título geral do simulado
    st.markdown(
        f"<div class='quiz-question-text'><strong>Pergunta {current_idx + 1}/{total_questions}:</strong></div>", 
        unsafe_allow_html=True)

    question_text = question_data['question']

    # Pré-processar para blocos de código "cercados" por ```python ... ```
    # Regex para encontrar ```python ... ``` e substituir por <pre><code class="language-python">...</code></pre>
    # A flag re.DOTALL faz com que '.' corresponda também a quebras de linha
    question_text = re.sub(
        r'```python\s*\n(.*?)\n\s*```',
        r'<pre><code class="language-python">\1</code></pre>',
        question_text,
        flags=re.DOTALL
    )
    # Pré-processar para código inline (envolvido por crases simples)
    question_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', question_text)

    st.markdown(f"<div class='quiz-question-text'>{question_text}</div>", unsafe_allow_html=True)
    original_options = list(question_data['options']) # Garante que é uma lista

    def format_option_for_display(opt_str):
        # Substitui múltiplos espaços por &nbsp; para correta renderização no HTML
        # Trata de 2 a 5 espaços consecutivos. Pode ser expandido se necessário.
        s = opt_str
        s = s.replace("     ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;") # 5 espaços
        s = s.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")   # 4 espaços
        s = s.replace("   ", "&nbsp;&nbsp;&nbsp;")      # 3 espaços
        s = s.replace("  ", "&nbsp;&nbsp;")         # 2 espaços
        return s

    display_options = [format_option_for_display(opt) for opt in original_options]
    
    # Determina o índice para st.radio com base na resposta original armazenada
    current_user_original_answer = st.session_state.user_answers[current_idx]
    radio_index = None
    if st.session_state.answer_submitted and current_user_original_answer is not None:
        try:
            # Encontra o índice da resposta original nas opções originais
            original_answer_index = original_options.index(current_user_original_answer)
            radio_index = original_answer_index # st.radio usará este índice com display_options
        except ValueError:
            # Caso a resposta armazenada não esteja nas opções originais (improvável com dados consistentes)
            radio_index = None

    # st.radio usa unsafe_allow_html implicitamente para as opções se elas contiverem HTML simples como &nbsp;
    user_choice_display_value = st.radio(
        "Escolha sua resposta:",
        options=display_options, # Usa as opções formatadas para exibição
        index=radio_index,
        key=f"q_radio_{current_idx}",
        disabled=st.session_state.answer_submitted
    )

    # Mapeia a escolha de exibição de volta para o valor da opção original
    if user_choice_display_value is not None:
        selected_display_index = display_options.index(user_choice_display_value)
        user_selected_original_option = original_options[selected_display_index]
        return user_selected_original_option
    return None

def display_timer_and_handle_timeout():
    if st.session_state.quiz_started and not st.session_state.quiz_completed and st.session_state.quiz_start_time > 0:
        timer_placeholder = st.sidebar.empty()
        current_time = time.time()
        elapsed = current_time - st.session_state.quiz_start_time
        time_limit_sec = QUIZ_TIME_LIMIT_MINUTES * 60

        if elapsed >= time_limit_sec:
            if not st.session_state.time_up:
                st.session_state.time_up = True
                st.session_state.quiz_completed = True
                timer_placeholder.error("⏰ Tempo Esgotado!")
                st.warning("⏰ Seu tempo para o quiz esgotou! Verificando resultados...")
                st.experimental_rerun()
            return

        remaining_time = time_limit_sec - elapsed
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_placeholder.markdown(
            f"<div class='timer-display'>⏳ Tempo Restante: {minutes:02d}:{seconds:02d}</div>", 
            unsafe_allow_html=True
        )

        display_ranking_sidebar()
        time.sleep(1)
        st.rerun()

def display_ranking_sidebar():
    st.sidebar.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    with st.sidebar.expander("🏆 Top 10 Ranking", expanded=False):
        ranking_data = load_ranking()
        if not ranking_data:
            st.write("O ranking ainda está vazio. Seja o primeiro a pontuar!")
        else:
            # Calcula a porcentagem para cada entrada
            for entry in ranking_data:
                total_q = entry.get('total_questions', NUM_QUESTIONS_PER_QUIZ) # Usa NUM_QUESTIONS_PER_QUIZ como fallback
                entry['percentage'] = (entry['score'] / total_q) * 100 if total_q > 0 else 0

            df = pd.DataFrame(ranking_data)
            # Formata o tempo para exibição
            df['Tempo'] = df['time_seconds'].apply(lambda s: f"{int(s // 60):02d}:{int(s % 60):02d}")
            # Formata a porcentagem para exibição
            df['Porcentagem'] = df['percentage'].apply(lambda p: f"{int(p)}%")
            # Seleciona e renomeia colunas para exibição
            df_display = df[['name', 'Porcentagem', 'Tempo', 'city', 'country']]
            df_display.columns = ["Nome", "Acerto", "Tempo", "Cidade", "País"]
            # Define o índice para começar em 1 (para o ranking)
            df_display.index = range(1, len(df_display) + 1)
            st.dataframe(df_display, use_container_width=True)

def show_results_page():
    score = st.session_state.score
    total = st.session_state.total_quiz_questions
    final_time_seconds = time.time() - st.session_state.quiz_start_time
    user_info = st.session_state.get("user_info", {})
    pct = (score / total) * 100 if total > 0 else 0

    if pct >= PASSING_PERCENTAGE:
        st.header("🎉 Simulado Concluído! 🎉")
    else:
        st.header("👎🏾 Simulado Concluído! 👎🏾")

    if st.session_state.get("time_up", False):
        st.warning("⏰ Seu tempo para o simulado esgotou!")

    # Garante que o ranking seja atualizado apenas uma vez por quiz
    if not st.session_state.get("ranking_updated", False):
        questions_answered = sum(1 for answer in st.session_state.user_answers if answer is not None)
        add_to_ranking(user_info, score, final_time_seconds, total, questions_answered)
        st.session_state.ranking_updated = True

    display_ranking_sidebar()

    st.markdown(f"<p class='score-display'>Você acertou {score} de {total} questões. ({pct:.1f}%)</p>", unsafe_allow_html=True)
    
    if pct >= PASSING_PERCENTAGE:
        st.success("✅ Parabéns! Você foi aprovado no simulado da certificação PSM I!")
        st.balloons()  # balões só para APROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://imagens.net.br/wp-content/uploads/2024/06/os-melhores-gifs-de-parabens-para-qualquer-ocasiao-1.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("❌ Você não atingiu a pontuação mínima de 85% para aprovação. Estude o Scrum Guide e tente novamente!")
        st.snow() # emojis de gelor para REPROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://media1.tenor.com/m/gw207uCZe_MAAAAC/estuda-porra-evelyn-castro.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📖 Revisar apenas as questões respondidas"):
        any_answered = False
        if not st.session_state.questions_to_ask:
            st.write("Nenhuma questão para revisar.")
        else:
            for i, q_data_original in enumerate(st.session_state.questions_to_ask):
                user_answer_for_this_q = st.session_state.user_answers[i]

                if user_answer_for_this_q is not None:  # Usuário respondeu a esta pergunta
                    any_answered = True
                    st.markdown(f"**Pergunta {i + 1}:**") # Usa o índice original da pergunta
                    st.markdown(q_data_original['question'], unsafe_allow_html=True)
                    st.markdown(f"**Sua resposta:** {user_answer_for_this_q}")

                    if user_answer_for_this_q == q_data_original["answer"]:
                        st.markdown(f"**Resultado:** ✅ Correto")
                    else:
                        st.markdown(f"**Resultado:** ❌ Incorreto")
                        st.markdown(f"**Resposta correta:** {q_data_original['answer']}")

                    st.markdown(
                        f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{q_data_original.get('explanation', 'Nenhuma explicação disponível.')}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")
            
            if not any_answered and st.session_state.questions_to_ask:
              st.write("Você não respondeu a nenhuma questão.")

    if st.button("Reiniciar Simulado ♻️"):
        initialize_quiz_session()
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.rerun()

# --- Inicializar estado do simulado ---
if "questions_to_ask" not in st.session_state:
    initialize_quiz_session()

# --- Interface principal do simulado ---
if not st.session_state.quiz_started:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="https://scrumorg-website-prod.s3.amazonaws.com/drupal/inline-images/2022-09/asset_44psmi_0.png" alt="Scrum.org Logo" width="160"/>
            <h1 style="margin: 0;">Simulado PSM I - Professional Scrum Master I</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
### 📢 Sobre a Certificação PSM I:
                
Este simulado é baseado na certificação oficial **Professional Scrum Master I (PSM I)** oferecida pela [Scrum.org](https://www.scrum.org/assessments/professional-scrum-master-i-certification).

A PSM I valida o entendimento profundo do framework **Scrum** conforme descrito no **Scrum Guide 2020**.

---  

📝 **Formato da Prova Oficial:**
- 🔢 **Número de questões:** 80 (múltipla escolha e verdadeiro/falso)  
- ⏰ **Tempo para realização:** 60 minutos  
- ✅ **Nota mínima para aprovação:** 85% (ou seja, 68 de 80 questões)  
- 💰 **Custo:** $200 USD (uma tentativa incluída)  
- 🌐 **Aplicação:** Online, sem necessidade de supervisor  
- ♾️ **Validade:** Não expira — certificação vitalícia  
- 📖 **Base:** [The Scrum Guide™ 2020](https://scrumguides.org/)

📋 **Tópicos cobertos neste simulado:**
- Pilares do Scrum (Transparência, Inspeção, Adaptação)
- Valores do Scrum (Comprometimento, Coragem, Foco, Abertura, Respeito)
- Papéis: Scrum Master, Product Owner, Developers
- Eventos: Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective
- Artefatos: Product Backlog, Sprint Backlog, Incremento
- Compromissos: Meta do Produto, Meta da Sprint, Definição de Pronto

🧠 Utilize este simulado para testar seus conhecimentos e se preparar para a certificação real!

""")
    
    display_ranking_sidebar() # Exibe o ranking na página inicial
    with st.expander("👤 Cadastro para o Top 10 Ranking (Opcional)"):
        with st.form("registration_form"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            city = st.text_input("Cidade")
            country = st.text_input("País")
            submitted = st.form_submit_button("Salvar Cadastro")
            if submitted and name: # Nome é obrigatório para o cadastro
                st.session_state.user_info = {
                    "name": name, "email": email, "city": city, "country": country
                }
                st.success(f"Olá, {name}! Você está cadastrado para o ranking.")

    if st.session_state.get("user_info", {}).get("name"):
        st.info(f"✅ Logado como **{st.session_state.user_info['name']}**. Seu resultado será registrado no ranking se estiver no Top 10.")

    if st.button("🚀 Iniciar Simulado"):
        st.session_state.quiz_started = True
        st.session_state.quiz_start_time = time.time()
        st.rerun()

elif st.session_state.quiz_completed:
    show_results_page()

else:
    current_idx = st.session_state.current_question_index
    total_questions = st.session_state.total_quiz_questions
    current_question = st.session_state.questions_to_ask[current_idx]

    # --- Barra de Progresso ---
    # O progresso e o texto devem refletir a questão atual (índice + 1)
    progress_value = (current_idx + 1) / total_questions
    st.markdown(
        f"<div class='progress-text'>{current_idx + 1} / {total_questions}</div>", 
        unsafe_allow_html=True
    )
    st.progress(progress_value)
    # --- Fim da Barra de Progresso ---
    user_choice = display_question(current_question, current_idx, total_questions)

    # Criar um placeholder para a área de feedback (sucesso/erro e explicação)
    feedback_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    initial_action_buttons_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    action_buttons_placeholder = st.empty()

    if not st.session_state.answer_submitted:
        # Botões "Confirmar e Avançar" e "Finalizar Simulado" DENTRO do placeholder inicial
        with initial_action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1]) # Ajuste a proporção conforme necessário
            with col1:
                if st.button("Confirmar e Avançar ❯", key=f"confirm_next_{current_idx}", use_container_width=True):
                    if user_choice is not None:  # Usuário selecionou uma resposta
                        st.session_state.answer_submitted = True
                        st.session_state.user_answers[current_idx] = user_choice
                        if user_choice == current_question["answer"]:
                            st.session_state.score += 1
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        # Não avança o índice ainda, apenas reroda para mostrar o feedback
                        st.rerun()
                    else:  # Usuário não selecionou, considera como "pulada" e avança
                        st.session_state.user_answers[current_idx] = None # Marca como não respondida
                        if current_idx < total_questions - 1:
                            st.session_state.current_question_index += 1
                            # st.session_state.answer_submitted permanece False
                        else:
                            st.session_state.quiz_completed = True
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_main", use_container_width=True):
                    st.session_state.quiz_completed = True
                    initial_action_buttons_placeholder.empty() # Limpa estes botões
                    if hasattr(st.session_state, 'timer_placeholder'): # Garante que o placeholder do timer existe
                        st.session_state.timer_placeholder.empty() # Limpa o timer também ao finalizar
                    else:
                        st.sidebar.empty() # Tenta limpar a sidebar se o placeholder específico não foi definido
                    st.rerun()
    else:
        # Resposta já foi submetida (answer_submitted is True), mostrar feedback DENTRO do placeholder
        with feedback_placeholder.container(): # Usar .container() para agrupar múltiplos elementos no placeholder
            correct_answer = current_question["answer"]
            user_answer_for_current_q = st.session_state.user_answers[current_idx]

            if user_answer_for_current_q == correct_answer:
                st.success("✅ Resposta correta!")
            else:
                st.error(f"❌ Resposta incorreta! A resposta correta é: **{correct_answer}**")

            st.markdown(
                f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{current_question.get('explanation', 'Nenhuma explicação disponível.')}</div><br>",
                unsafe_allow_html=True
            )


        # Botões após o feedback DENTRO do placeholder de botões de ação
        with action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1])
            with col1:
                if current_idx < total_questions - 1:
                    if st.button("Próxima Pergunta ➡️", key=f"next_question_{current_idx}", use_container_width=True):
                        st.session_state.current_question_index += 1
                        st.session_state.answer_submitted = False  # Reset para a próxima pergunta
                        initial_action_buttons_placeholder.empty() # Garante que os botões iniciais não reapareçam indevidamente
                        feedback_placeholder.empty() # Limpa o feedback anterior
                        action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
                else: # Última pergunta já respondida e feedback mostrado
                    if st.button("Ver Resultado Final 🏁", key="finish_quiz_final_feedback", use_container_width=True):
                        st.session_state.quiz_completed = True
                        feedback_placeholder.empty()
                        action_buttons_placeholder.empty()
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_feedback", use_container_width=True):
                    st.session_state.quiz_completed = True
                    feedback_placeholder.empty()
                    action_buttons_placeholder.empty()
                    if hasattr(st.session_state, 'timer_placeholder'):
                        st.session_state.timer_placeholder.empty()
                    else:
                        st.sidebar.empty()
                    st.rerun()

display_timer_and_handle_timeout()

# --- Rodapé com informações do desenvolvedor e versão ---
st.markdown(
    f"""
    <div class="rodape-container">
      <div class="rodape">
          <div class="linha"> 👨🏾‍💻 <b>Desenvolvido por:</b></div>
          <div class="links">
              <a href="https://github.com/pedroar9/" target="_blank">
                  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
              </a>
              <a href="https://www.linkedin.com/in/pedrocarlos-assis/" target="_blank">
                  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
              </a>         
          </div>  
          <div class="linha"> <br> </div>
          <div class="linha">⚙️ <b>Versão:</b> 1.0.4</div> 
          <div class="linha">🗓️ <b>Build:</b> {data_build}</div>        
      </div>
    </div>
    """,
    unsafe_allow_html=True
)