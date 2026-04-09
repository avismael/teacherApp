@echo off
echo Compilando Tailwind CSS...
npx tailwindcss -i ./static/css/tailwind_src.css -o ./static/css/tailwind.css --minify
echo Finalizado.
pause
