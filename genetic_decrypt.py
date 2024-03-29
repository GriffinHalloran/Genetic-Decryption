
import random
import math
import copy 
import sys
import encode
import string


def get_cipher_list():
    letters = string.ascii_lowercase
    return [list(''.join(random.sample(letters, len(letters)))) for i in range(0, 30)]


#Select random parents in cypher
def weighted_random_choice(corpus_dict, text, cipher_list):
    max_fit = total_fitness(corpus_dict, text, cipher_list)
    pick = random.uniform(0, max_fit)
    current = 0
    for cipher in cipher_list:
        current += fitness(corpus_dict, text, cypher)
        if current > pick:
            return cipher


def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1)-1)
    child1 = parent1[:crossover_point]+parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def encode_text(text, cipher):
    final_string = ""
    for i in text:
        if i is " ":
            final_string = final_string + " "
        else:
            pos = string.ascii_lowercase.index(i)
            final_string = final_string + cipher[pos]
    return final_string


#Fitness of an entire population
def total_fitness(corpus_dict, text, population):
    total = 0
    for chromosome in population:
        total += fitness(corpus_dict, text, chromosome)
    return total


def fitness(corpus_dict, text, cipher):
    final_score = 0
    encoded_dict = get_prob_scores(encode_text(text, cipher))
    for p in encoded_dict:
        if p in corpus_dict:
            final_score = final_score + corpus_dict.get(p)
    return final_score


#Find best suited parents
def top_population(cipher_list, corpus_dict, text):
    population = sorted(cipher_list, key = lambda x: fitness(corpus_dict, text, x), reverse = True)
    parent_length = int(0.1 * len(population))
    parents = population[:parent_length]
    return parents


# put your code here!
def break_code(encoded, corpus):
    corpus_dict = get_prob_scores(corpus)
    cipher_list = get_cipher_list()
    generation = 0
    while(generation < 200):
        new_cipher_generation = top_population(cipher_list, corpus_dict, encoded)
        while(len(new_cipher_generation) < len(cipher_list)):
                parent1 = weighted_random_choice(corpus_dict, encoded, cipher_list)
                parent2 = weighted_random_choice(corpus_dict, encoded, cipher_list)
                child1, child2 = one_point_crossover(parent1, parent2)
                new_cipher_generation += [mutate(child1)]
                new_cipher_generation += [mutate(child2)]

        cipher_list = new_cipher_generation
        generation += 1

    print(fitness(corpus_dict, encoded, cipher_list[0]))
    print(fitness(corpus_dict, corpus, (string.ascii_lowercase)))
    return encode_text(encoded, cipher_list[0])


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

