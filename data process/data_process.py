import numpy as np
import pandas as pd
from tqdm import tqdm
#%% Read Data
path1 = '中医名家医案数据(20180610).xlsx'
path2 = '中医字典.xlsx'

data = pd.read_excel(path2,sheet_name='症状同义词')

#%% Get the Array
values = data.get_values()

#%% Get rid of the redundancy
numbers = len(values)
s_values =[]
mess_symptoms=[]
index = 0
for i in range(numbers):
    if values[i,1] not in mess_symptoms:
        mess_symptoms.append(values[i,1])
        s_values.append(values[i])

s_values = np.array(s_values)

#%% Find main symptoms from s_values
main_symptoms=[]
s_numbers = len(s_values)
index =[]
for i in range(s_numbers):
    if s_values[i,0] in main_symptoms:
        index.append(main_symptoms.index(s_values[i,0]))
    else:
        main_symptoms.append(s_values[i,0])
        index.append(len(main_symptoms)-1)

for i in range(s_numbers):
    if s_values[i,0] not in mess_symptoms:
        mess_symptoms.append(s_values[i,0])
        index.append(main_symptoms.index(s_values[i,0]))

main_symptoms.append('others')
num = len(main_symptoms)-1
#%% Def sym2index, sym2main, index2main

def sym2index(symptom):
    global index
    global num
    if symptom not in mess_symptoms:
        return num
    else:
        return index[mess_symptoms.index(symptom)]

def sym2main(symptom):
    global main_symptoms
    return main_symptoms[sym2index(symptom)]

#%% Test for s_values
for i in range(s_numbers):
    if s_values[i,0]!= sym2main(s_values[i,1]):
        print(i)
        print(s_values[i])
        print(sym2main(s_values[i,1]))



#%% Now Transform 中国名家医案数据
new_data = pd.read_excel('中医名家医案数据(20180610).xlsx')
t_values = new_data.get_values()
t_values = t_values[:,8:12]
t_number = np.size(t_values,0)
num_sym = len(main_symptoms)
mat=[]

for i in tqdm(range(t_number)):
    patient = []
    t_value = t_values[i]
    mat.append([])
    for j in range(4):

        if pd.isna(t_value[j]):
            t_value[j]=''
        char = ''
        for k in range(len(t_value[j])):
             if u'\u4e00' <= t_value[j][k] <= u'\u9fff':
                 char += t_value[j][k]
             else:
                 patient.append(char)
                 char = ''
        if char!='':
            patient.append(char)
    for symptom in patient:
        main_symptom = sym2index(symptom)
        if main_symptom not in mat[i]:
            mat[i].append(main_symptom)


#%% Export the data
f = open('out.csv','w')
t=1
for patient in mat:
    patient.sort()
    f.write(str(t))
    t+=1
    f.write(' ')
    for index in patient:
        f.write(str(index))
        f.write(' ')
    f.write('\n')
f.close()

#%% Export index2main
f = open('dic.txt','w')
t=1
for symptom in main_symptoms:
    f.write(str(t))
    t+=1
    f.write(' ')
    f.write(symptom)
    f.write('\n')
f.close()