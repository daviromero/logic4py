import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
from logic4py.parser_formula import get_formula
from logic4py.parser_theorem import get_theorem
from logic4py.parser_def_formula import check_proof
from logic4py.formula import get_atoms, v_bar, get_vs, consequence_logic, truth_table, is_falsiable, is_unsatisfiable, is_satisfiable, is_valid, sat, is_countermodel, get_signature_predicates, get_propositional_atoms, get_signature_propositional_atoms
from logic4py.decoder import decode_fo_interpretation
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
    display(HTML(rf'O termo {input_term} é substituível para a variável {input_var} na fórmula {input_formula}:'))
  else:
    display(HTML(rf'The term {input_term} is substitutable for the variable {input_var} in the formula {input_formula}:'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = get_formula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and (cResult.value=='Sim' or cResult.value=='Yes')):
              if language_pt:
               display(HTML(r'<font color="blue">Parabéns você acertou a questão!</font>')) 
               display(HTML(rf'O termo {input_term} é substituível para a variável {input_var} na fórmula {input_formula}.'))
              else:
                display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))
                display(HTML(rf'The term {input_term} is substitutable for the variable {input_var} in the formula {input_formula}.'))
            elif not f.is_substitutable(input_var,input_term) and (cResult.value=='Não' or cResult.value=='No'):
              if language_pt:
                display(HTML(r'<font color="blue">Parabéns você acertou a questão!</font>'))              
                display(HTML(rf'O termo {input_term} não é substituível para a variável {input_var} na fórmula {input_formula}.'))
              else:
                display(HTML(r'<font color="blue">Congratulations you got the question right!</font>'))              
                display(HTML(rf'The term {input_term} is not substitutable for the variable {input_var} in the formula {input_formula}.'))
            else:
              if language_pt:
                display(HTML(rf'<font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(rf'<font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">The formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
  
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
    display(HTML(rf'Digite o conjunto de variávels da fórmula {input_formula}:'))
    display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'Enter the set of variables of the formula {input_formula}:'))
    display(HTML(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
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
    display(HTML(rf'Digite o conjunto de variávels livres da fórmula {input_formula}:'))
    display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'Enter the set of the free variables of the formula {input_formula}:'))
    display(HTML(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
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
    display(HTML(rf'Digite o conjunto de variávels ligadas da fórmula {input_formula}:'))
    display(HTML(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(HTML(rf'Enter the set of bound variables of the formula {input_formula}:'))
    display(HTML(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))              
            else:
              if language_pt:
                display(HTML(r'<font color="red">Infelizmente, você errou a questão.</font>'))
              else:
                display(HTML(r'<font color="red">Unfortunately, you got the question wrong.</font>'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
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
    display(HTML(rf'Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:'))
  else:
    display(HTML(rf'Enter the formula that results from substitution the variable {input_var} with the term {input_term} in the formula {input_formula}:'))
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
                display(HTML(r'<font color="blue">Parabéns essa é a subtituição correta:</font>'))              
              else:
                display(HTML(r'<font color="blue">Congratulations this is the correct substitution:</font>'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(HTML(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              if language_pt:
                display(HTML(rf'<font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>'))
              else:
                display(HTML(rf'<font color="red">Formula {result.toString()} is not the result of substitution {input_var} with {input_term} in the formula {input_formula}.</font>'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

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
    questao = r'Considere as seguintes afirmações:' if language_pt else r'Consider the following statements:'
    i = 1
    for assumption in input_assumptions:
        questao += f'\n1. {assumption}'
        i+=1
    display(Markdown(questao))
    questao= r'Podemos concluir que a afirmação abaixo segue logicamente das afirmações acima?' if language_pt else r'Can we conclude that the statement below follows logically from the statements above?'
    display(Markdown(questao))
    questao =f'\n{i}. {input_conclusion}'
    display(HTML(questao))
    display(widgets.HBox([cResult,wButtons]), output)

    def on_button_run_clicked(_):
        output.clear_output()
        with output:
            if (cResult.value==None):
                if language_pt:
                    display(HTML(r'<font color="red">Escolha uma das alternativas! Tente novamente!</font>'))
                else:
                    display(HTML(r'<font color="red">Choose an option! Try again!</font>'))
            elif(result_value==(cResult.value=='Sim' or cResult.value=='Yes')):
                if language_pt:
                    display(HTML(r'<font color="blue">Parabéns, você acertou a questão.</font>'))
                else: 
                    display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))
                cResult.disabled = True
                run.disabled = True
            else:
                if language_pt:
                    display(HTML(r'<font color="red">Infelizmente, você errou a questão.</font>'))
                else:
                    display(HTML(r'<font color="red">Unfortunately, you got the question wrong.</font>'))
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
    display(HTML(r'Digite sua fórmula:'))
  else:
    display(HTML(r'Enter your formula:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value)
          if(result!=None):
              if language_pt:
                display(HTML(r'<font color="blue">Parabéns! Esta é uma fórmula da lógica:</font>'))
              else:
                display(HTML(r'<font color="blue">Congratulations this is a formula of logic:</font>'))

              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                print(result.toString(parentheses=cParentheses.value))
                #display(HTML(rf'{result.toString(parentheses=cParentheses.value)}'))
          else:
            if language_pt:
              display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
            else:
              display(HTML(r'<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>'))
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
  
  display(HTML(rf'{input_text_question}'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          if(result!=None):
              
              if(str(function(result))==inputResult.value.strip()):
                display(HTML(rf'<font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
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
  
  display(HTML(rf'{input_text_question}:'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          resultAtom = get_formula(inputAtom.value.strip())
          if(result!=None):
              
              if(str(function(result,resultAtom))==inputResult.value.strip()):
                display(HTML(rf'<font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
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

  display(HTML(rf'{input_text_question}:'))
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
                    display(HTML(rf'<font color="red">{input_text_result_error}</font>'))
                    return    
              else:
                setResult = set()
              if(function(result)==setResult):
                display(HTML(rf'<font color="blue">{input_text_result}</font>'))
              else:
                display(HTML(rf'<font color="red">{input_text_result_error}</font>'))
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def check_def_formula_proof(input_proof='', height_layout='300px', language_pt=True):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Verificar")
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:' if language_pt else 'Enter your proof:',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(widgets.HTML('<h3>Digite sua demonstração de que uma fórmula pertence a linguagem da lógica:</h3>'), 
          input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result, errors = check_proof(input.value)
          display(HTML(result))
          for er in errors:
            print(er)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
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
        display(Markdown(fr'Marque os itens abaixo que são verdadeiros para a fórmula ${formula.toLatex(parentheses=parentheses)}$'))
        display(cSat, cVal, cFals, cInsat,run, output)
      else:
        display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
  except ValueError:
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      erro = False
      if(is_satisfiable(formula)!=cSat.value):
        erro = True
        display(HTML(r'<font color="red">Revise a sua reposta sobre satisfatível.</font>'))  
      if(is_valid(formula)!=cVal.value):
        erro = True
        display(HTML(r'<font color="red">Revise a sua reposta sobre válida.</font>'))  
      if(is_falsiable(formula)!=cFals.value):
        erro = True
        display(HTML(r'<font color="red">Revise a sua reposta sobre falsificável.</font>'))  
      if(is_unsatisfiable(formula)!=cInsat.value):
        erro = True
        display(HTML(r'<font color="red">Revise a sua reposta sobre insatisfatível.</font>'))  
      if not erro:
        display(HTML(r'<font color="blue">Parabéns, você acertou todas as respostas!</font>'))
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
  
  display(HTML(r'Digite sua fórmula para gerar a Tabela-Verdade:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          formula = get_formula(input.value)
          if(formula!=None):
              display(truth_table(formula, show_subformulas=cSubformulas.value,parentheses=cParentheses.value).style.hide_index())
          else:
            display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>'))
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
        display(HTML(fr'Considere a função de valoração:'))
        display(Markdown(fr'${sV}$'))
        display(Markdown(fr'Marque o item abaixo se a fórmula ${formula.toLatex(parentheses=parentheses)}$ é verdadeira para a função de valoração.'))
        display(cTrue,run, output)
      else:
        display(HTML(r'<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>'))
  except ValueError:
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      if(v_bar(formula,v)!=cTrue.value):
        erro = True
        display(HTML(r'<font color="red">Você errou, revise a sua reposta.</font>'))  
      else:
        display(HTML(r'<font color="blue">Parabéns, você acertou todas as respostas!</font>'))
      if response!='':
         display(HTML(fr'Resposta: {response}.'))
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
  
  display(HTML(r'Digite seu teorema:'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          premises, conclusion = get_theorem(input.value)
          if(conclusion!=None):
              result= consequence_logic(conclusion,premises=premises)
              if(result==None):
                display(HTML(r'<font color="blue">O teorema é válido!</font>'))
                if(cTabelaVerdade.value):
                  df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)
                  display(df.style.hide_index())
              else:
                display(HTML(fr'<font color="red">O teorema é inválido. A linha {result} da Tabela-Verdade abaixo é um contraexemplo.</font>'))  
                df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)                
                display(df)
          else:
            display(HTML(r'<font color="red">A definição do teorema não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ F | F & F | F | F | F -> F | F <-> F | (F), onde P (em caixa alta) é um átomo e F é uma fórmula qualquer. Um Teorema é forma por uma lista de fórmula, |= e uma fórmula.</font>'))
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
      display(HTML(fr'Considere a interpretação:'))
      
      if language_pt:
        display(HTML(fr"- Conjunto universo: {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"- Universe set: {'{'+', '.join(sorted(list(universe)))+'}'}"))
      for p_key, p_values in preds.items():
        if p_values==1 or p_values==0:
           s_values = str(p_values)
        else:
           s_values = '{'+', '.join(['('+','.join([k for k in r])+')' if type(r)==tuple else '('+r+')' for r in sorted(list(p_values))])+'}'
        if language_pt:          
          display(HTML(fr"- Predicado {p_key[0]}= {s_values}")) 
        else:
          display(HTML(fr"- Predicate {p_key[0]}= {s_values}")) 

      if len(s)>0:
        if language_pt:
          display(HTML(fr'- Variáveis: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'- Variables: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
      premises, conclusion = get_theorem(input_theorem)

      if is_countermodel(premises,conclusion,universe,s, preds):
        if language_pt:
          display(HTML(fr'<font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
        else:
          display(HTML(fr'<font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
      else:
        if language_pt:
          display(HTML(fr'<font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
        else:
          display(HTML(fr'<font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
  except ValueError as error:
    display(HTML(fr'<font color="red">{error}</font>'))   
  else:
      pass


def display_truth_formulas(formulas, universe=set(), s={}, preds={}, language_pt=True):
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  cFormulas = [widgets.Checkbox(value=False, description=f) for f in formulas]
  output = widgets.Output()
  
  try:
      display(HTML(fr'Considere a interpretação:'))
      
      if language_pt:
        display(HTML(fr"- Conjunto universo: {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"- Universe set: {'{'+', '.join(sorted(list(universe)))+'}'}"))
      for p_key, p_values in preds.items():
        s_values = '{'+', '.join(['('+','.join([k for k in r])+')' if type(r)==tuple else '('+r+')' for r in sorted(list(p_values))])+'}'
        if language_pt:
          display(HTML(fr'- Predicado {p_key[0]}= {s_values}')) 
        else:
          display(HTML(fr'- Predicate {p_key[0]}= {s_values}')) 

      if len(s)>0:
        if language_pt:
          display(HTML(fr'- Variáveis: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'- Variables: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
      if language_pt:
        display(HTML(fr'Marque as fórmulas abaixo que são verdadeiras para o grafo acima:'))
      else:
        display(HTML(fr'Check the formulas below which are true for the above graph:'))
      display(*tuple(cFormulas + [run, output]))
      l_formulas = [get_formula(f) for f in formulas]
  except ValueError:
      if language_pt:
        display(HTML(r'<font color="red">A definição de alguma das fórmulas não está correta</font>'))
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
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
          display(HTML(r'<font color="blue">Parabéns, você acertou todas as respostas!</font>'))
        else:
          display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))              
      else:
        if language_pt:
          display(HTML(r'<font color="red">Você errou as seguintes fórmulas:</font>'))  
        else:
          display(HTML(r'<font color="red">You got wrong the following fórmulas:</font>'))  
        s_formulas = ', '.join(erro_formulas)
        display(HTML(f'{s_formulas}'))  
  run.on_click(on_button_run_clicked)

def display_graph_truth_formulas(formulas, arcs, universe=None, s={}, parentheses=False, language_pt=True):
  run = widgets.Button(description="Verificar") if language_pt else widgets.Button(description="Check")
  cFormulas = [widgets.Checkbox(value=False, description=f) for f in formulas]
  output = widgets.Output()
  
  try:
      preds={}
      preds['E',2]= arcs
      if language_pt:
        display(HTML(fr'Considere o seguinte grafo:'))
      else:
        display(HTML(fr'Consider the following graph:'))
        
      if universe==None:
        universe = set()
        for (x,y) in arcs:
          universe.add(x)
          universe.add(y)      
          
      if language_pt:
        display(HTML(fr"- Conjunto universo: {'{'+', '.join(sorted(list(universe)))+'}'}"))
      else:
        display(HTML(fr"- Universe set: {'{'+', '.join(sorted(list(universe)))+'}'}"))

      display(visualiza_relacao(universe, arcs))
      if len(s)>0:
        if language_pt:
          display(HTML(fr'- Variáveis: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
        else:
          display(HTML(fr'- Variables: {", ".join([x_key+"="+x_values for x_key, x_values in s.items()])}'))
      if language_pt:
        display(HTML(fr'Marque as fórmulas abaixo que são verdadeiras para o grafo acima:'))
      else:
        display(HTML(fr'Check the formulas below which are true for the above graph:'))

      display(*tuple(cFormulas + [run, output]))
      l_formulas = [get_formula(f) for f in formulas]
  except ValueError:
      if language_pt:
        display(HTML(r'<font color="red">A definição de alguma das fórmulas não está correta</font>'))
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      print (f'{result}')
  else:
      pass

  def on_button_run_clicked(_):
    output.clear_output()
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
          display(HTML(r'<font color="blue">Parabéns, você acertou todas as respostas!</font>'))
        else:
          display(HTML(r'<font color="blue">Congratulations, you got the question right!</font>'))              

      else:
        if language_pt:
          display(HTML(r'<font color="red">Você errou as seguintes fórmulas:</font>'))  
        else:
          display(HTML(r'<font color="red">You got wrong the following fórmulas:</font>'))  
        s_formulas = ', '.join(erro_formulas)
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

def display_countermodel_decoder(input_theorem, input_interpretation = '', height_layout='300px', language_pt=True):
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
    display(HTML(fr'Apresente um contraexemplo para o teorema {input_theorem}'))
  else:
    display(HTML(fr'Define a countermodel for the theorem {input_theorem}')) 
  premises, conclusion = get_theorem(input_theorem)
  signature_preds = get_signature_predicates(conclusion, premises)
  l_preds = sorted(list(signature_preds.keys()))
  if input_interpretation=='':
    if language_pt:
      input_string = "#Defina o conjunto universo:\nU = {}\n#Defina os predicados:"
    else: 
      input_string = "#Set the universe set:\nU = {}\n#Set the Predicates:"
    for p in l_preds:
        for arity in signature_preds[p]:
          input_string+=f"\n{p} = "+"{("+','.join([' ' for x in range(arity)])+")}"
    free_variables = conclusion.free_variables()
    for prem in premises:
      free_variables = free_variables.union(prem.free_variables())
    free_variables=sorted(list(free_variables))
    if len(free_variables)>0:
      if language_pt:
        input_string += "\n#Defina as variáveis:"
      else: 
        input_string += "\n#Set the variables:"
      for x in free_variables:
        input_string+=f"\n{x} = "
    input.value = input_string
  display(input, run, output)
  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
        universe, preds, s  = decode_fo_interpretation(input.value)
        if is_countermodel(premises,conclusion,universe,s, preds):
          if language_pt:
            display(HTML(fr'<font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
          else:
            display(HTML(fr'<font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
        else:
          if language_pt:
            display(HTML(fr'<font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
          else:
            display(HTML(fr'<font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
      except ValueError as error:
        display(HTML(fr'<font color="red">{error}</font>'))   
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
    display(HTML(fr'Apresente um contraexemplo para o teorema {input_theorem}'))
  else:
    display(HTML(fr'Define a countermodel for the theorem {input_theorem}')) 

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
    display(HTML(fr'Entre com o conjunto universo:'))
  else:
    display(HTML(fr'Enter the universe set:'))
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
        text_pred = HTML(fr'Para cada predicado abaixo, marque as tuplas que são válidas para o predicado.')
      else:
        text_pred = HTML(fr'For each predicate below, check the tuples that are true for the predicate.')
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
          text_var = HTML(fr'Para cada variável abaixo, selecione a interpretação da variável.')
        else:
          text_var = HTML(fr'For each variable below, select the interpretation for the variable.')
        display(text_var)
        display(widgets.HBox(w_variables))
    with output_run:
      # display(HTML(fr'Verifique se a interpretação acima é um contraexemplo para o teorema'))
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
            display(HTML(fr'<font color="blue">Parabéns, a interpretração acima é um contraexemplo para o teorema {input_theorem}!</font>'))
          else:
            display(HTML(fr'<font color="blue">Congratulations, the interpretation is a countermodel of the theorem {input_theorem}!</font>'))              
        else:
          if language_pt:
            display(HTML(fr'<font color="red">Infelizmente, você errou a questão! A interpretação não é um contraexemplo para o teorema {input_theorem}!</font>'))  
          else:
            display(HTML(fr'<font color="red">Unfortunately, you got the question wrong. The interpretation is not a countermodel of the theorem {input_theorem}!</font>'))  
      
  continue_universe.on_click(on_button_continue_universe_clicked)
  run.on_click(on_button_run_clicked)



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
