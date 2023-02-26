from logic4py.logic_gui import verify_reasoning, display_is_countermodel, display_truth_formulas, display_graph_truth_formulas



def verify_reasoning_q1_ex(language_pt=True):
    input_assumptions  =['Se está chovendo, então a rua está molhada.','Está chovendo.'] if language_pt else ["If it's raining, then the street is wet.","It's raining"]
    input_conclusion = 'A rua está molhada.' if language_pt else "The street is wet."
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)


def verify_reasoning_q2_ex(language_pt=True):
    input_assumptions  =['Se C, então M','C'] if language_pt else  ['If C, then M','C'] 
    input_conclusion = 'M'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q3_ex(language_pt=True):
    input_assumptions  =['Se $\\varphi$ então $\\psi$', '$\\varphi$'] if language_pt else ['If $\\varphi$ then $\\psi$', '$\\varphi$'] 
    input_conclusion = '$\\psi$'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q4_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o trem tivesse chegado atrasado e não houvesse táxi na estação, então John se atrasaria para seu compromisso.',
    'John não se atrasou para seu compromisso.','O trem chegou atrasado.']
      input_conclusion = 'Havia táxis na estação.'
    else: 
      input_assumptions  =['If the train was late and there was no cab at the station, then John would be late for his appointment.',
    'John was not late for his appointment.','The train arrived late.']
      input_conclusion = 'There was a cab at the station.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q5_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Se tivesse chovendo e Jane não estivesse com seu guarda-chuva, então ela se molharia.',
      'Jane não está molhada.','Está chovendo.'] 
      input_conclusion = 'Jane está com seu guarda-chuva.'
    else: 
      input_assumptions  =["If it was raining and Jane didn't have her umbrella, then she would get wet.",
      'Jane is not wet.',"It's raining."] 
      input_conclusion = 'Jane has her umbrella.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q6_ex(language_pt=True):
    input_assumptions  =['$(\\varphi\\wedge\\lnot\\psi)\\rightarrow\\sigma$','$\\lnot\\sigma$', '$\\varphi$'] 
    input_conclusion = '$\\psi$'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q1(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Os produtos não ficaram mais caros.'] 
      input_conclusion = 'dólar não subiu.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q2(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Os produtos ficaram mais caros.'] 
      input_conclusion = 'dólar não subiu.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q3(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Os produtos ficaram mais caros.'] 
      input_conclusion = 'dólar subiu.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q4(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'O dólar não subiu.'] 
      input_conclusion = 'Os produtos não ficaram mais caros.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q5(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'O dólar não subiu.'] 
      input_conclusion = 'Os produtos ficaram mais caros.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q6(language_pt=True):
    if language_pt:
      input_assumptions  =['O dólar sobe ou o petróleo sobe.',
      'O dólar não subiu.'] 
      input_conclusion = 'O petróleo subiu.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q7(language_pt=True):
    if language_pt:
      input_assumptions  =['O dólar sobe ou o petróleo sobe.',
      'Se o dólar sobe, então aumenta a inflação.','Se o petróleo sobe, então aumenta a inflação.'] 
      input_conclusion = 'Aumentou a inflação.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q8(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe ou o petróleo sobe, então aumenta a inflação.',
      'O dólar não subiu.','O petróleo não subiu.'] 
      input_conclusion = 'Aumentou a inflação.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q9(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe ou o petróleo sobe, então aumenta a inflação.',
      'O dólar não subiu.','O petróleo não subiu.'] 
      input_conclusion = 'Não aumentou a inflação.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q10(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Se o dólar não sobe, então compro mais comida.','Os produtos não ficaram mais caro.'] 
      input_conclusion = 'Comprei mais comida.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q11(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Se o dólar não sobe, então compro mais comida.','Os produtos ficaram mais caro.'] 
      input_conclusion = 'Comprei mais comida.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_q12(language_pt=True):
    if language_pt:
      input_assumptions  =['Se o dólar sobe, então os produtos ficam mais caros.',
      'Se o dólar não sobe, então compro mais comida.','Os produtos ficaram mais caro.'] 
      input_conclusion = 'Não comprei mais comida.'
#    else: 
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)


