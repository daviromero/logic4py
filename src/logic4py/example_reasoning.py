EXAMPLES = {}

EXAMPLES['q1_ex'] = {  
    'input_assumptions_pt': ['Se está chovendo, então a rua está molhada.','Está chovendo.'], 
    'input_conclusion_pt' : 'A rua está molhada.',
    'input_assumptions_en': ["If it's raining, then the street is wet.","It's raining"],
    'input_conclusion_en' : "The street is wet.",
    'result_value': True
    }

EXAMPLES['q2_ex'] = {  
    'input_assumptions_pt': ['Se C, então M','C'], 
    'input_conclusion_pt' :  'M',
    'input_assumptions_en': ['If C, then M','C'],
    'input_conclusion_en' :  'M',
    'result_value': True
    }

EXAMPLES['q3_ex'] = {  
    'input_assumptions_pt': ['Se $\\varphi$ então $\\psi$', '$\\varphi$'], 
    'input_conclusion_pt' : '$\\psi$',
    'input_assumptions_en': ['If $\\varphi$ then $\\psi$', '$\\varphi$'],
    'input_conclusion_en' : '$\\psi$',
    'result_value': True
    }

EXAMPLES['q4_ex'] = {  
    'input_assumptions_pt': ['Se o trem tivesse chegado atrasado e não houvesse táxi na estação, então John se atrasaria para seu compromisso.',
                                'John não se atrasou para seu compromisso.','O trem chegou atrasado.'],
    'input_conclusion_pt' : 'Havia táxis na estação.',
    'input_assumptions_en': ['If the train was late and there was no cab at the station, then John would be late for his appointment.',
                                'John was not late for his appointment.','The train arrived late.'],
    'input_conclusion_en' : 'There was a cab at the station.',
    'result_value': True
    }

EXAMPLES['q5_ex'] = {  
    'input_assumptions_pt': ['Se tivesse chovendo e Jane não estivesse com seu guarda-chuva, então ela se molharia.',
                                'Jane não está molhada.','Está chovendo.'], 
    'input_conclusion_pt' : 'Jane está com seu guarda-chuva.',
    'input_assumptions_en': ["If it was raining and Jane didn't have her umbrella, then she would get wet.",
                                'Jane is not wet.',"It's raining."],
    'input_conclusion_en' : 'Jane has her umbrella.',
    'result_value': True
    }


EXAMPLES['q6_ex'] = {  
    'input_assumptions_pt': ['$(\\varphi\\wedge\\lnot\\psi)\\rightarrow\\sigma$','$\\lnot\\sigma$', '$\\varphi$'],
    'input_conclusion_pt' : '$\\psi$',
    'input_assumptions_en': ['$(\\varphi\\wedge\\lnot\\psi)\\rightarrow\\sigma$','$\\lnot\\sigma$', '$\\varphi$'] ,
    'input_conclusion_en' : '$\\psi$',
    'result_value': True
    }

EXAMPLES['q1'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.', 
                                'Os produtos não ficaram mais caros.'], 
    'input_conclusion_pt' : 'dólar não subiu.',
    'input_assumptions_en': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'Os produtos não ficaram mais caros.'], 
    'input_conclusion_en' : 'O dólar não subiu.',
    'result_value': True
    }

EXAMPLES['q2'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
      'Os produtos ficaram mais caros.'], 
    'input_conclusion_pt' : 'O dólar não subiu.',
    'result_value': False
    }

EXAMPLES['q3'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
      'Os produtos ficaram mais caros.'], 
    'input_conclusion_pt' : 'O dólar subiu.',
    'result_value': False
    }

EXAMPLES['q4'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'O dólar não subiu.'], 
    'input_conclusion_pt' : 'Os produtos não ficaram mais caros.',
    'result_value': False
    }

EXAMPLES['q5'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'O dólar não subiu.'], 
    'input_conclusion_pt' : 'Os produtos ficaram mais caros.',
    'result_value': False
    }

EXAMPLES['q6'] = {  
    'input_assumptions_pt': ['O dólar sobe ou o petróleo sobe.', 'O dólar não subiu.'], 
    'input_conclusion_pt' : 'O petróleo subiu.',
    'result_value': True
    }

EXAMPLES['q7'] = {  
    'input_assumptions_pt': ['O dólar sobe ou o petróleo sobe.',
                                'Se o dólar sobe, então aumenta a inflação.','Se o petróleo sobe, então aumenta a inflação.'], 
    'input_conclusion_pt' : 'Aumentou a inflação.',
    'result_value': True
    }

EXAMPLES['q8'] = {  
    'input_assumptions_pt': ['Se o dólar sobe ou o petróleo sobe, então aumenta a inflação.',
                                'O dólar não subiu.','O petróleo não subiu.'], 
    'input_conclusion_pt' : 'Aumentou a inflação.',
    'result_value': False
    }

EXAMPLES['q9'] = {  
    'input_assumptions_pt': ['Se o dólar sobe ou o petróleo sobe, então aumenta a inflação.',
                                'O dólar não subiu.','O petróleo não subiu.'], 
    'input_conclusion_pt' : 'Não aumentou a inflação.',
    'result_value': False
    }

EXAMPLES['q10'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'Se o dólar não sobe, então compro mais comida.','Os produtos não ficaram mais caro.'], 
    'input_conclusion_pt' : 'Comprei mais comida.',
    'result_value': True
    }

EXAMPLES['q11'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'Se o dólar não sobe, então compro mais comida.','Os produtos ficaram mais caro.'], 
    'input_conclusion_pt' : 'Comprei mais comida.',
    'result_value': False
    }

