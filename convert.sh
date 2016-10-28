for file in ./*.docx; do
	unoconv -f html -o html $file;
done
