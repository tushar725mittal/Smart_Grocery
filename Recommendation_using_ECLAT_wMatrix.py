"""
eclat implementation 
"""
import csv
# import matplotlib.pyplot as plt
# #filling the dict with item->purchase no.
# def itemdict_initialize(item_dict,datacsv,item_list):
#     with open(datacsv,mode="r",encoding='utf-8-sig') as file:
#         csvfile=csv.reader(file)
#         for i,lines in enumerate(csvfile):
#             for item in lines:
#                 if item=='':
#                     continue
#                 if item not in item_dict:
#                     item_dict[item]=set()
#                     item_dict[item].add(i)
#                 else:
#                     item_dict[item].add(i)
#                 if item not in item_l:
#                     item_list.append(item)
#     return item_dict,item_list

# #making item sets by finding intersections of common transaction ids
# def pairmaker(pairlist,support,item_dict):
#     newpair_l=[]
#     for i in range(0,len(pairlist)-1):
#         for j in range(i+1,len(pairlist)):
#             int_set=item_dict[pairlist[i]].intersection(item_dict[pairlist[j]])
#             if len(int_set)>=support:
#                 set_i,set_j=set(pairlist[i].split(",")),set(pairlist[j].split(","))
#                 str=",".join(list(set_i.union(set_j)))
#                 if str in item_dict:
#                     continue
#                 item_dict[str]=int_set
#                 newpair_l.append(str)
#     return newpair_l

# if __name__=="__main__":
#     #loading arrays for plotting
#     x1=[]
#     y1=[]
#     y2=[]

#     ##lOADING TEST CASES
#     test=[]
#     with open("Grocery_Test.csv",mode="r",encoding='utf-8-sig') as file:
#         csvfile=csv.reader(file)
#         for line in csvfile:
#             lst=[]
#             for item in line:
#                 if item=='':
#                     break
#                 else:
#                     lst.append(item)
#             test.append(lst)
#     #MAKING THE DICT FOR ECLAT
#     for i in range(1,16):
#         s_value=i*10
#         x1.append(i)
#         y1.append(s_value/169)
#         #item parining wuth order no. dict
#         item_order={}
#         #list for maintaining the item pairings
#         item_l=[]
#         #initializing the item dict
#         item_order,item_l=itemdict_initialize(item_order,"Grocery_Products_Purchase.csv",item_l)
#         with open("Grocery_Result_ECLAT.csv",mode="w") as csvfile:
#             csvwriter=csv.writer(csvfile)
#             while(len(item_l)>1):
#                 item_l=pairmaker(item_l,s_value,item_order)
#                 for x in item_l:
#                     csvwriter.writerow(x.split(","))
#         item_matrix_7={}
#         with open("Grocery_Result_ECLAT.csv",mode="r",encoding='utf-8-sig') as file:
#             csvfile=csv.reader(file)
#             for lines in csvfile:
#                 if len(lines)==0:
#                     continue
#                 for i in lines:
#                     main_item=i
#                     for j in lines:
#                         if i==j:
#                             continue
#                         if i in item_matrix_7:
#                             item_matrix_7[i].add(j)
#                         else:
#                             item_matrix_7[i]={j}
#         ##TESTING ACCURACY
#         valid_cases=0
#         score=[]
#         for i in test:
#             if len(i)<=1:
#                 continue
#             valid_cases+=1
#             main_item=i[0]
#             actual_item=i[1:]
#             len_a=len(actual_item)
#             set_a=set(actual_item)
#             if main_item in item_matrix_7:
#                 score.append(len(set_a.intersection(item_matrix_7[main_item]))/len_a)
#         score=sum(score)/valid_cases
#         y2.append(score)

#     default_x_ticks = range(len(x1))
#     plt.plot(default_x_ticks, y1,'r-',label='Support')
#     plt.plot(default_x_ticks, y2,'b-',label='Accuracy')
#     plt.xticks(default_x_ticks, x1)
#     plt.grid()
#     plt.legend(loc='best')
#     plt.savefig('testplot_woMatrix.png')

user_brand={}
with open("Grocery_Brands_Purchase.csv",mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for lines in csvfile:
            user=lines[0]
            if user not in user_brand:
                user_brand[user]={}
            for item in lines[1:]:
                if item=='':
                    break
                if item in user_brand[user]:
                    user_brand[user][item]+=1
                else:
                    user_brand[user][item]=0
for user in user_brand:
    user_brand[user]=sorted(user_brand[user],reverse=True,key=lambda x:user_brand[user][x])
    print(user,user_brand[user][0:6])