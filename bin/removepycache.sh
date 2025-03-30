echo "Buscando pycaches para remover"
find . -type d -name "__pycache__" ! -path "./env/*" | xargs echo
find . -type d -name "__pycache__" ! -path "./env/*" | xargs rm -r
echo "Pycaches deletados"