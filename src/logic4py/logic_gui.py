import ipywidgets as widgets
from IPython.display import display, Markdown
from logic4py.parser_formula import get_formula
from logic4py.parser_theorem import get_theorem
from logic4py.parser_def_formula import check_proof
from logic4py.formula import get_atoms, v_bar, get_vs, consequence_logic, truth_table, is_falsiable, is_unsatisfiable, is_satisfiable, is_valid
from random import randrange
import traceback

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
    display(Markdown(rf'**A variável {input_var} é substituível pelo termo {input_term} na fórmula {input_formula}:**'))
  else:
    display(Markdown(rf'**Variable {input_var} is substitutable by the term {input_term} in the formula {input_formula}:**'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = get_formula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and (cResult.value=='Sim' or cResult.value=='Yes')):
              if language_pt:
               display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**')) 
               display(Markdown(rf'A variável {input_var} **é substituível** pelo termo {input_term} na fórmula {input_formula}.'))                          
              else:
                display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
                display(Markdown(rf'The variable {input_var} **is substitutable** by the term {input_term} in the formula {input_formula}.'))              
            elif not f.is_substitutable(input_var,input_term) and (cResult.value=='Não' or cResult.value=='No'):
              if language_pt:
                display(Markdown(r'**<font color="blue">Parabéns você acertou a questão!</font>**'))              
                display(Markdown(rf'A variável {input_var} **não é substituível** pelo termo {input_term} na fórmula {input_formula}.')) 
              else:
                display(Markdown(r'**<font color="blue">Congratulations you got the question right!</font>**'))              
                display(Markdown(rf'The variable {input_var} **is not substitutable** by the term {input_term} in the formula {input_formula}.')) 
            else:
              if language_pt:
                display(Markdown(rf'**<font color="red">Infelizmente, você errou a questão.</font>**'))
              else:
                display(Markdown(rf'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">The formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
  
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
    display(Markdown(rf'**Digite o conjunto de variávels da fórmula {input_formula}:**'))
    display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(Markdown(rf'**Enter the set of variables of the formula {input_formula}:**'))
    display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(Markdown('<font color="blue">**Parabéns, você acertou a questão.**</font>'))
              else:
                display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              if language_pt:
                display(Markdown(r'**<font color="red">Infelizmente, você errou a questão.</font>**'))
              else:
                display(Markdown(r'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
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
    display(Markdown(rf'**Digite o conjunto de variávels livres da fórmula {input_formula}:**'))
    display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(Markdown(rf'**Enter the set of the free variables of the formula {input_formula}:**'))
    display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(Markdown('<font color="blue">**Parabéns, você acertou a questão.**</font>'))
              else:
                display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              if language_pt:
                display(Markdown(r'**<font color="red">Infelizmente, você errou a questão.</font>**'))
              else:
                display(Markdown(r'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
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
    display(Markdown(rf'**Digite o conjunto de variávels ligadas da fórmula {input_formula}:**'))
    display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
  else:
    display(Markdown(rf'**Enter the set of bound variables of the formula {input_formula}:**'))
    display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
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
                display(Markdown('<font color="blue">**Parabéns, você acertou a questão.**</font>'))
              else:
                display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              if language_pt:
                display(Markdown(r'**<font color="red">Infelizmente, você errou a questão.</font>**'))
              else:
                display(Markdown(r'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
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
    display(Markdown(rf'**Digite a fórmula que é resultado da substituição da variável {input_var} pelo termo {input_term} na fórmula {input_formula}:**'))
  else:
    display(Markdown(rf'**Enter the formula that results from substitution the variable {input_var} with the term {input_term} in the formula {input_formula}:**'))
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
                display(Markdown(r'**<font color="blue">Parabéns essa é a subtituição correta:</font>**'))              
              else:
                display(Markdown(r'**<font color="blue">Congratulations this is the correct substitution:</font>**'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(Markdown(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              if language_pt:
                display(Markdown(rf'**<font color="red">A fórmula {result.toString()} não é o resultado da substituição de {input_var} por {input_term} na fórmula {input_formula}.</font>**'))
              else:
                display(Markdown(rf'**<font color="red">Formula {result.toString()} is not the result of substitution {input_var} with {input_term} in the formula {input_formula}.</font>**'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
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
    questao = r'**Considere as seguintes afirmações:**' if language_pt else r'**Consider the following statements:**'
    i = 1
    for assumption in input_assumptions:
        questao += f'\n1. {assumption}'
        i+=1
    display(Markdown(questao))
    questao= r'**Podemos concluir que a afirmação abaixo segue logicamente das afirmações acima?**' if language_pt else r'**Can we conclude that the statement below follows logically from the statements above?**'
    display(Markdown(questao))
    questao =f'\n{i}. {input_conclusion}'
    display(Markdown(questao))
    display(widgets.HBox([cResult,wButtons]), output)

    def on_button_run_clicked(_):
        output.clear_output()
        with output:
            if (cResult.value==None):
                if language_pt:
                    display(Markdown(r'**<font color="red">Escolha uma das alternativas! Tente novamente!</font>**'))
                else:
                    display(Markdown(r'**<font color="red">Choose an option! Try again!</font>**'))
            elif(result_value==(cResult.value=='Sim' or cResult.value=='Yes')):
                if language_pt:
                    display(Markdown(r'**<font color="blue">Parabéns, você acertou a questão.</font>**'))
                else: 
                    display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))
                cResult.disabled = True
                run.disabled = True
            else:
                if language_pt:
                    display(Markdown(r'**<font color="red">Infelizmente, você errou a questão.</font>**'))
                else:
                    display(Markdown(r'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
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
    display(Markdown(r'**Digite sua fórmula:**'))
  else:
    display(Markdown(r'**Enter your formula:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value)
          if(result!=None):
              if language_pt:
                display(Markdown(r'**<font color="blue">Parabéns! Esta é uma fórmula da lógica:</font>**'))
              else:
                display(Markdown(r'**<font color="blue">Congratulations this is a formula of logic:</font>**'))

              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                print(result.toString(parentheses=cParentheses.value))
                #display(Markdown(rf'{result.toString(parentheses=cParentheses.value)}'))
          else:
            if language_pt:
              display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
            else:
              display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
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
  
  display(Markdown(rf'**{input_text_question}**'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          if(result!=None):
              
              if(str(function(result))==inputResult.value.strip()):
                display(Markdown(rf'**<font color="blue">{input_text_result}</font>**'))
              else:
                display(Markdown(rf'**<font color="red">{input_text_result_error}</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
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
  
  display(Markdown(rf'**{input_text_question}:**'))
  display(wInputs, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = get_formula(input.value.strip())
          resultAtom = get_formula(inputAtom.value.strip())
          if(result!=None):
              
              if(str(function(result,resultAtom))==inputResult.value.strip()):
                display(Markdown(rf'**<font color="blue">{input_text_result}</font>**'))
              else:
                display(Markdown(rf'**<font color="red">{input_text_result_error}</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
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

  display(Markdown(rf'**{input_text_question}:**'))
  display(Markdown(r'Cada elemento do seu conjunto deve ser separado por ; (ponto-e-vírgula)'))
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
                    display(Markdown(rf'**<font color="red">{input_text_result_error}</font>**'))
                    return    
              else:
                setResult = set()
              if(function(result)==setResult):
                display(Markdown(rf'**<font color="blue">{input_text_result}</font>**'))
              else:
                display(Markdown(rf'**<font color="red">{input_text_result_error}</font>**'))
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
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
          display(Markdown(result))
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
        display(Markdown(fr'**Marque os itens abaixo que são verdadeiros para a fórmula ${formula.toLatex(parentheses=parentheses)}$**'))
        display(cSat, cVal, cFals, cInsat,run, output)
      else:
        display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
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
        display(Markdown(r'**<font color="red">Revise a sua reposta sobre satisfatível.</font>**'))  
      if(is_valid(formula)!=cVal.value):
        erro = True
        display(Markdown(r'**<font color="red">Revise a sua reposta sobre válida.</font>**'))  
      if(is_falsiable(formula)!=cFals.value):
        erro = True
        display(Markdown(r'**<font color="red">Revise a sua reposta sobre falsificável.</font>**'))  
      if(is_unsatisfiable(formula)!=cInsat.value):
        erro = True
        display(Markdown(r'**<font color="red">Revise a sua reposta sobre insatisfatível.</font>**'))  
      if not erro:
        display(Markdown(r'**<font color="blue">Parabéns, você acertou todas as respostas!</font>**'))
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
  
  display(Markdown(r'**Digite sua fórmula para gerar a Tabela-Verdade:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          formula = get_formula(input.value)
          if(formula!=None):
              display(truth_table(formula, show_subformulas=cSubformulas.value,parentheses=cParentheses.value).style.hide_index())
          else:
            display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q (em caixa alta) são átomos.</font>**'))
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
        sV = ''
        for a in atoms:
          sV+= '~~$v('+a+') = '+str(int(v[a]))+'$,'
        display(Markdown(fr'**Considere a função de valoração:**'))
        display(Markdown(fr'${sV}$'))
        display(Markdown(fr'**Marque o item abaixo se a fórmula ${formula.toLatex(parentheses=parentheses)}$ é verdadeira para a função de valoração.**'))
        display(cTrue,run, output)
      else:
        display(Markdown(r'**<font color="red">A definição da fórmula não está correta, verifique se todas regras foram aplicadas corretamente. <br>Lembre-se que uma fórmula é definida pela seguinte BNF: <br>F :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), <br>onde P,Q (em caixa alta) são átomos.</font>**'))
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
        display(Markdown(r'**<font color="red">Você errou, revise a sua reposta.</font>**'))  
      else:
        display(Markdown(r'**<font color="blue">Parabéns, você acertou todas as respostas!</font>**'))
      if response!='':
         display(Markdown(fr'**Resposta:** {response}.'))
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
  
  display(Markdown(r'**Digite seu teorema:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          premises, conclusion = get_theorem(input.value)
          if(conclusion!=None):
              result= consequence_logic(conclusion,premises=premises)
              if(result==None):
                display(Markdown(r'**<font color="blue">O teorema é válido!</font>**'))
                if(cTabelaVerdade.value):
                  df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)
                  display(df.style.hide_index())
              else:
                display(Markdown(fr'**<font color="red">O teorema é inválido. A linha {result} da Tabela-Verdade abaixo é um contra-exemplo.</font>**'))  
                df = truth_table(conclusion,premises=premises, show_subformulas=cSubformulas.value,parentheses=cParentheses.value)                
                display(df)
          else:
            display(Markdown(r'**<font color="red">A definição do teorema não está correta, verifique se todas regras foram aplicadas corretamente. Lembre-se que uma fórmula é definida pela seguinte BNF: F :== P | ~ F | F & F | F | F | F -> F | F <-> F | (F), onde P (em caixa alta) é um átomo e F é uma fórmula qualquer. Um Teorema é forma por uma lista de fórmula, |= e uma fórmula.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
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