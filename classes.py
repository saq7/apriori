
from apriori import * #vertical_dataform, subset, count_itemsets, gen_candidates, prune_infreq_itemsets
class itemsets:
    
    def __init__(self):
        self.data = {}
        self.transaction_db = {}
        self.last_itemsets = 0
    
    def create_tdb_from_csv(self,csv_file):
        '''create transaction database from csv
        consumes a csv file which has the form - user,item,count
        user = <any>, item = <any - has to support comparisions>, count = <int,float>'''
        N = sum(1 for line in open(csv_file))
        infile = open(csv_file, "r")
        #self.data['transaction_db'] = {}
        for line in infile:
            line = line.rstrip()
            l = line.split(',')
            user = l[0]
            key = l[1]
            counts = l[2]
            try:
                self.transaction_db[user]
            except: 
                self.transaction_db[user] = {}
            self.transaction_db[user][key] = counts

    def apriori(self, n, min_sup):
        '''Consumes a transaction database and a positive integer representing the 
        size of the itemsets to be generated, and a minimum support.
        Produces n-itemsets that meet minsup.'''
        
        if n<=0 or type(n) != int or min_sup<0 or type(min_sup) != int:
            raise ValueError('n must be an greater than 0; min_sup n must be an greater or equal to 0')
        
        transaction_db = self.transaction_db
        
        for i in range(self.last_itemsets,n):
            prev_itemsets = 'itemsets'+str(i) 
            new_itemsets = 'itemsets'+str(i+1)
            if i == 0:
                itemsets = vertical_dataform(transaction_db)
            else:
                itemsets = gen_candidates(self.data[prev_itemsets], self.last_itemsets)
            itemsets = count_itemsets(itemsets, transaction_db)
            itemsets = prune_infreq_itemsets(itemsets, min_sup)
            self.data[new_itemsets]=itemsets
            self.last_itemsets = i + 1
        #return itemsets

    def get_itemset(self,n):
        '''returns n-itemset if it has been computed, otherwise raises key exception'''
        x = 'itemsets'+str(n)
        return self.data[x]
    
    def get_support (self,itemset):
        length = len(itemset)
        itemset_in_data = 'itemsets'+str(length)
        support = self.data[itemset_in_data][itemset]
        return support
    
    def mine_assoc_rules (self, min_conf):
        '''given an itemsets obj, mines all association rules that meet min_conf threshold'''
        largest_itemset = 'itemsets'+str(self.last_itemsets)
        largest_itemset = self.data[largest_itemset]
        output_set = set()
        for itemset in largest_itemset:
            rules = self.itemset_confidence(itemset)
            for rule in rules:
                if rule[-1] >= min_conf:
                    output_set.add(rule)
        return output_set
    
    
    def itemset_confidence (self,itemset):
        '''consumes an itemset, returns a set of tuples of the form (A, B, conf) ; P(B|A) = conf'''
        subsets = generate_subsets(itemset)
        support_itemset = self.get_support(itemset)            
        itemset = set(itemset)
        output = set()
        for subset in subsets:
            support_subset = self.get_support(subset)
            diffitems = tuple(itemset.difference(subset))
            output_tuple = (diffitems,subset,float(support_itemset)/support_subset)
            output.add(output_tuple)
        return output
