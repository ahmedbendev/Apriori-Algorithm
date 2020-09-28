from collections import defaultdict
import operator
THRESHOLD = 100

item_counts = defaultdict(int)
pair_counts = defaultdict(int)
triple_counts = defaultdict(int)

with open('browsing-data.txt') as f:
    lines = f.readlines()
f.close()

def normalize_group(*args):
    return str(sorted(args))

def generate_pairs(*args):
    pairs=[]
    for idx_1 in range(len(args)-1):
        for idx_2 in range(idx_1 + 1,len(args)):
            pairs.append(normalize_group(args[idx_1],args[idx_2]))
    return pairs

# first pass

for line in lines:
    for item in line.split():
        item_counts[item] +=1


frequent_items = set()
for key in item_counts:
    if item_counts[key] > THRESHOLD:
        frequent_items.add(key) 


#secend pass

for line in lines:
    items = line.split()
    for idx_1 in range(len(items)-1):
        if items[idx_1] not in frequent_items:
            continue
        for idx_2 in range(idx_1 + 1, len(items)):
            if items[idx_2] not in frequent_items:
                continue
            pair = normalize_group(items[idx_1],items[idx_2])
            pair_counts[pair] += 1        

frequent_pairs = set()
for key in pair_counts:
    if pair_counts[key] > THRESHOLD:
        frequent_pairs.add(key)


# third pass

for line in lines:
    items = line.split()
    for idx_1 in range(len(items) - 2):
        if items[idx_1] not in frequent_items:
            continue
        for idx_2 in range(idx_1 + 1, len(items) - 1):
            if items[idx_2] not in frequent_items:
                continue
            first_pair = normalize_group(items[idx_1],items[idx_2])
            if first_pair not in frequent_pairs:
                continue
            for idx_3 in range(idx_2 + 1, len(items)):
                if items[idx_3] not in frequent_items:
                    continue
                pairs= generate_pairs(items[idx_1],items[idx_2],items[idx_3])
                if any(pair not in frequent_pairs for pair in pairs):
                    continue
                triple = normalize_group(items[idx_1],items[idx_2],items[idx_3])
                triple_counts[triple] +=1

frequent_triples= set()
for key in triple_counts:
    if triple_counts[key] > THRESHOLD:
        frequent_triples.add(key)  


#the results



triple_counts = {k: v for k, v in triple_counts.items() if v > THRESHOLD}
sorted_tripels = sorted(triple_counts.items(),key=operator.itemgetter(1))

for entry in sorted_tripels:
    print('{0}: {1}'.format(entry[0], entry[1]))


# print('sorted_tripels',sorted_tripels)



pair_counts = {k: v for k, v in pair_counts.items() if v > THRESHOLD}
sorted_pairs = sorted(pair_counts.items(),key=operator.itemgetter(1))

# print('frequent_pairs',frequent_pairs)
# print('sorted_pairs',sorted_pairs)



item_counts = {k: v for k, v in item_counts.items() if v > THRESHOLD}
sorted_items = sorted(item_counts.items(),key=operator.itemgetter(1))

# print('frequent_items',frequent_items)
# print('sorted_items',sorted_items)



# //calculate confident in pair
list_pair_with_conf=[]
# create new list of xy with confidence and order them
for pair in sorted_pairs:
    xy=pair[0]
    x=xy[2:10]
    y=xy[14:22]
    x_accurence=0
    y_accurence=0
    xy_accurence = pair[1]
    for item in sorted_items:
        if x == item[0]:
            x_accurence=item[1]
        if y == item[0]:
            y_accurence=item[1]
    
    # x =>y
    xy_confidence =  xy_accurence/x_accurence
    pair_with_conf=(x,y,xy_confidence)
    list_pair_with_conf.append(pair_with_conf)

    # y =>x
    yx_confidence=  xy_accurence/y_accurence
    pair_with_conf=(y,x,yx_confidence)
    list_pair_with_conf.append(pair_with_conf)


def Sort_Tuple(tup):  
    tup.sort(key = lambda x: x[2])  
    return tup 

the_final_list_revers=Sort_Tuple(list_pair_with_conf)
the_final_list= the_final_list_revers[::-1]

print('the_final_list:',the_final_list)



text="OUTPUT A \n"
# get only the five first XYZ item
n=0
while n < 5:
    print(the_final_list[n])
    n=n+1
    itm=the_final_list[n]
    textline=str(itm[0])+' '+str(itm[1])+' '+str(itm[2])+'\n'
    text=text+textline

print(text)








# //calculate confident in tupels
list_tuple_with_conf=[]
# create new list of xy with confidence and order them
for triple in sorted_tripels:
    # print('triple',triple)
    xyz=triple[0]
    x=xyz[2:10]
    y=xyz[14:22]
    z=xyz[26:34]
    xy_accurence=0
    xz_accurence=0
    yz_accurence=0
    xyz_accurence = triple[1]
    for pair in sorted_pairs:
        xy_pair=pair[0]
        x_pair=xy_pair[2:10]
        y_pair=xy_pair[14:22]
        xy_pair_accurence = pair[1]
        if (x_pair==x and y_pair==y) or (x_pair==y and y_pair==x):
            xy_accurence = xy_pair_accurence
        if (x_pair==x and y_pair==z) or (x_pair==z and y_pair==x):
            xz_accurence = xy_pair_accurence
        if (x_pair==y and y_pair==z) or (x_pair==z and y_pair==y):
            yz_accurence = xy_pair_accurence
    
    # print('xyz_accurence',xyz_accurence)
    # print(xy_accurence,xz_accurence,yz_accurence)
    # (x,y) =>z
    xyz_confidence=  xyz_accurence/xy_accurence
    tuple_with_conf=(x,y,z,xyz_confidence)
    list_tuple_with_conf.append(tuple_with_conf)

    # (x,z) =>y
    xzy_confidence=  xyz_accurence/xz_accurence
    tuple_with_conf=(x,z,y,xzy_confidence)
    list_tuple_with_conf.append(tuple_with_conf)

    # (y,z) =>x
    yzx_confidence=  xyz_accurence/yz_accurence
    tuple_with_conf=(y,z,x,yzx_confidence)
    list_tuple_with_conf.append(tuple_with_conf)

print('list_tuple_with_conf',list_tuple_with_conf)
        


def Sort_Tuple_Three(tup):  
    tup.sort(key = lambda x: x[3])  
    return tup 

the_final_xyz_list_revers=Sort_Tuple_Three(list_tuple_with_conf)
the_final_xyz_list= the_final_xyz_list_revers[::-1]

print('the_final_xyz_list:',the_final_xyz_list)

text=text+"OUTPUT B \n"
# get only the five first XYZ item
n=0
while n < 5:
    print(the_final_xyz_list[n])
    n=n+1
    itm=the_final_xyz_list[n]
    textline=str(itm[0])+' '+str(itm[1])+' '+str(itm[2])+' '+str(itm[3])+'\n'
    text=text+textline

print('text',text)

# creating the file
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'output.txt')
file = open("output.txt", "w") 
file.write(text) 
file.close()