EXAMPLES['q12'] = {  
    'input_assumptions_pt': ['Se o dólar sobe, então os produtos ficam mais caros.',
                                'Se o dólar não sobe, então compro mais comida.','Os produtos ficaram mais caro.'], 
    'input_conclusion_pt' : 'Não comprei mais comida.',
    'result_value': False
    }

EXAMPLES['q1_fo_ex'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente gosta de esporte radical.','Maria gosta de voo de parapente.'], 
    'input_conclusion_pt' : 'Maria gosta de esporte radical.',
    'result_value': True
    }

EXAMPLES['q2_fo_ex'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente gosta de esporte radical.','Maria não gosta de esporte radical.'], 
    'input_conclusion_pt' : 'Maria gosta de voo de parapente.',
    'result_value': False
    }

EXAMPLES['q3_fo_ex'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente não gosta de chuva.','João gosta chuva.'], 
    'input_conclusion_pt' : 'João não gosta de voo de parapente.',
    'result_value': True
    }

EXAMPLES['q4_fo_ex'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente não gosta de chuva.','João não gosta chuva.'], 
    'input_conclusion_pt' : 'João gosta de voo de parapente.',
    'result_value': False
    }

EXAMPLES['q5_fo_ex'] = {  
    'input_assumptions_pt': ['Todo mundo que é amado por alguém é feliz.',
                                'Existe alguém que não é feliz.'], 
    'input_conclusion_pt' : 'Existe alguém que não é amado por ninguém.',
    'result_value': True
    }

EXAMPLES['q1_fo'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente gosta de esporte radical.','Maria gosta de voo de parapente.'], 
    'input_conclusion_pt' : 'Maria não gosta de esporte radical.',
    'result_value': False
    }

EXAMPLES['q2_fo'] = {  
    'input_assumptions_pt': ['Quem não gosta de esporte radical não gosta de voo de parapente.','Maria gosta de voo de parapente.'], 
    'input_conclusion_pt' : 'Maria gosta de esporte radical.',
    'result_value': True
    }

EXAMPLES['q3_fo'] = {  
    'input_assumptions_pt': ['Quem não gosta de esporte radical não gosta de voo de parapente.','Maria não gosta de voo de parapente.'], 
    'input_conclusion_pt' : 'Maria gosta de esporte radical.',
    'result_value': False
    }

EXAMPLES['q4_fo'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente gosta de esporte radical.','Alguém gosta de voo de parapente.'], 
    'input_conclusion_pt' : 'Alguém gosta de esporte radical.',
    'result_value': True
    }

EXAMPLES['q5_fo'] = {  
    'input_assumptions_pt': ['Quem gosta de voo de parapente gosta de esporte radical.', 'Alguém gosta de esporte radical.'] , 
    'input_conclusion_pt' : 'Alguém gosta de voo de parapente.',
    'result_value': False
    }

EXAMPLES['q6_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Todos frequentam as aulas.', 'Todos fazem os exercícios'], 
    'input_conclusion_pt' : 'Todos são aprovados.',
    'result_value': True
    }

EXAMPLES['q7_fo'] = {  
    'input_assumptions_pt':['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém frequenta as aulas e faz os exercícios.']  , 
    'input_conclusion_pt' : 'Alguém é aprovado.',
    'result_value': True
    }

EXAMPLES['q8_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém frequenta as aulas.', 'Alguém faz os exercícios'], 
    'input_conclusion_pt' : 'Alguém é aprovado.',
    'result_value': False
    }

EXAMPLES['q9_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém foi aprovado.'], 
    'input_conclusion_pt' : 'Existe alguém que frequenta as aulas e fez os exercícios.',
    'result_value': False
    }

EXAMPLES['q10_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'] , 
    'input_conclusion_pt' : 'Existe alguém que não frequenta as aulas ou não faz os exercícios.',
    'result_value': True
    }

EXAMPLES['q11_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'], 
    'input_conclusion_pt' : 'Existe alguém que não frequenta as aulas.',
    'result_value': False
    }

EXAMPLES['q12_fo'] = {  
    'input_assumptions_pt': ['Todos que frequentam as aulas e fazem os exercícios são aprovados.', 'Alguém não é aprovado.'] , 
    'input_conclusion_pt' : 'Existe alguém que não frequenta as aulas e não faz os exercícios.',
    'result_value': False
    }


def to_str(input_assumptions, input_conclusion, result_value=False, language_pt=True):
    result = 'Considere as seguintes afirmações:' if language_pt else 'Consider the following statements:'
    i = 1
    for s in input_assumptions:
        result+=f'\n{i}. '+s
        i+=1
    result+= f'\nPodemos concluir que a afirmação abaixo segue logicamente das afirmações acima?' if language_pt else 'Can we conclude that the statement below follows logically from the statements above?'
    result+=f'\n{i}.'+input_conclusion
    result+="\nA) Sim" if language_pt else "\nA) Yes"
    result+="\nB) Não" if language_pt else "\nB) No"
    return result

def to_aiken(input_assumptions, input_conclusion, result_value=False, language_pt=True):
    result = 'Considere as seguintes afirmações:' if language_pt else 'Consider the following statements:'
    i = 1
    for s in input_assumptions:
        result+=f' {i}. '+s
        i+=1
    result+= f' Podemos concluir que a afirmação a seguir segue logicamente das afirmações anteriores?' if language_pt else ' Can we conclude that the following statement follows logically from the previous statements?'
    result+=f' {i}.'+input_conclusion
    result+="\nA) Sim" if language_pt else "\nA) Yes"
    result+="\nB) Não" if language_pt else "\nB) No"
    result+="\nANSWER: "+ ("A" if result_value else "B")
    return fr'{result}'

