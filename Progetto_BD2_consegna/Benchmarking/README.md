```bash
	cd Benchmarking/
	gunzip trec_eval.8.1.tar.gz
	tar xf trec_eval.8.1.tar
	cd trec_eval.8.1
	make
	cd ..
	./trec.sh
	./get_maps.sh
	python evaluation.py
```
