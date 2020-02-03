.PHONY: test
all: extract transform load

extract:
	echo "Extracting...."
	python3 ./01_Extract/extract.py -o ./tmp/ -i ./organizations_01.csv

transform:
	echo "Transforming...."
	python3 ./02_Transform/transform.py -o ./tmp/ -i ./organizations_01.csv

load:
	echo "Loading...."
	python3 ./03_load/load.py -o ./tmp/ -i ./organizations_01.csv

clean:
	rm ./tmp/*.json
