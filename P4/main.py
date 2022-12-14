import os
from os import path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from afinn import Afinn
import sys
# sys.path.insert(1, './spidy')

from crawler import spidy_main
from bs4 import BeautifulSoup

CRAWL_FOLDER='./saved'
NUMBER_OF_INDEX_TERMS=20

# Extract text from html files with BeautifulSoup
def get_text_from_pages(folder):
	extracted_texts = []
	for subdir, dirs, files in os.walk(folder):
		for filename in files:
			# only extracting text from html files
			if filename.endswith((".html")):
				filename = os.path.join(folder, filename)
				if path.exists(filename):
					# need to force encoding otherwise beutifulsoup cannot properly use codec
					file = open(filename, 'r', encoding="utf8")
					soup = BeautifulSoup(file.read(), 'lxml') 
					extracted_texts.append(soup.get_text())
					print("[SUCESS]: extracted text from " + filename)
				'''
				else:
					print("[ERROR]: cannot extract text from " + filename)
				'''
	print()
	return extracted_texts

# Compute AFINN score
def compute_afinn_score(text):
	afinn = Afinn()
	return afinn.score(text)

# Clusters
def cluster_collection(extracted_texts, true_k):
	cluster_top_terms = []

	# Vectorize
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(extracted_texts)

	# Apply k-means
	kmeans = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
	kmeans.fit(X)

	cluster_ids, cluster_sizes = np.unique(kmeans.labels_, return_counts=True)
	print(f"Number of elements asigned to each cluster: {cluster_sizes}")

	# Get top terms
	order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names_out()
	for i in range(true_k):
		current_words = ""
		for ind in order_centroids[i, :NUMBER_OF_INDEX_TERMS]:
			current_words += terms[ind] + ' '
		cluster_top_terms.append(current_words)

	return cluster_top_terms

def print_top_terms_and_afinn_score(top_terms):
	print(f"------ COMPUTING CLUSTER TOP {NUMBER_OF_INDEX_TERMS} TERMS AND THEIR AFINN SCORE WITH K={len(top_terms)} ------")
	for i in range(len(top_terms)):
		print(f"Top terms for cluster {i} with k = {len(top_terms)}: {top_terms[i]}")
		afinn_score = compute_afinn_score(top_terms[i])
		print(f"AFINN score for cluster {i} with k = {len(top_terms)}: {afinn_score}\n")	


if __name__ == "__main__":
	# Crawl Concordia Websites using Spidy Package
	ans = input('Do you want to run the crawler? y/n (crawled data is going to be saved in ./saved)')
	if (ans in ['y', 'Y']):
		spidy_main()

	# After execution, all the downloaded pages are in ./saved/
	print("\n------ EXCTRACTING TEXT WITH BeutifulSoup ------")
	extracted_texts = get_text_from_pages(CRAWL_FOLDER)

	print("\n------ CLUSTERING THE EXTRACTED TEXT WITH K=3 ------")
	top_terms_k3 = cluster_collection(extracted_texts, 3)
	print_top_terms_and_afinn_score(top_terms_k3)

	print("\n------ CLUSTERING THE EXTRACTED TEXT WITH K=6 ------")
	top_terms_k6 = cluster_collection(extracted_texts, 6)
	print_top_terms_and_afinn_score(top_terms_k6)