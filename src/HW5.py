# -*- coding: utf-8 -*-
"""
Created on Wen Apr 28 12:32:43 2021

@author: Nooreldean Koteb
"""
from collections import defaultdict
from math import log

class translate():
    def preprocess(self):
        with open('starwars/train.zh-en', encoding='utf-8') as f:    
            self.lines = []
            for line in f:
                line.replace('\n', '')
                spl = line.split('\t')
                self.lines.append((spl[0], 'NULL '+spl[1]))
        
        eng = []
        for line in self.lines:
            eng.append(line[1].split())
            
        self.eng_corp =  len(eng)
        
        self.words = defaultdict(dict)
        self.count = defaultdict(dict)
        for line in self.lines:
            for i in line[0].split():
                for j in line[1].split():
                    
                    try:
                        self.words[i][j] += 1/self.eng_corp
                    except:
                        self.words[i][j] = 1/self.eng_corp
                    
                    self.count[i][j] = 0
    
    
    def clear_count(self):
        for zh in self.count:
            for eng in self.count[zh]:
                self.count[zh][eng] = 0
                
    
    def e_step(self):
        for line in self.lines:
            for i in line[0].split():
                for j in line[1].split():
                    
                    sumation = 0
                    for k in line[1].split():
                        if j != k:
                            sumation += self.words[i][k]
                    
                    self.count[i][j] += self.words[i][j]/sumation
    
    
    
        
    def m_step(self):
        for zh in self.words:
            for eng in self.words[zh]:
                
                sumation = 0
                for k in self.count:
                    if k != zh:
                        try:
                            sumation += self.count[k][eng]
                        except:
                            pass
                    
                if sumation == 0:
                    sumation = 1
                    
                self.words[zh][eng] = self.count[zh][eng]/sumation
    
    
    def log_likelihood(self):
        sumation = 0
        for zh in self.words:
            for eng in self.words[zh]:
                sumation += self.words[zh][eng]
                
            sumation*= 1/self.eng_corp+1
            try:
                self.result+= sumation
            except:
                self.result = sumation
                
            sumation = 0
        self.result*= 1/100
        
        print(f"Pre-Log: {self.result}")
        return log(self.result)
        

epochs = 4
five_words = ['jedi', 'force', 'droid', 'sith', 'lightsabre']


trans = translate()
trans.preprocess()

log_like = 0
for i in range(epochs+1):
    print(f'Epoch - {i}/{epochs}')
    print('e-step')
    trans.e_step()
    print('m-step')
    trans.m_step()
    print('clearing count')
    trans.clear_count()
    print('calculating Log')
    log_like += trans.log_likelihood()
    print(f'Log-Likelihood: {log_like}')



words = trans.words
count = trans.count

five_words_zh = []
for i in five_words:
    largest = []
    for zh in words:
        for en in words[zh]:
            if en == i:
                if largest == []:
                    largest = [words[zh][en], zh]
                else:
                    if words[zh][en] > largest[0]:
                            largest = [words[zh][en], zh]
    five_words_zh.append(largest[1])

print('Five words english to chinese:')
for i in range(5):
    print(f'{five_words[i]} -> {five_words_zh[i]}')
    

eng_dic = defaultdict(dict)

for zh in words:
    for eng in words[zh]:
        eng_dic[eng][zh] = words[zh][eng]


with open("ttable.txt", "w", encoding='utf-8') as f:
    for eng in eng_dic:
        for zh in eng_dic[eng]:
            f.write(f'{eng} {zh} {eng_dic[eng][zh]}\n')
    
    
    
    




