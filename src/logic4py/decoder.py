import ruamel.yaml

import ruamel.yaml
def decode_fo_interpretation(input_fo_interpretatio, universe_key='U'):
  data_fo_interpretatio = input_fo_interpretatio.replace('=',':').replace('{','[').replace('}',']').replace('set()','[]').replace('(','[').replace(')',']')
  yaml = ruamel.yaml.YAML(typ='safe')
  data = yaml.load(data_fo_interpretatio)
  U = set([str(s) for s in data[universe_key]])
  preds = {}
  s = {}
  for key in data.keys():
    if key==universe_key:
      continue
    elif key[0].isupper():
      if '_' in key:
        s_key, s_arity = key.split('_')
        arity = int(s_arity)
      else:
        s_key = key
        if len(data[key])==0:
          arity = -1
        else:
          arity = len(data[key][0]) if list==type(data[key][0]) else 1
      if arity>1:
        for t in data[key]:
          if type(t)!=list:
            raise ValueError(f'No predicado {key}, {t} deveria ser uma tupla de tamanho {arity}')
          elif len(t)!=arity:
            raise ValueError(f'No predicado {key}, a tupla {tuple(t)} deve ter tamanho {arity}')
          for k in t:
            if not k in U:
              raise ValueError(f'No predicado {key}, o elemento {k} da tupla {tuple(t)} deveria fazer parte do conjunto universo')
      elif arity==1:
        for t in data[key]:
          if type(t)==list and len(t)!=arity:
            raise ValueError(f'No predicado {key}, {tuple(t)} deveria ser uma tupla de tamanho {arity}')
          elif type(t)!=list and not t in U:
            raise ValueError(f'No predicado {key}, {t} deveria fazer parte do conjunto universo')
          elif type(t)==list and not t[0] in U:
            raise ValueError(f'No predicado {key}, {t[0]} deveria fazer parte do conjunto universo')
      preds[s_key,arity] = set()
      for t in data[key]:
        if (type(t)!=list):
          preds[s_key,arity].add(t)
        elif (type(t)==list and len(t)==1):
          preds[s_key,arity].add(t[0])
        else:  
          preds[s_key,arity].add(tuple([str(k) for k in t]))
    else:
      if data[key] in U:
        s[key] = data[key]
      else:
        raise ValueError(f'O valor {data[key]} deveria fazer parte do conjunto universo')
  return U, preds, s
# import ruamel.yaml

# def decode_fo_interpretation(input_fo_interpretatio, universe_key='U'):
#   data_fo_interpretatio = input_fo_interpretatio.replace('=',':').replace('{','[').replace('}',']').replace('set()','[]').replace('(','[').replace(')',']')
#   yaml = ruamel.yaml.YAML(typ='safe')
#   data = yaml.load(data_fo_interpretatio)
#   U = set([str(s) for s in data[universe_key]])
#   preds = {}
#   s = {}
#   for key in data.keys():
#     if key==universe_key:
#       continue
#     elif key[0].isupper():
      
#       preds[key] = set()
#       for t in data[key]:
#         if (type(t)!=list):
#           preds[key].add(t)
#         elif (type(t)==list and len(t)==1):
#           preds[key].add(t[0])
#         else:  
#           preds[key].add(tuple([str(k) for k in t]))
#     else:
#       s[key] = data[key]
#   return U, preds, s