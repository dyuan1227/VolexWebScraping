import sys
import json
import multiprocessing.dummy
import requests
import csv
from bs4 import BeautifulSoup

def main():
	if len(sys.argv) > 1 and sys.argv[1] == "get_categories":
		categories = get_categories()
		for category in categories:
			print category
		return 0

	categories = set([
		#("acne-vulgaris-diagnosis", "Acne Vulgaris", "Acne Vulgaris"),
		("acne-vulgaris-nodulocystic-diagnosis", "acne vulgaris","nodulo cystic"),
		("hirsutism-diagnosis","hirsutism","hirsutism")

	])
	pool = multiprocessing.dummy.Pool(100)
	pool.map(lambda category: search_category(*category), categories)
	return 0

def get_categories():
	#This returns all the name of categories
	with requests.Session() as sesh:
	    response = sesh.get("https://www.derm101.com/image-library/")
	    all_inputs = parse_response(response).find_all('input')
	    category_inputs = filter(lambda input: input.has_attr("name") and input["name"] == "tax_case_category[]" and input.has_attr("value") and input["value"].endswith("diagnosis"), all_inputs)
	    categories = map(lambda input: input["value"], category_inputs)
	return categories


def search_category(tax_case_category, dx_label, lesion_label):
	responses = get_responses(tax_case_category)
	images = process_responses(responses)
	result = map(lambda image: (image, dx_label, lesion_label), images)
	output_csv(result, tax_case_category)

def output_csv(result, csv_file_name):
	with open('{}.csv'.format(csv_file_name), 'wb') as csvfile:
	    a = csv.writer(csvfile, delimiter=',')
	    for row in result:
	    	a.writerow(row)


def get_responses(tax_case_category):
	#Get a list of response
	responses = []
	with requests.Session() as sesh:
	    form_data = {
	    	"action": "wpas_ajax_load",
	    	"page": None,
	    	"form_data":"match=IN&tax_case_category%5B%5D={}&wpas_id=my-form&wpas_submit=1&posts_per_page=96".format(tax_case_category)
	    }
	    page = 1
	    response = None
	    while True:
	    	form_data["page"] = page
	    	print "Searching for {}, page {}".format(tax_case_category, page)
	    	#sesh.request("POST", "https://www.derm101.com/wp-admin/admin-ajax.php", data=form_data)
	    	response = sesh.post("https://www.derm101.com/wp-admin/admin-ajax.php", data=form_data)
	    	if is_empty_response(response):
	    		break
	    	responses.append(response)
	    	page += 1
	return responses

def parse_response(response):
	#This returns the prettified html
	try:
		html = json.loads(response.text)["results"]  # grab the html
	except Exception as e:
		html = response.text
	
	soup = BeautifulSoup(html, 'html.parser')
	return soup


def is_empty_response(response):
	#stoping condition
	try:
		soup = parse_response(response)
		for p in soup.find_all('p'):
			if p.get_text() == "Sorry, no images matched your criteria.":
				return True
		return False
	except Exception as e:
		return True

def process_responses(responses):
	#returns a list of img urls
	soups = [parse_response(response) for response in responses]
	sources = []
	for soup in soups:
		images = soup.find_all('img')
		images = filter(lambda image: image.has_attr("class") and "case-img" in image['class'], images)
		sources += map(lambda image: image['src'], images)
	if len(sources)>100:
		sources=sources[:100]
		print sources

	return sources


if __name__ == '__main__':
	main()