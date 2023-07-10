import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
from logic4py.parser_formula import get_formula
from logic4py.parser_theorem import get_theorem
from logic4py.parser_def_formula import check_proof
from logic4py.formula import get_atoms, v_bar, get_vs, consequence_logic, truth_table, is_falsiable, is_unsatisfiable, is_satisfiable, is_valid, sat, is_countermodel, get_signature_predicates, get_propositional_atoms, get_signature_propositional_atoms, is_valid_interpretation
from logic4py.decoder import decode_fo_interpretation
from logic4py.example_reasoning import EXAMPLES
from random import randrange
import traceback
from graphviz import Digraph

def visualiza_relacao(A, R, labelSet=""):
	g = Digraph()
	g.attr(rankdir='LR')

	with g.subgraph(name='cluster_1') as c:
		c.attr(color='blue')
		c.node_attr.update(style='filled')
		c.attr(label=labelSet)
		for a1 in A:
			c.node(str(a1))
	for (a1,a2) in R:
		g.edge(str(a1),str(a2))
	return g

def is_substitutable(input_formula='', input_var ='x', input_term='a', language_pt=True):
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  cResult = widgets.RadioButtons(
    options=['Sim', 'Não'] if language_pt else ['Yes', 'No'],
    value=None, 
    description='Resposta:' if language_pt else 'Answer:',
    disabled=False
)
  output = widgets.Output()
  wButtons = widgets.HBox([run])

  if language_pt:
    display(HTML(rf'<b>O termo {input_term} é substituível para a variável {input_var} na fórmula {input_formula}:'))
  else:
    display(HTML(rf'<b>The term {input_term} is substitutable for the variable {input_var} in the formula {input_formula}:'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = get_formula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and (cResult.value=='Sim' or cResult.value=='Yes')):
              if language_pt:
               display(HTML(r'<b><font color="blue">Parabéns você acertou a questão!</font>')) 
               display(HTML(rf'<b>O termo {input_term} é substituível para a variável {input_var} na fórmula {input_formula}.'))
              else:
                display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))
                display(HTML(rf'<b>The term {input_term} is substitutable for the variable {input_var} in the formula {input_formula}.'))
            elif not f.is_substitutable(input_var,input_term) and (cResult.value=='Não' or cResult.value=='No'):
              if language_pt:
                display(HTML(r'<b><font color="blue">Parabéns você acertou a questão!</font>'))              
                display(HTML(rf'<b>O termo {input_term} não é substituível para a variável {input_var} na fórmula {input_formula}.'))
              else:
                display(HTML(r'<b><font color="blue">Congratulations you got the question right!</font>'))
                display(HTML(rf'<b>The term {input_term} is not substitutable for the variable {input_var} in the formula {input_formula}.'))
            else:
              if language_pt:
                display(HTML(rf'<b><font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(rf'<b><font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">The formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
  
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_variables(input_string='', input_formula = '', language_pt=True):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ; (ponto-e-vírgula)' if language_pt else 'Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  if language_pt:
    display(HTML(rf'<b>Digite o conjunto de variávels da fórmula {input_formula}:'))
    display(HTML(r'<b>Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'<b>Enter the set of variables of the formula {input_formula}:'))
    display(HTML(r'<b>Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.all_variables():
              if language_pt:
                display(HTML('<font color="blue">Parabéns, você acertou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<b><font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_free_variables(input_string='', input_formula = '', language_pt=True):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ; (ponto-e-vírgula)' if language_pt else 'Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  if language_pt:
    display(HTML(rf'<b>Digite o conjunto de variávels livres da fórmula {input_formula}:'))
    display(HTML(r'<b>Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'<b>Enter the set of the free variables of the formula {input_formula}:'))
    display(HTML(r'<b>Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.free_variables():
              if language_pt:
                display(HTML('<font color="blue">Parabéns, você acertou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<b><font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_bound_variables(input_string='', input_formula = '', language_pt=True):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite as variáveis separadas por ; (ponto-e-vírgula)' if language_pt else 'Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  if language_pt:
    display(HTML(rf'<b>Digite o conjunto de variávels ligadas da fórmula {input_formula}:'))
    display(HTML(r'<b>Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'<b>Enter the set of bound variables of the formula {input_formula}:'))
    display(HTML(r'<b>Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.bound_variables():
              if language_pt:
                display(HTML('<font color="blue">Parabéns, você acertou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<b><font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<b><font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_substitution(input_string='', input_formula = '', input_var ='x', input_term='a', language_pt=True):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite sua fórmula:' if language_pt else 'Enter your formula:',
      description='',
      layout=layout
      )
  if language_pt:
    cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  else:
    cParentheses = widgets.Checkbox(value=False, description='Display Formula with Parentheses')
  if language_pt:
    cLatex = widgets.Checkbox(value=False, description='Exibir Fórmula em Latex')
  else:
    cLatex = widgets.Checkbox(value=False, description='Display Formula in Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  if language_pt:
    display(HTML(rf'<b>Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:'))
  else:
    display(HTML(rf'<b>Enter the formula that results from substitution the variable {input_var} with the term {input_term} in the formula {input_formula}:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = get_formula(input_formula)
          result = get_formula(input.value)
          if(result!=None):
            if result==f.substitution(input_var,input_term):
              if language_pt:
                display(HTML(r'<b><font color="blue">Parabéns essa é a subtituição correta:</font>'))              
              else:
                display(HTML(r'<b><font color="blue">Congratulations this is the correct substitution:</font>'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'<b>${s}$'))
              else:
                display(HTML(rf'<b>{result.toString(parentheses=cParentheses.value)}'))
            else:
              if language_pt:
                display(HTML(rf'<b><font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>'))
              else:
                display(HTML(rf'<b><font color="red">Formula {result.toString()} is not the result of substitution {input_var} with {input_term} in the formula {input_formula}.</font>'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_reasoning_example(question, language='pt'):
  return verify_reasoning_exercise(EXAMPLES, question, language=language)

def verify_reasoning_exercise(examples, question, language='pt'):
    language_pt = language=='pt'
    if question not in examples.keys():
        if language_pt:
            raise ValueError(f"Questão {question} não está definida!")
        else:
            raise ValueError(f"Question {question} is not defined!")
    elif 'input_assumptions_'+language not in examples[question].keys():
        if language_pt:
           raise ValueError(f"Premissas da {question} não está definida na língua portuguesa!")
        else:
           raise ValueError(f"Assumptions for {question} is not defined in the language {language}!")
    elif 'input_conclusion_'+language not in examples[question].keys():
        if language_pt:
           raise ValueError(f"A conclusão da {question} não está definida na língua portuguesa!")
        else:
           raise ValueError(f"Conclusion for {question} is not defined in the language {language}!")
    elif 'result_value' not in examples[question].keys():
        if language_pt:
           raise ValueError(f"O valor-verdade da {question} não está definido!")
        else:
           raise ValueError(f"The truth-value for {question} is not defined!")
    return verify_reasoning(examples[question]['input_assumptions_'+language],examples[question]['input_conclusion_'+language], examples[question]['result_value'], language_pt=language_pt)


def verify_reasoning(input_assumptions, input_conclusion, result_value=False, language_pt=True):
    run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
    output = widgets.Output()
    wButtons = widgets.HBox([run])
    cResult = widgets.RadioButtons(
        options=['Sim', 'Não'] if language_pt else ['Yes', 'No'],
        value=None, 
        description=r'Resposta:' if language_pt else r'Answer:',
        disabled=False
    )
    questao = r'<b>Considere as seguintes afirmações:</b>' if language_pt else r'<b>Consider the following statements:</b>'
    i = 1
    for assumption in input_assumptions:
        questao += f'\n1. {assumption}'
        i+=1
    display(Markdown(questao))
    questao= r'<b>Podemos concluir que a afirmação abaixo segue logicamente das afirmações acima?' if language_pt else r'<b>Can we conclude that the statement below follows logically from the statements above?'
    display(Markdown(questao))
    questao =f'\n{i}. {input_conclusion}'
    display(Markdown(questao))
    display(widgets.HBox([cResult,wButtons]), output)

    def on_button_run_clicked(_):
        output.clear_output()
        with output:
            if (cResult.value==None):
                if language_pt:
                    display(HTML(r'<b><font color="red">Escolha uma das alternativas! Tente novamente!</font>'))
                else:
                    display(HTML(r'<b><font color="red">Choose an option! Try again!</font>'))
            elif(result_value==(cResult.value=='Sim' or cResult.value=='Yes')):
                if language_pt:
                    display(HTML(r'<b><font color="blue">Parabéns, você acertou a questão.</font>'))
                else: 
                    display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))
                cResult.disabled = True
                run.disabled = True
            else:
                if language_pt:
                    display(HTML(r'<b><font color="red">Infelizmente, você errou a questão.</font>'))
                else:
                    display(HTML(r'<b><font color="red">Unfortunately, you got the question wrong.</font>'))
                cResult.disabled = True
                run.disabled = True
    run.on_click(on_button_run_clicked)


def verify_formula(input_string='', language_pt=True):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite sua fórmula:' if language_pt else 'Enter your formula:',
      description='',
      layout=layout
      )
  if language_pt:
    cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  else:
    cParentheses = widgets.Checkbox(value=False, description='Display Formula with Parentheses')
  if language_pt:
    cLatex = widgets.Checkbox(value=False, description='Exibir Fórmula em Latex')
  else:
    cLatex = widgets.Checkbox(value=False, description='Display Formula in Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  if language_pt:
    display(Markdown(r'<b>Digite sua fórmula:'))
  else:
    display(Markdown(r'<b>Enter your formula:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value)
          if(result!=None):
              if language_pt:
                display(Markdown(r'<b><font color="blue">Parabéns! Esta é uma fórmula da lógica:</font></b>'))
              else:
                display(Markdown(r'<b><font color="blue">Congratulations this is a formula of logic:</font></b>'))

              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                print(result.toString(parentheses=cParentheses.value))
                #display(HTML(rf'<b>{result.toString(parentheses=cParentheses.value)}'))
          else:
            if language_pt:
              display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<b><font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)



def verify_formula_function(function,input_formula='', input_text_question='Considere a fórmula abaixo.', input_text_result='Parabéns, você acertou a questão.', input_text_result_error='Seu resultado não está correto. Tente novamente!', placeholder_result='Digite aqui a sua resposta:', language_pt=True):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Executar")
  input = widgets.Text(
      value=input_formula,
      placeholder='Digite sua fórmula:' if language_pt else 'Enter your formula:',      
      description='',
      layout=layout
      )
  inputResult = widgets.Text(
      value='',
      placeholder=placeholder_result,
      description='',
      layout=layout
      )
  output = widgets.Output()
  wInputs = widgets.HBox([input, inputResult])
  wButtons = widgets.HBox([run])
#  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  display(HTML(rf'<b>{input_text_question}'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          if(result!=None):
              
              if(str(function(result))==inputResult.value.strip()):
                display(HTML(rf'<b><font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<b><font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_formula_function_atoms(function,input_formula='',input_atom='', input_text_question='Considere a fórmula abaixo.', input_text_result='Parabéns, você acertou a questão.', input_text_result_error='Seu resultado não está correto. Tente novamente!', placeholder_result='Digite aqui a sua resposta:', language_pt=True):
  layout = widgets.Layout(width='33.3%')
  run = widgets.Button(description="Executar")
  input = widgets.Text(
      value=input_formula,
      placeholder='Digite sua fórmula',
      description='',
      layout=layout
      )
  inputAtom = widgets.Text(
      value=input_atom,
      placeholder='Digite o átomo',
      description='',
      layout=layout
      )
  inputResult = widgets.Text(
      value='',
      placeholder=placeholder_result,
      description='',
      layout=layout
      )
  output = widgets.Output()
  wInputs = widgets.HBox([input,inputAtom, inputResult])
  wButtons = widgets.HBox([run])
#  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  display(HTML(rf'<b>{input_text_question}:'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          resultAtom = get_formula(inputAtom.value.strip())
          if(result!=None):
              
              if(str(function(result,resultAtom))==inputResult.value.strip()):
                display(HTML(rf'<b><font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<b><font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_formula_function_set(function,input_formula='', input_text_question='Considere a fórmula abaixo.', input_text_result='Parabéns, você acertou a questão.', input_text_result_error='Seu resultado não está correto. Tente novamente!', placeholder_result='Digite aqui a sua resposta:', language_pt=True):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Executar")
  input = widgets.Text(
      value=input_formula,
      placeholder='Digite sua fórmula:' if language_pt else 'Enter your formula:',      
      description='',
      layout=layout
      )
  inputResult = widgets.Text(
      value='',
      placeholder=placeholder_result,
      description='',
      layout=layout
      )
  output = widgets.Output()
  wInputs = widgets.HBox([input, inputResult])
  wButtons = widgets.HBox([run])

  display(HTML(rf'<b>{input_text_question}:'))
  display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          if(result!=None):
              if(inputResult.value!=''):
                setResult = set()
                for x in inputResult.value.strip().split(";"):
                  f = get_formula(x) 
                  if f!=None:
                    setResult.add(f)
                  else:
                    display(HTML(rf'<b><font color="red">{input_text_result_error}</font>'))
                    return    
              else:
                setResult = set()
              if(function(result)==setResult):
                display(HTML(rf'<b><font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<b><font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def check_def_formula_proof(input_proof='', height_layout='300px', language_pt=True):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description='Verificar' if language_pt else 'Check')
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:' if language_pt else 'Enter your proof:',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  if (language_pt):
    display(widgets.HTML('<h3>Digite sua demonstração de que uma fórmula pertence a linguagem da lógica:</h3>'))
  else:
    display(widgets.HTML('<h3>Enter your proof that a formula is in the propositional logic:</h3>'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result, errors = check_proof(input.value)
          if errors==[]:
            display(HTML(rf'<b><font color="blue">{result}</font>'))
          else:
            display(HTML(rf'<b><font color="red">{result}</font>'))
          # display(HTML(result))
          for er in errors:
            display(HTML(er))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          display(HTML (f'{result}'))
      else:
          pass
  run.on_click(on_button_run_clicked)

def display_formula_property(input_formula='', parentheses=False, language_pt=True):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Verificar")
  cSat = widgets.Checkbox(value=False, description='Satisfatível.')
  cVal = widgets.Checkbox(value=False, description='Válida.')
  cFals = widgets.Checkbox(value=False, description='Falsificável.')
  cInsat = widgets.Checkbox(value=False, description='Insatisfatível.')
  output = widgets.Output()
  
  try:
      formula = get_formula(input_formula)
      if(formula!=None):
        display(Markdown(fr'<b>Marque os itens abaixo que são verdadeiros para a fórmula ${formula.toLatex(parentheses=parentheses)}$'))
        display(cSat, cVal, cFals, cInsat,run, output)
      else:
        display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
  except ValueError:
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      erro = False
      if(is_satisfiable(formula)!=cSat.value):
        erro = True
        display(HTML(r'<b><font color="red">Revise a sua reposta sobre satisfatível.</font>'))  
      if(is_valid(formula)!=cVal.value):
        erro = True
        display(HTML(r'<b><font color="red">Revise a sua reposta sobre válida.</font>'))  
      if(is_falsiable(formula)!=cFals.value):
        erro = True
        display(HTML(r'<b><font color="red">Revise a sua reposta sobre falsificável.</font>'))  
      if(is_unsatisfiable(formula)!=cInsat.value):
        erro = True
        display(HTML(r'<b><font color="red">Revise a sua reposta sobre insatisfatível.</font>'))  
      if not erro:
        display(HTML(r'<b><font color="blue">Parabéns, você acertou todas as respostas!</font>'))
  run.on_click(on_button_run_clicked)


def display_truth_table(input_string='', language_pt=True):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Tabela-Verdade")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite sua fórmula',
      description='',
      layout=layout
      )
  cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  cSubformulas = widgets.Checkbox(value=True, description='Exibir Subfórmulas')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cSubformulas])
  
  display(HTML(r'<b>Digite sua fórmula para gerar a Tabela-Verdade:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      try:
          formula = get_formula(input.value)
          if(formula!=None):
              display(truth_table(formula, show_subformulas=cSubformulas.value,parentheses=cParentheses.value).style.hide(axis='index'))
          else:
            display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def display_formula_is_true(input_formula='', v=None, parentheses=False, response='', language_pt=True):
  run = widgets.Button(description="Verificar")
  cTrue = widgets.Checkbox(value=False, description='Verdadeira.')
  output = widgets.Output()
  
  try:
      formula = get_formula(input_formula)
      atoms = sorted([a.toString() for a in get_atoms(formula)])
#      atoms = sorted(list(get_atoms(formula)))
      vs = get_vs(formula)
      if(v==None):
        v = vs[randrange(0,len(vs))]

      if(formula!=None):
        sV = '~~'+',~'.join([f'v({a}) = {v[a]}' for a in atoms])
        display(HTML(fr'<b>Considere a função de valoração:'))
        display(Markdown(fr'<b>${sV}$'))
        display(Markdown(fr'<b>Marque o item abaixo se a fórmula ${formula.toLatex(parentheses=parentheses)}$ é verdadeira para a função de valoração.'))
        display(cTrue,run, output)
      else:
        display(HTML(r'<b><font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
  except ValueError:
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      if(v_bar(formula,v)!=cTrue.value):
        erro = True
        display(HTML(r'<b><font color="red">Você errou, revise a sua reposta.</font>'))  
      else:
        display(HTML(r'<b><font color="blue">Parabéns, você acertou todas as respostas!</font>'))
      if response!='':
         display(HTML(fr'<b>Resposta: {response}.'))
  run.on_click(on_button_run_clicked)

def display_truth_table_consequence_logic(input_string='', language_pt=True):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Verificar")
  input = widgets.Text(
      value=input_string,
      placeholder='Digite seu teorema',
      description='',
      layout=layout
      )
  cParentheses = widgets.Checkbox(value=False, description='Exibir Fórmula com Parênteses')
  cSubformulas = widgets.Checkbox(value=False, description='Exibir Subfórmulas')
  cTabelaVerdade = widgets.Checkbox(value=False, description='Exibir Tabela-Verdade')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cSubformulas, cTabelaVerdade])
  
  display(HTML(r'<b>Digite seu teorema:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      try:
          premises, conclusion = get_theorem(input.value)
          if(conclusion!=None):
              result= consequence_logic(conclusion,premises=premises)
              if(result==None):
                display(HTML(r'<b><font color="blue">O teorema é válido!</font>'))
                if(cTabelaVerdade.value):
                  df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)
                  display(df.style.hide(axis='index'))
              else:
                display(HTML(fr'<b><font color="red">O teorema é inválido. A linha {result} da Tabela-Verdade abaixo é um contraexemplo.</font>'))  
                df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)                
                display(df)
          else:
            display(HTML(r'<b><font color="red">A definição do teorema não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ F | F & F | F | F | F -> F | F <-> F | (F), onde P (em caixa alta) é um átomo e F é uma fórmula qualquer. Um Teorema é forma por uma lista de fórmula, |= e uma fórmula.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def display_is_countermodel(input_theorem, universe=set(), s={}, preds={}, language_pt=True):
  output = widgets.Output()
  
  try:
      display(HTML(fr'<b>Considere a interpretação:'))
      
      if language_pt:
        display(HTML(fr"<b>- Conjunto universo:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"<b>- Universe set:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      for p_key, p_values in preds.items():
        if p_values==1 or p_values==0:
           s_values = str(p_values)
        else:
           s_values = '{'+', '.join(['('+','.join([k for k in r])+')' if type(r)==tuple else '('+r+')' for r in sorted(list(p_values))])+'}'
        if language_pt:          
          display(HTML(fr"<b>- Predicado {p_key[0]}</b> = {s_values}")) 
        else:
          display(HTML(fr"<b>- Predicate {p_key[0]}</b> = {s_values}")) 

      if len(s)>0:
        if language_pt:
          display(HTML(fr'<b>- Variáveis:</b> {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'<b>- Variables:</b> {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
      premises, conclusion = get_theorem(input_theorem)

      if is_countermodel(premises,conclusion,universe,s, preds):
        if language_pt:
          display(HTML(fr'<b><font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
        else:
          display(HTML(fr'<b><font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
      else:
        if language_pt:
          display(HTML(fr'<b><font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
        else:
          display(HTML(fr'<b><font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
  except ValueError as error:
    display(HTML(fr'<b><font color="red">{error}</font>'))   
  else:
      pass


def display_truth_formulas(formulas, universe=set(), s={}, preds={}, language_pt=True):
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  cFormulas = [widgets.Checkbox(value=False, description=f) for f in formulas]
  output = widgets.Output()
  
  try:
      display(HTML(fr'<b>Considere a interpretação:</b>'))
      
      if language_pt:
        display(HTML(fr"<b>- Conjunto universo:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"<b>- Universe set:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      for p_key, p_values in preds.items():
        s_values = '{'+', '.join(['('+','.join([k for k in r])+')' if type(r)==tuple else '('+r+')' for r in sorted(list(p_values))])+'}'
        if language_pt:
          display(HTML(fr'<b>- Predicado {p_key[0]}</b>= {s_values}')) 
        else:
          display(HTML(fr'<b>- Predicate {p_key[0]}=</b> {s_values}')) 

      if len(s)>0:
        if language_pt:
          display(HTML(fr'<b>- Variáveis:</b> {", ".join(["<b>"+x_key+"</b>="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'<b>- Variables:</b> {", ".join(["<b>"+x_key+"</b>="+x_values for x_key, x_values in s.items()])}'))
      if language_pt:
        display(HTML(fr'<b>Marque as fórmulas abaixo que são verdadeiras para a interpretação acima:</b>'))
      else:
        display(HTML(fr'<b>Check the formulas below which are true for the above interpretation:</b>'))
      display(*tuple(cFormulas + [run, output]))
      l_formulas = [get_formula(f) for f in formulas]
  except ValueError:
      if language_pt:
        display(HTML(r'<b><font color="red">A definição de alguma das fórmulas não está correta</font>'))
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      erro = False
      erro_formulas = []
      formulas_sat = [sat(f,universe,s,preds) for f in l_formulas]
      
      for i in range(len(formulas)):
        if formulas_sat[i]!=cFormulas[i].value:
          erro = True
          erro_formulas.append(formulas[i])

      if not erro:
        if language_pt:
          display(HTML(r'<b><font color="blue">Parabéns, você acertou todas as respostas!</font></b>'))
        else:
          display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font></b>'))              
      else:
        if language_pt:
          display(HTML(r'<b><font color="red">Você errou as seguintes fórmulas:</font></b>'))  
        else:
          display(HTML(r'<b><font color="red">You got wrong the following fórmulas:</font></b>'))  
        s_formulas = '<br> '.join(erro_formulas)
        display(HTML(f'{s_formulas}'))  
  run.on_click(on_button_run_clicked)

def display_graph_truth_formulas(formulas, edges, universe=None, s={}, parentheses=False, language_pt=True):
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  cFormulas = [widgets.Checkbox(value=False, description=f) for f in formulas]
  output = widgets.Output()
  
  try:
      preds={}
      preds['E',2]= edges
      if language_pt:
        display(HTML(fr'<b>Considere o seguinte grafo:'))
      else:
        display(HTML(fr'<b>Consider the following graph:'))
        
      if universe==None:
        universe = set()
        for (x,y) in edges:
          universe.add(x)
          universe.add(y)      
          
      if language_pt:
        display(HTML(fr"- <b>Conjunto universo:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"- <b>Universe set:</b> {'{'+', '.join(sorted(list(universe)))+'}'}"))
      for p_key, p_values in preds.items():
        s_values = '{'+', '.join(['('+','.join([k for k in r])+')' if type(r)==tuple else '('+r+')' for r in sorted(list(p_values))])+'}'
        if language_pt:
          display(HTML(fr'<b>- Arcos {p_key[0]}</b>= {s_values}')) 
        else:
          display(HTML(fr'<b>- Edges {p_key[0]}=</b> {s_values}')) 

      if len(s)>0:
        if language_pt:
          display(HTML(fr'<b>- <b>Variáveis:</b> {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'<b>- <b>Variables:</b> {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
      display(visualiza_relacao(universe, edges))
      if language_pt:
        display(HTML(fr'<b>Marque as fórmulas abaixo que são verdadeiras para o grafo acima:'))
      else:
        display(HTML(fr'<b>Check the formulas below which are true for the above graph:'))

      display(*tuple(cFormulas + [run, output]))
      l_formulas = [get_formula(f) for f in formulas]
  except ValueError:
      if language_pt:
        display(HTML(r'<b><font color="red">A definição de alguma das fórmulas não está correta</font>'))
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      erro = False
      erro_formulas = []
      formulas_sat = [sat(f,universe,s,preds) for f in l_formulas]
      
      for i in range(len(formulas)):
        if formulas_sat[i]!=cFormulas[i].value:
          erro = True
          erro_formulas.append(formulas[i])
      if not erro:
        if language_pt:
          display(HTML(r'<b><font color="blue">Parabéns, você acertou todas as respostas!</font>'))
        else:
          display(HTML(r'<b><font color="blue">Congratulations, you got the question right!</font>'))              

      else:
        if language_pt:
          display(HTML(r'<b><font color="red">Você errou as seguintes fórmulas:</font>'))  
        else:
          display(HTML(r'<b><font color="red">You got wrong the following fórmulas:</font>'))  
        s_formulas = '<br>'.join(erro_formulas)
        display(HTML(f'{s_formulas}'))  
  run.on_click(on_button_run_clicked)


def parser_lista_strings(s):
  C_string = [x for x in s.strip().split(' ') if x!='']
  return [ int(x.strip()) if x.isdigit() else x.strip() for x in C_string] if C_string!=[''] else set()

def parser_conjunto_tuplas_strings(s):
  tuplas = [tuple(parser_lista_strings(x)) for x in s.strip().split(';')]
  return set(tuplas) if tuplas !=[()] else set() 

def produto_cartesiano(A, size):
  R = []
  A = list(A)  
  if size==1:
    return A
  for i in range(len(A)**size):
    R.append(tuple([A[i // (len(A)(size-j-1)) % len(A)] for j in range(size)]))
  return R

def display_countermodel_decoder(input_theorem, input_interpretation = '', height_layout='140px', language_pt=True):
  layout = widgets.Layout(width='90%', height=height_layout)
  output = widgets.Output()
  run = widgets.Button(description="Verificar" if language_pt else "Check")
  input = widgets.Textarea(
      value=input_interpretation,
      placeholder='Digite a interpretação' if language_pt else 'Enter the interpretation',
      description='',
      layout=layout
      )
  if language_pt:
    display(HTML(fr'<b>Apresente um contraexemplo para o teorema {input_theorem}'))
  else:
    display(HTML(fr'<b>Define a countermodel for the theorem {input_theorem}')) 
  premises, conclusion = get_theorem(input_theorem)
  signature_preds = get_signature_predicates(conclusion, premises)
  l_preds = sorted(list(signature_preds.keys()))
  if input_interpretation=='':
    if language_pt:
      input_string = "# Defina o conjunto universo:\nU = {}\n# Defina os predicados:"
    else: 
      input_string = "# Set the universe set:\nU = {}\n# Set the Predicates:"
    for p in l_preds:
        for arity in signature_preds[p]:
          input_string+=f"\n{p} = "+"{("+','.join([' ' for x in range(arity)])+")}"
    free_variables = conclusion.free_variables()
    for prem in premises:
      free_variables = free_variables.union(prem.free_variables())
    free_variables=sorted(list(free_variables))
    if len(free_variables)>0:
      if language_pt:
        input_string += "\n# Defina as variáveis:"
      else: 
        input_string += "\n# Set the variables:"
      for x in free_variables:
        input_string+=f"\n{x} = "
    input.value = input_string
  display(input, run, output)
  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      try:
        universe, preds, s  = decode_fo_interpretation(input.value)
        if is_countermodel(premises,conclusion,universe,s, preds):
          if language_pt:
            display(HTML(fr'<b><font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
          else:
            display(HTML(fr'<b><font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
        else:
          if language_pt:
            display(HTML(fr'<b><font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
          else:
            display(HTML(fr'<b><font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
      except ValueError as error:
        display(HTML(fr'<b><font color="red">{error}</font>'))   
      else:
          pass
  run.on_click(on_button_run_clicked)


def display_valid_model_decoder(input_theorem, input_interpretation = '', height_layout='140px', language_pt=True):
  layout = widgets.Layout(width='90%', height=height_layout)
  output = widgets.Output()
  run = widgets.Button(description="Verificar" if language_pt else "Check")
  input = widgets.Textarea(
      value=input_interpretation,
      placeholder='Digite a interpretação' if language_pt else 'Enter the interpretation',
      description='',
      layout=layout
      )
  if language_pt:
    display(HTML(fr'<b>Apresente uma interpretação para o teorema {input_theorem} que torne verdadeira a conclusão e cada uma das premissas.'))
  else:
    display(HTML(fr'<b>Define an interpretation for the theorem {input_theorem} that the conclusion and every premise are true.')) 
  premises, conclusion = get_theorem(input_theorem)
  signature_preds = get_signature_predicates(conclusion, premises)
  l_preds = sorted(list(signature_preds.keys()))
  if input_interpretation=='':
    if language_pt:
      input_string = "# Defina o conjunto universo:\nU = {}\n# Defina os predicados:"
    else: 
      input_string = "# Set the universe set:\nU = {}\n# Set the Predicates:"
    for p in l_preds:
        for arity in signature_preds[p]:
          input_string+=f"\n{p} = "+"{("+','.join([' ' for x in range(arity)])+")}"
    free_variables = conclusion.free_variables()
    for prem in premises:
      free_variables = free_variables.union(prem.free_variables())
    free_variables=sorted(list(free_variables))
    if len(free_variables)>0:
      if language_pt:
        input_string += "\n# Defina as variáveis:"
      else: 
        input_string += "\n# Set the variables:"
      for x in free_variables:
        input_string+=f"\n{x} = "
    input.value = input_string
  display(input, run, output)
  def on_button_run_clicked(_):
    output.clear_output()
    run.disabled=True
    with output:
      try:
        universe, preds, s  = decode_fo_interpretation(input.value)
        if is_valid_interpretation(premises,conclusion,universe,s, preds):
          if language_pt:
            display(HTML(fr'<b><font color="blue">Parabéns, a interpretração acima é uma interpretação válida para o teorema {input_theorem}!</font>'))
          else:
            display(HTML(fr'<b><font color="blue">Congratulations, the interpretation is a valid interpretation for the theorem {input_theorem}!</font>'))              
        else:
          if language_pt:
            display(HTML(fr'<b><font color="red">Infelizmente, você errou a questão! A interpretação não é uma interpretação válida para o teorema {input_theorem}!</font>'))  
          else:
            display(HTML(fr'<b><font color="red">Unfortunately, you got the question wrong. The interpretation is not a valid interpretation for the theorem {input_theorem}!</font>'))  
      except ValueError as error:
        display(HTML(fr'<b><font color="red">{error}</font>'))   
      else:
          pass
  run.on_click(on_button_run_clicked)


def display_countermodel(input_theorem, language_pt=True):
  output = widgets.Output()
  output_interpretation = widgets.Output()
  output_variables = widgets.Output()
  output_run = widgets.Output()
  output_result = widgets.Output()
  layout = widgets.Layout(width='70%')
  layout2 = widgets.Layout(width='150px')
  layout3 = widgets.Layout(width='180px')
  continue_universe = widgets.Button(description="Continuar" if language_pt else "Continue")
  input_universe = widgets.Textarea(
      value='',
      placeholder='Digite o universo (separado por espaço)' if language_pt else "Enter the universe set",
      description='',
      layout=layout
      )
  run = widgets.Button(description="Verificar" if language_pt else "Check")
  if language_pt:
    display(HTML(fr'<b>Apresente um contraexemplo para o teorema {input_theorem}'))
  else:
    display(HTML(fr'<b>Define a countermodel for the theorem {input_theorem}')) 

  premises, conclusion = get_theorem(input_theorem)
  signature_preds = get_signature_predicates(conclusion,premises)
  w_preds = []
  l_preds = sorted(list(signature_preds.keys()))
  for p in l_preds:
    for arity in signature_preds[p]:
      w_preds.append(widgets.SelectMultiple(
        options=[],
        value=[],
        description=f'Predicado {p}' if language_pt else f'Predicate {p}',
        layout=layout3,
        disabled=False
        ))
  w_atoms = []  
  l_atoms = sorted(list(get_signature_propositional_atoms(conclusion,premises)))
  for p in l_atoms:
    w_atoms.append(widgets.Dropdown(
      options=[('1',1),('0',0)],
      value=1,
      description=f'Predicado {p}' if language_pt else f'Predicate {p}',
      layout=layout2,
      disabled=False
      ))
  free_variables = conclusion.free_variables()
  for prem in premises:
    free_variables = free_variables.union(prem.free_variables())
  free_variables=sorted(list(free_variables))
  w_variables = []
  for x in free_variables:
    w_variables.append(widgets.Dropdown(
      options=[],
      description=f'Variável {x}' if language_pt else f'Variable {x}',
      layout=layout2,
      disabled=False
      ))

  input_universe.value = ''
  if language_pt:
    display(HTML(fr'<b>Entre com o conjunto universo:'))
  else:
    display(HTML(fr'<b>Enter the universe set:'))
  display(widgets.HBox([input_universe, continue_universe]))

  display(output)
  display(output_interpretation)
  display(output_variables)
  display(output_run)
  display(output_result)

  
  def on_button_continue_universe_clicked(_):
    output_interpretation.clear_output()
    with output_interpretation:
      input_universe.disabled = True
      continue_universe.disabled = True
      universe = parser_lista_strings(input_universe.value)
      if language_pt:
        text_pred = HTML(fr'<b>Para cada predicado abaixo, marque as tuplas que são válidas para o predicado.')
      else:
        text_pred = HTML(fr'<b>For each predicate below, check the tuples that are true for the predicate.')
      i=0
      for p in l_preds:
        for arity in signature_preds[p]:
          pc = produto_cartesiano(universe, arity)
          d_pc ={}
          for r in pc:
            if type(r)!=tuple:
              d_pc['('+r+')'] = r  
            else:
              d_pc['('+','.join([k for k in r])+')'] = r
          w_preds[i].options = d_pc 
          i+=1
      display(text_pred)
      display(widgets.HBox(w_preds+w_atoms))
      # display(widgets.HBox(w_atoms))

    with output_variables:
      if len(free_variables)>0:
        i=0
        for x in free_variables:
          w_variables[i].options= universe
          i+=1
        if language_pt:
          text_var = HTML(fr'<b>Para cada variável abaixo, selecione a interpretação da variável.')
        else:
          text_var = HTML(fr'<b>For each variable below, select the interpretation for the variable.')
        display(text_var)
        display(widgets.HBox(w_variables))
    with output_run:
      # display(HTML(fr'<b>Verifique se a interpretação acima é um contraexemplo para o teorema'))
      display(run)

  def on_button_run_clicked(_):
      output_result.clear_output()
      preds = dict()
      i = 0
      for pred in l_preds:
        for arity in signature_preds[pred]:
          preds[pred,arity] = set(w_preds[i].value)
          i+=1
      i = 0
      for pred in l_atoms:
        preds[pred] = w_atoms[i].value
        i+=1
      s = dict()
      i = 0
      for dVar in free_variables:
        s[dVar] = w_variables[i].value
        i+=1
      universe = parser_lista_strings(input_universe.value)
      with output_result:
        if is_countermodel(premises,conclusion,universe,s, preds):
          if language_pt:
            display(HTML(fr'<b><font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
          else:
            display(HTML(fr'<b><font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
        else:
          if language_pt:
            display(HTML(fr'<b><font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
          else:
            display(HTML(fr'<b><font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
      
  continue_universe.on_click(on_button_continue_universe_clicked)
  run.on_click(on_button_run_clicked)


