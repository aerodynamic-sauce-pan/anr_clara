#!/bin/bash
# Runs the static analysers and tests

case $1 in
all)
	list_dir=("src/" "tests/")
	;;
l)
	list_dir=("src/")
	;;
t)
	list_dir=("tests/")
	;;
"")
	list_dir=("src/")
	;;
*)
	list_dir=($1)
	;;
esac

for dir in ${list_dir[@]};
do
	echo -e "\n\e[1m++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo -e "        Working in \e[92m $dir \e[0m... "
	echo -e "\e[1m++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\e[0m"
	liste=$(find $dir -maxdepth ${2-1} -type f -iname '*.py' -not -path '*Tesseract_pre_processing/*' -not -path '*tfidf_monkey_learn/*' -not -path '*ipynb_checkpoints/*')
	for fichier in $liste;
	do
		if [[ $fichier != *"__init__.py"* ]] ; then
			echo -e " \e[1m\e[92m> \e[4m$fichier\e[0m"
			if [[ $fichier == *"tests/"* ]]  ; then
				echo -e "Running \e[95m\e[1m pytest\e[0m,\e[95m\e[1m coverage \e[0m on\e[92m ${fichier##*/} \e[39m..."
				coverage run -m pytest $fichier
				coverage report
			else
				echo -e "Running \e[95m\e[1m Flake8 \e[0m on\e[92m ${fichier##*/} \e[39m..."
				flake8 $fichier
				echo -e "Running \e[95m\e[1m Pylint \e[0m on\e[92m ${fichier##*/} \e[39m..."
				pylint $fichier
				echo -e "Running \e[95m\e[1m Pydocstyle \e[0m on\e[92m ${fichier##*/} \e[39m..."
				pydocstyle $fichier -v
				echo
			fi
		fi
	done
done
