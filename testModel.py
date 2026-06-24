from model.modello import Model

model = Model()

model.creaGrafo(2000, 'flash')

nodi, archi = model.getInfo()
print(f'Numero di vertici: {nodi}')
print(f'Numero di archi: {archi}')

bestArchi = model.getBestArchi()
print(f'I 5 archi di peso maggiore sono:')
for u, v, data in bestArchi:
    print(f'{u} -> {v} | weight = {data['weight']}')