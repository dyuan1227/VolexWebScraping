## Project explanation:

Parsing medical images from a website called DermQuest (prob not existing right now)using Beautiful soup
The results contains three columnL image_url, dx_label(acne vulgaris), lesion_label(nodulo cystic) 
The goal is to prepare 100 image urls per dx_label.

derm101.com/image_library

- get_categoies function: returns all the name of categories. Call the parse_response function to get the soup and find_all input tag and filter all the input with name attribute, input["name"]="tax_Case_Category" and has value attribute end with diagnosis
- parse_response function: Uses json.loads to grad the html and use beautifulsoup to return the soup
- get_response function: get a list of response using form_data(used) parse every single page/ post
- process_responses function: returns a list of img urls and only get the first 100 sources.
- is_empty_response function: if the p tag says Sorry, no images match your criteria return True
- search_category function: get_reponses, process_responses and output to csv
- out_put_csv function: csv output
