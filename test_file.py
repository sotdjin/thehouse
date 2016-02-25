import os
import re
import sys
import math

def main():
    term_frequency = {}
    doc_query = {}
    doc_similarity = {}
    if len(sys.argv) < 2:
        sys.exit()

    if os.path.exists(sys.argv[2]):
        f = open(sys.argv[2])
        contents = f.read()
        f.close()
        for word in re.split("[^a-zA-Z]*", contents):
            if len(word) >= 3:
                if word not in doc_query:
                    doc_query[word] = 1.0
                else:
                    doc_query[word] += 1.0
    else:
        print 'No such location'
        sys.exit()

    path = sys.argv[1]
    if os.path.exists(path):
        file_names = os.listdir(path)
        total_documents = len(file_names)  # amount of documents N

        for words in doc_query:  # query DF
            for files in file_names:
                f = open(path + "/" + files)
                contents = f.read()
                contents = re.split("[^a-zA-Z]*", contents)
                f.close()
                count = contents.count(str(words))
                if count > 0:
                    if words in doc_query:
                        if words not in term_frequency:
                            term_frequency[words] = 1
                        else:
                            term_frequency[words] += 1

        for words in doc_query:
            idf = math.log10(float(total_documents)/term_frequency[words])  # query IDF
            doc_query[words] *= idf  # query TFIDF ~ weight

        for files in file_names:
            doc_dict = {}
            products = []
            total = 0
            doc_sum = 0

            f = open(path + "/" + files)
            contents = f.read()
            f.close()

            for word in re.split("[^a-zA-Z]*", contents):  # going through each word in the document
                if len(word) >= 3:
                    if word not in doc_dict:
                        doc_dict[word] = 1
                    else:
                        doc_dict[word] += 1

            for words in doc_dict:  # document TF-weight
                doc_dict[words] = 1 + math.log10(doc_dict[words])
            for words in doc_dict:  # document Sum(x^2)
                total += doc_dict[words] ** 2
            for words in doc_dict:  # document TF-weight/Sqrt(Sum(x^2)) ~ n'lized value
                doc_dict[words] = float(doc_dict[words])/math.sqrt(total)
            for words in doc_query:
                if words not in doc_dict:
                    prod = 0  # if word doesn't exist in document dictionary, product is 0
                else:
                    prod = doc_query[words] * doc_dict[words]  # product between query TFIDF and document n'lized val
                products.append(prod)
            for x in products:  # sum all of the products for similarity score (dot product)
                doc_sum += x
            if files not in doc_similarity:
                doc_similarity[files] = doc_sum  # put similarity score into dictionary with file

    else:
        print 'No such location'
        sys.exit()

    sorted_list = sorted(doc_similarity.items(), key=lambda x: x[1])
    sorted_list.reverse()
    for x in range(0, 5):
        print sorted_list[x]

if __name__ == '__main__':
    main()
