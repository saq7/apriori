from itertools import combinations
def apriori(transaction_db, n, min_sup):
    '''Consumes a transaction database and a 
    positive integer representing the 
    size of the itemsets to be generated, 
    and a minimum support.
    Produces n-itemsets that meet minsup.'''
    if n<=0 or type(n) != int:
        raise ValueError('n must greater than 0')
    for i in range(0,n):
        if i == 0:
            itemsets = vertical_dataform(transaction_db)
        else:
            itemsets = gen_candidates(itemsets)
        itemsets = count_itemsets(itemsets, transaction_db)
        itemsets = prune_infreq_itemsets(itemsets, min_sup)
    return itemsets
        

def vertical_dataform(data_dict):
    '''given a user-transaction dict of the form 
    {'user_1': {'item_1':quantity,...,'item_n':quantity},
    ..., 
    'user_m':{'item_1':quantity,...,'item_n':quantity}}
    produces a dict, with all values initialized to zero, 
    of items 1 through n as keys'''
    vert_dict = {}
    for user in data_dict:
        for key in data_dict[user]:
            vert_dict[(key,)] = 0
    return vert_dict


def count_itemsets(itemsets_dict,transactions_dict):
    '''given a dict of itemsets (initialized to zero) 
    and a transaction database, 
    returns counts of itemsets in the TDB'''
    itemsets_dict2 = itemsets_dict
    for user in transactions_dict:
        user_items = transactions_dict[user].keys()
        user_items.sort()
        for itemset in itemsets_dict2:
            if subset(itemset,user_items):
                itemsets_dict2[itemset] +=1
    return itemsets_dict2

def prune_infreq_itemsets(itemsets_dict, min_sup):
    '''prune itemsets whose support is less than min_sup''' 
    itemsets_dict2 = itemsets_dict
    small_subs = []
    for key in itemsets_dict2:
        if itemsets_dict2[key] < min_sup:
            small_subs.append(key)
    for i in small_subs:
        itemsets_dict2.pop(i,None)     
    return itemsets_dict2

        
def gen_candidates(itemsets, n):
    '''given an n-itemset, generates a 
    (n+1)-itemset also requires value of n 
    i.e. the size of the itemset in the itemsets given'''
    itemsets2 = {}
    first_iter = True
    str_bit = 0
    
    for key1 in itemsets:
        for key2 in itemsets:
            if key1[:-1]==key2[:-1]:
                key1_last = key1[-1]
                key2_last = key2[-1]
                if key1_last != key2_last:
                    if key1_last < key2_last:
                        # create a key with both the 
                        # last elements from key1 and key2
                        # keep sorted
                        key = list(key1)
                        key.append(key2_last)
                    else:
                        key = list(key2)
                        key.append(key1_last)
                    itemsets2[tuple(key)] = 0
    return itemsets2
    

# check whether smallset is a subset of bigset
def subset(smallset, bigset):
    '''expects bigset to be sorted in ascending order'''
    for i in smallset: 
        if binary_search(bigset, i, 0, len(bigset)-1) == None:
            return False
        #print i
    return True

def binary_search(lst, x, imin, imax):
    ''' returns index if x is found, None otherwise'''
    while (imin<=imax):
        imid = (imin+imax)/2
        if lst[imid] == x:
            return imid
        elif lst[imid] < x:
            imin = imid + 1
        else:
            imax = imid - 1
    return None


def generate_subsets (itemset):
    ''' generates all non empty subsets of 
        itemset of size up to len(itemset)-1'''
    output = set()
    itemset = sorted(itemset)
    for i in range(1,len(itemset)):
        output = output.union(
            set(combinations(itemset, i)))
    return output
    
