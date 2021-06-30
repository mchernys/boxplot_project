PLOT_SRC=create_networks_and_plot.py
PLOT_EXE=python3
PROTEIN_LINKS_TXT=9606.protein.links.v11.0.txt.gz
PROTEIN_DOMAINS_TXT=proteins_w_domains.txt
BOXPLOT=protein_domains_vs_string_degree.png

.PHONY : all
all : $(BOXPLOT)

$(BOXPLOT) : $(PLOT_SRC) $(PROTEIN_LINKS_TXT) $(PROTEIN_DOMAINS_TXT)
	conda env create -f environment.yml
	conda run -n boxplot_env $(PLOT_EXE) $^

.PHONY : PROTEIN_LINKS_TXT
$(PROTEIN_LINKS_TXT) :
	wget https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz

.PHONY : PROTEIN_DOMAINS_TXT
$(PROTEIN_DOMAINS_TXT) :
	wget https://stockholmuniversity.box.com/shared/static/n8l0l1b3tg32wrzg2ensg8dnt7oua8ex
	mv n8l0l1b3tg32wrzg2ensg8dnt7oua8ex $(PROTEIN_DOMAINS_TXT)

.PHONY : clean
clean :
	rm -rf $(BOXPLOT)
	rm -rf $(PROTEIN_LINKS_TXT)
	rm -rf $(PROTEIN_DOMAINS_TXT)

.PHONY : variables
variables:
	@echo BOXPLOT: $(BOXPLOT)
	@echo PLOT_SRC: $(PLOT_SRC)
	@echo PLOT_EXE: $(PLOT_EXE)
	@echo PROTEIN_LINKS_TXT: $(PROTEIN_LINKS_TXT)
	@echo PROTEIN_DOMAINS_TXT: $(PROTEIN_DOMAINS_TXT)
