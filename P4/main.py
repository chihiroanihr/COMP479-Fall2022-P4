import os
from os import path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from afinn import Afinn

from crawler import spidy_main
from globals import *
from bs4 import BeautifulSoup

CRAWL_FOLDER='./saved'
NUMBER_OF_INDEX_TERMS=20

START_TIME = get_time()
START_TIME_LOG = get_time_log()
START_TIME_FLOAT = get_time_float()

# Log location
LOG_FILE_NAME = path.join('logs', 'scrape_log_{0}.txt'.format(START_TIME_LOG))
# Error log location
ERR_LOG_FILE = path.join('logs', 'scrape_error_log_{0}.txt'.format(START_TIME_LOG))

LOG_FILE = open_log(LOG_FILE_NAME)
LOGGER = create_logger('BS4', ERR_LOG_FILE)


# Extract text from html files with BeautifulSoup
def get_text_from_pages(folder):
	write_log(LOG_FILE, 'INIT', 'Starting scraping with BeautifulSoup', package='bs4')

	extracted_texts = []

	# Go through files in "/saved"
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

					# print("[SUCESS]: extracted text from " + filename)
					write_log(LOG_FILE, 'SCRAPE', 'Extracted text from: {0}'.format(filename), package='bs4')
				else:
					# print("[ERROR]: cannot extract text from " + filename)
					write_log(LOG_FILE, 'SCRAPE', 'Extracted text from: {0}'.format(filename), package='bs4', status='ERROR')
	print()
	return extracted_texts


# Clusters
def cluster_collection(extracted_texts, k):
	cluster_terms = []

	# Vectorize
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(extracted_texts)

	# Apply k-means
	kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
	kmeans.fit(X)

	cluster_ids, cluster_sizes = np.unique(kmeans.labels_, return_counts=True)
	print(f"Number of elements asigned to each cluster: {cluster_sizes}\n")

	# Get cluster terms
	order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names_out()
	for i in range(k):
		current_words = ""
		for ind in order_centroids[i, :]:
			current_words += terms[ind] + ' '
		cluster_terms.append(current_words)

	return cluster_terms

# Get top cluster terms
def get_top_cluster_terms(cluster_terms):
	cluster_top_terms = []
	k = len(cluster_terms)
	for i in range(k):
		current_words = ""
		lst_terms = cluster_terms[i].split(" ")
		for term in lst_terms[:NUMBER_OF_INDEX_TERMS]:
			current_words += term + ' '
		cluster_top_terms.append(current_words)

		print(f"Top {NUMBER_OF_INDEX_TERMS} terms for cluster {i} with k = {k}: \n{current_words}")

	return cluster_top_terms


# Compute AFINN score
def compute_afinn_score(cluster_terms):
	afinn_score_cluster_terms = []
	k = len(cluster_terms)

	for i in range(k):
		# Calulate AFINN score of each term
		afinn_score = Afinn().score(cluster_terms[i])
		num_words = len(cluster_terms[i].split())
		print(f"AFINN score for cluster {i} with k = {k} and top {num_words} terms: {afinn_score}")

		afinn_score_cluster_terms.append(afinn_score)

	return afinn_score_cluster_terms


# Output to file
def write_clusters_scores_to_file(result, k):
	# Create result file for clusters
	try:
		makedirs(WORKING_DIR + '/clusters')  # Attempts to make the logs directory
	except OSError:
		pass  # Assumes only OSError wil complain if /logs already exists

	FILE_NAME = path.join('clusters', 'k-{0}({1}).txt'.format(str(k)))
	FILE = open(FILE_NAME, 'w+', encoding='utf-8', errors='ignore')

	i = 0
	for top_cluster, top_score in result:
		num_words_top_clusters = len(top_cluster.split())
		FILE.write(f"Top {num_words_top_clusters} terms for cluster {i} with k = {k}: \n{top_cluster}\n")
		FILE.write(f"AFINN score for cluster {i} with k = {k} and top {num_words_top_clusters} terms: {top_score}\n\n")
		i += 1

	write_log(LOG_FILE, 'SAVE', 'Saved clusters to {0}'.format(FILE_NAME))


if __name__ == "__main__":
	# Crawl Concordia Websites using Spidy Package
	ans = input('Do you want to run the crawler? y/n (crawled data is going to be saved in ./saved)')
	if (ans in ['y', 'Y', 'yes', 'Yes', 'YES']):
		write_log(LOG_FILE, 'INIT', 'Creating variables...')
		spidy_main()

	# After execution, all the downloaded pages are in ./saved/
	print("\n------ EXCTRACTING TEXT WITH BeutifulSoup ------")
	extracted_texts = get_text_from_pages(CRAWL_FOLDER)

	print("\n------ CLUSTERING AND SCORING THE EXTRACTED TEXT WITH K=3 ------")
	cluster_terms_k3 = cluster_collection(extracted_texts, 3)
	top_cluster_terms_k3 = get_top_cluster_terms(cluster_terms_k3)
	afinn_score_k3 = compute_afinn_score(top_cluster_terms_k3)
	result = list(zip(top_cluster_terms_k3, afinn_score_k3))
	write_clusters_scores_to_file(result, 3)

	print("\n------ CLUSTERING AND SCORING THE EXTRACTED TEXT WITH K=6 ------")
	cluster_terms_k6 = cluster_collection(extracted_texts, 6)
	top_cluster_terms_k6 = get_top_cluster_terms(cluster_terms_k6)
	afinn_score_k6 = compute_afinn_score(top_cluster_terms_k6)
	result = list(zip(top_cluster_terms_k6, afinn_score_k6))
	write_clusters_scores_to_file(result, 6)