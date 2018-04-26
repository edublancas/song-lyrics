.PHONY: requirements get_data bootstrap report

requirements:
	echo 'Installing R packages...'
	./install_r_requirements

	echo 'Installing Python packages...'
	pip install -e process/pkg


get_data:
	echo 'Downloading data...'
	./get_data
	echo 'Done. Remember to manually download GloVe'

bootstrap:
	echo 'Boostrapping project...'
	./bootstrap

report:
	echo 'Building report...'
	cat report/1-intro.Rmd report/2-data-description.Rmd \
		report/3-data-quality.Rmd report/4-main-analysis.Rmd \
		report/5-executive-summary.Rmd report/7-conclusion.Rmd > report/final.Rmd
	./report/render report/final.Rmd
	mv report/final.html index.html
	echo 'Report in index.html'