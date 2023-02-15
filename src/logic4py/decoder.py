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
      preds[key] = set()
      for t in data[key]:
        if (type(t)!=list):
          preds[key].add(t)
        elif (type(t)==list and len(t)==1):
          preds[key].add(t[0])
        else:  
          preds[key].add(tuple([str(k) for k in t]))
    else:
      s[key] = data[key]
  return U, preds, s