.PHONY: test
all: extract transform load

extract:
	echo "Extracting...."
	python3 ./01_extract_organizations/extractOrganizations.py -o ./tmp/ -i ./organizations_15.csv

transform:
	echo "Transforming...."
	python3 ./02_transform/transform.py -o ./tmp/ -i ./organizations_15.csv

load:
	echo "Loading...."
	python3 ./03_load_publishers/loadPublishers.py -o ./tmp/ -i ./organizations_15.csv

clean:
	rm ./tmp/*.json
