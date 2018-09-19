import xml.etree.ElementTree as ET
import os

def get_listing(filename_contents):
	listing = ""
	# remaining = ""
	end_marker = "</listing>"
	while True:
		line = filename_contents.readline()
		if end_marker in line:
			listing += line[line.index(end_marker): len(end_marker)]
			# remaining = line.replace(end_marker, "")
			break
		elif line == "":
			break
		else:
			listing += line
	return listing


def find_address_index(tree):
	for i, child in enumerate(tree):
		if child.tag == "address":
			return i
	return None

def add_city_element(listing, i):
	try:
		tree = ET.fromstring(listing)
		# We are assumning address is on number 9
		# and we are assuming city is in position 1
		try:
			assert tree[9][1].attrib['name'] == "city"
			city =  tree[9][1].text
		except:
			print("{} Order of tags is not correct".format(i))
			city = ""

		city_element = ET.Element("city")
		city_element.text = city

		tree.append(city_element)

		return ET.tostring(tree)
	except Exception as err:
		import pdb; pdb.set_trace()
		print err
		return None




def process_file_contents(filename_contents, output_file, skip=0):
	listing= get_listing(filename_contents)
	remaining = "<listing>"
	i = 0
	while listing != "":
		i += 1

		if remaining not in listing:
			listing = remaining + listing
		new_listing = add_city_element(listing, i)
		listing = get_listing(filename_contents)

		if new_listing is None:
			continue

		if i < skip:
			continue

		with open(output_file, "a") as result_file:
			result_file.write(new_listing)

		if i % 100 == 0:
			print "{} listings processed".format(i)


def rapid_count(filename_contents):
	counter = 0
	line = filename_contents.readline()
	while line != "":
		if "<listing>" in line:
			counter += 1
		line = filename_contents.readline()
		if counter % 10000 == 0:
			print "{} so far".format(counter)
	print "{} total".format(counter)

if __name__=="__main__":
	## CHANGE THIS VARIABLE
	## then click run.sh
	# filename = "AdrollFeed_9.17.xml"


	path = "/Users/marktrapani/Documents/Feeds/Adroll"


	input_folder = os.path.join(path, "input")
	output_folder = os.path.join(path, "output")

	all_files = [ f for f in os.listdir(input_folder) if ".xml" in f ]

	files_to_process = []

	for filename in all_files:
		if os.path.exists(os.path.join(output_folder, filename)):
			print("{} already processed".format(filename))
			continue
		files_to_process.append(filename)

	if len(files_to_process) == 0:
		print "Nothing to process"

	for filename in files_to_process:
		output_file = os.path.join(output_folder, filename)
		filename_contents = open(os.path.join(input_folder, filename), "r")

		# rapid_count(filename_contents)

		# 237979
		top_file = """<?xml version="1.0"?>
		<listings>
		  <title>Apartment List feed</title>
		  <link rel="self" href="https://www.apartmentlist.com"/>
		"""
		end_file = "</listings>"

		with open(output_file, "w") as result_file:
			result_file.write(top_file)

		process_file_contents(filename_contents, output_file)

		with open(output_file, "a") as result_file:
			result_file.write(end_file)

