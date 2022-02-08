"""
eclat implementation with matrix for lower support items
"""
import csv
import matplotlib.pyplot as plt
import json 
import sys
import jsonpickle
#filling the dict with item->purchase no.
def itemdict_initialize(item_dict,datacsv,item_list):
    with open(datacsv,mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for i,lines in enumerate(csvfile):
            for item in lines:
                if item=='':
                    continue
                if item not in item_dict:
                    item_dict[item]=set()
                    item_dict[item].add(i)
                else:
                    item_dict[item].add(i)
                if item not in item_l:
                    item_list.append(item)
    return item_dict,item_list

#making item sets by finding intersections of common transaction ids
def pairmaker(pairlist,support,item_dict):
    newpair_l=[]
    for i in range(0,len(pairlist)-1):
        for j in range(i+1,len(pairlist)):
            int_set=item_dict[pairlist[i]].intersection(item_dict[pairlist[j]])
            if len(int_set)>=support:
                set_i,set_j=set(pairlist[i].split(",")),set(pairlist[j].split(","))
                str=",".join(list(set_i.union(set_j)))
                if str in item_dict:
                    continue
                item_dict[str]=int_set
                newpair_l.append(str)
    return newpair_l

if __name__=="__main__":
    #loading arrays for plotting
    x1=[]
    y1=[]
    y2=[]
    #master dict to map item_matrix with its most popular side purchases
    item_matrix={}

    item_count={}

    order_count=0
    #opening product purchases and adding freq of related item_matrix line by line
    with open("Grocery_Products_Purchase.csv",mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for lines in csvfile:
            order_count+=1
            for itemA in lines:
                if itemA=='':
                    break
                if itemA in item_count:
                    item_count[itemA]+=1
                if itemA not in item_count:
                    item_count[itemA]=1
                for itemB in lines:
                    if itemA==itemB or itemB=='':
                        continue
                    else:
                        if itemA not in item_matrix:
                            item_matrix[itemA]={}
                        if itemB in item_matrix[itemA]:
                            item_matrix[itemA][itemB]+=1
                        if itemB not in item_matrix[itemA]:
                            item_matrix[itemA][itemB]=1
                        if itemB in item_count:
                            item_count[itemB]+=1
                        if itemB not in item_count:
                            item_count[itemB]=1
    ##for a pairing i->j
    #results when sorting by confidence support i->j
    with open("Grocey_Result_Confidence_1.csv",mode="w") as csvfile1:
        csvwriter1=csv.writer(csvfile1)
        for i in item_matrix:
            list1=[]
            for t in item_matrix[i]:
                confidence_t_i=item_matrix[i][t]/item_count[t]
                confidence_i_t=item_matrix[i][t]/item_count[i]
                list1.append((t,confidence_i_t))
            list1=sorted(list1,reverse=True,key=lambda x:x[1])
            list1=[x[0] for x in list1]
            csvwriter1.writerow([i]+list1)

    #MAKING THE DICT FOR ECLAT
    # for i in range(1,16):
    s_value=70
    x1.append(i)
    y1.append(s_value/169)
    #item parining wuth order no. dict
    item_order={}
    #list for maintaining the item pairings
    item_l=[]
    #initializing the item dict
    item_order,item_l=itemdict_initialize(item_order,"Grocery_Products_Purchase.csv",item_l)
    with open("Grocery_Result_ECLAT.csv",mode="w") as csvfile:
        csvwriter=csv.writer(csvfile)
        while(len(item_l)>1):
            item_l=pairmaker(item_l,s_value,item_order)
            for x in item_l:
                csvwriter.writerow(x.split(","))

    ### for test###
    item_matrix_eclat={}
    with open("Grocery_Result_ECLAT.csv",mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for lines in csvfile:
            if len(lines)==0:
                continue
            for i in lines:
                main_item=i
                for j in lines:
                    if i==j:
                        continue
                    if i in item_matrix_eclat:
                        item_matrix_eclat[i].add(j)
                    else:
                        item_matrix_eclat[i]={j}
    
    #importing reusltant pairing matrices from their respectives csv
    item_matrix_matrix={}
    with open("Grocey_Result_Confidence_1.csv",mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for lines in csvfile:
            if len(lines)==0:
                continue
            main_item=lines[0]
            if main_item in item_matrix_eclat:
                if len(item_matrix_eclat[main_item])>4:
                    continue
            if len(lines)>1:
                item_matrix_matrix[main_item]=set([x for x in lines[1:10]])
            else:
                item_matrix_matrix[main_item]=set()

    #importing subcategories of the items
    item_catg={}
    with open("Grocery_Categories.csv",mode="r",encoding='utf-8-sig') as file:
        csvfile=csv.reader(file)
        for lines in csvfile:
            for i,x in enumerate(lines):
                if x=='':
                    break
                if i==0:
                    item_main=x
                    item_catg[x]=[]
                else:
                    item_catg[item_main].append(x)

        
    
user_items=int(input("Number of items you want initially:"))
if user_items==0:
    print("Number should be more than one!")
res_user=set()
for t in range(user_items):
    print("---")
    print("Item number:",t+1)
    print()
    print("Item Categories:")
    for i in item_catg:
        print(i)
    print()
    catg=str(input("Your Choice:"))
    print()
    print("Items in the Category:")
    for i in item_catg[catg]:
        print(i)
    print()
    strng=str(input("Your Choice:"))
    print()
    if strng in item_matrix_eclat:
        if len(res_user)==0:
            res_user=res_user.union(item_matrix_eclat[strng])
        else:
            res_user=res_user.intersection(item_matrix_eclat[strng])
    else:
        if len(res_user)==0:
            res_user=res_user.union(item_matrix_matrix[strng])
        else:
            res_user=res_user.intersection(item_matrix_matrix[strng])
print("Your recommended Items:")
print(res_user)