def verify_reasoning_fo_q1_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente gosta de esporte radical.','Maria gosta de voo de parapente.'] 
      input_conclusion = 'Maria gosta de esporte radical.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q2_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente gosta de esporte radical.','Maria não gosta de esporte radical.'] 
      input_conclusion = 'Maria gosta de voo de parapente.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q3_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente não gosta de chuva.','João gosta chuva.'] 
      input_conclusion = 'João não gosta de voo de parapente.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q4_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente não gosta de chuva.','João não gosta chuva.'] 
      input_conclusion = 'João gosta de voo de parapente.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q5_ex(language_pt=True):
    if language_pt:
      input_assumptions  =['Todo mundo que é amado por alguém é feliz.',
      'Existe alguém que não é feliz.'] 
      input_conclusion = 'Existe alguém que não é amado por ninguém.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q1(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente gosta de esporte radical.','Maria gosta de voo de parapente.'] 
      input_conclusion = 'Maria não gosta de esporte radical.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q2(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem não gosta de esporte radical não gosta de voo de parapente.','Maria gosta de voo de parapente.'] 
      input_conclusion = 'Maria gosta de esporte radical.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q3(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem não gosta de esporte radical não gosta de voo de parapente.','Maria não gosta de voo de parapente.'] 
      input_conclusion = 'Maria gosta de esporte radical.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q4(language_pt=True):
    if language_pt:
      input_assumptions  =['Quem gosta de voo de parapente gosta de esporte radical.','Alguém gosta de voo de parapente.'] 
      input_conclusion = 'Alguém gosta de esporte radical.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q5(language_pt=True):
    if language_pt:
      input_assumptions = ['Quem gosta de voo de parapente gosta de esporte radical.', 'Alguém gosta de esporte radical.'] 
      input_conclusion = 'Alguém gosta de voo de parapente.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q6(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Todos frequentam as aulas.', 'Todos fazem os exercícios'] 
      input_conclusion = 'Todos são aprovados.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q7(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém frequenta as aulas e faz os exercícios.'] 
      input_conclusion = 'Alguém é aprovado.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q8(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém frequenta as aulas.', 'Alguém faz os exercícios'] 
      input_conclusion = 'Alguém é aprovado.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q9(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém foi aprovado.'] 
      input_conclusion = 'Existe alguém que frequenta as aulas e fez os exercícios.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q10(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'] 
      input_conclusion = 'Existe alguém que não frequenta as aulas ou não faz os exercícios.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=True, language_pt=language_pt)

def verify_reasoning_fo_q11(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'] 
      input_conclusion = 'Existe alguém que não frequenta as aulas.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_reasoning_fo_q12(language_pt=True):
    if language_pt:
      input_assumptions = ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'] 
      input_conclusion = 'Existe alguém que não frequenta as aulas e não faz os exercícios.'
    verify_reasoning(input_assumptions,input_conclusion, result_value=False, language_pt=language_pt)

def verify_truth_fo_graph_q1(language_pt=True):
  formulas = ['Ex E(x,x)', 'Ax E(x,x)', 'Ax Ey E(x,y)', 'Ax Ey E(x,y)', 'Ax Ay (E(x,y)<->E(y,x))', 'Ex Ay ~E(y,x)', 'Ex Ay ~E(x,y)']
  universe = {'a','b','c','d'}
  arcs = {('a','b'),('b','a'),('b','c'),('c','c')}
  display_graph_truth_formulas(formulas, arcs, universe, language_pt=language_pt)

def verify_truth_formulas_q1(language_pt=True):
  universe = {'Socrates','Aristoteles','Zeus', 'Heitor'}
  s={}
  s['s']='Socrates'
  s['a']='Aristoteles'
  s['z']='Zeus'
  preds = {}
  preds['H',1] = {('Socrates'),('Aristoteles')}
  preds['M',1] = {('Socrates'),('Aristoteles')}

  formulas = ['H(s)','H(z)', 'Ex M(x)', 'Ax H(x)', 'Ax M(x)', 'Ax (H(x)->M(x))']
  display_truth_formulas(formulas,universe,s,preds, language_pt=language_pt)


def verify_countermodel_q1(language_pt=True):
  universe = {'0','1','2','3','4','5'}
  s={}
  preds = {}
  preds['P',1] = {('0'),('2'),('4')}
  preds['I',1] = {('1'),('3'),('5')}

  input_theorem = 'Ax (P(x) | I(x)) |= Ax P(x) | Ax I(x)'
  display_is_countermodel(input_theorem,universe,s,preds, language_pt=language_pt)
