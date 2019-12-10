#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: PLEASE PUT YOUR NAMES AND USERIDS HERE
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#  A more sophisticated genetic algorimn is used to break the code. Currently it runs correctly but is not efficient enough to solve in ten minutes.
#  Even if I improving run time I'm not sure if it'll be able to solve it in ten minutes, so this implementation is on hold while I attempt other things
#


import random
import math
import copy 
import sys
import encode
import string


def get_cypher_list():
    letters = string.ascii_lowercase
    return [list(''.join(random.sample(letters, len(letters)))) for i in range(0, 30)]


#Select random parents in cypher
def weighted_random_choice(corpus_dict, text, cypher_list):
    max_fit = total_fitness(corpus_dict, text, cypher_list)
    pick = random.uniform(0, max_fit)
    current = 0
    for cypher in cypher_list:
        current += fitness(corpus_dict, text, cypher)
        if current > pick:
            return cypher


def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1)-1)
    child1 = parent1[:crossover_point]+parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def encode_text(text, cypher):
    final_string = ""
    for i in text:
        if i is " ":
            final_string = final_string + " "
        else:
            pos = string.ascii_lowercase.index(i)
            final_string = final_string + cypher[pos]
    return final_string


#Fitness of an entire population
def total_fitness(corpus_dict, text, population):
    total = 0
    for chromosome in population:
        total += fitness(corpus_dict, text, chromosome)
    return total


def fitness(corpus_dict, text, cypher):
    final_score = 0
    encoded_dict = get_prob_scores(encode_text(text, cypher))
    for p in encoded_dict:
        if p in corpus_dict:
            final_score = final_score + corpus_dict.get(p)
    return final_score


#Find best suited parents
def top_population(cypher_list, corpus_dict, text):
    population = sorted(cypher_list, key = lambda x: fitness(corpus_dict, text, x), reverse = True)
    parent_length = int(0.1 * len(population))
    parents = population[:parent_length]
    return parents


# put your code here!
def break_code(encoded, corpus):
    corpus_dict = get_prob_scores(corpus)
    cypher_list = get_cypher_list()
    generation = 0
    while(generation < 200):
        new_cypher_generation = top_population(cypher_list, corpus_dict, encoded)
        while(len(new_cypher_generation) < len(cypher_list)):
                parent1 = weighted_random_choice(corpus_dict, encoded, cypher_list)
                parent2 = weighted_random_choice(corpus_dict, encoded, cypher_list)
                child1, child2 = one_point_crossover(parent1, parent2)
                new_cypher_generation += [mutate(child1)]
                new_cypher_generation += [mutate(child2)]

        cypher_list = new_cypher_generation
        generation += 1

    print(fitness(corpus_dict, encoded, cypher_list[0]))
    print(fitness(corpus_dict, corpus, (string.ascii_lowercase)))
    return encode_text(encoded, cypher_list[0])


def mutate(child):
    mutation_rate = 0.05
    for gene in range(1, len(child)):
        pick = random.uniform(0, 1)
        if pick <= mutation_rate:
            temp = child[gene - 1]
            child[gene - 1] = child[gene]
            child[gene] = temp
    return child


#Find probs for any encoded text
def get_prob_scores(corpus):
    prob_dict = {}
    for i in range(len(corpus) - 1):
        char1 = corpus[i]
        char2 = corpus[i + 1]
        key = char1+char2
        if key in prob_dict:
             prob_dict[key]+=1
        else:
            prob_dict[key]=1
    return prob_dict


if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")
    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded, corpus)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)

