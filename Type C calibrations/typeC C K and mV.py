from thermocouples_reference import thermocouples
import numpy as np
import pandas as pd

typeC=thermocouples['C']
test=np.arange(0,2315,0.02)
out = typeC.emf_mVC(test)
typeC_df = pd.DataFrame(data=out, index=test,dtype='float32',columns=['mV'])

typeC_df.index.name = 'C'

K = typeC_df.index+273.15
typeC_df.insert(loc=0, column='K', value=K)

# write to excel
xlwrite = pd.ExcelWriter('typeC degC and K to mV.xlsx')
typeC_df.to_excel(xlwrite)
xlwrite.save()


def find_Tref(mV, T):
    x = np.arange(290, 301, 0.01)
    x = x[::-1]
    i = 1
    while typeC.inverse_KmV(mV, Tref=x[i]) - T >= 0:
        i += 1
    print(x[i])
    return x[i]

#
# df is the imported df
# tempdf = df.query('T>273.15')
Treflist=[]

# for idx in tempdf.index:
#     print(idx)
#     Treflist.append(find_Tref(mV=tempdf['TypeCmV'][idx], T=tempdf['T'][idx]))
# print(Treflist)