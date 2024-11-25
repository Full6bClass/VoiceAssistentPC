x = ['звук', 'убавить,', 'стоп']
y = ['убавить,', 'стоп']



tokens = [i for i in x if i not in y]
print(tokens)