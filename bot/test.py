from os import read
from utils import *

data = {'name': 'Daniele', 'surname': 'Pellegrini', 'Età': 23}
data2 = {'name': 'Daniele', 'surname': 'Pellegrini'}
data3 = {'name': 'Daniele', 'id': 382370960}

#save_user_data('prova', data)
save_user_data(382370960, data3)
# user = get_user('prova')
# print(user)