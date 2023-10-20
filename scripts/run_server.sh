#cd ..
uvicorn server.__main__:app --host 0.0.0.0 --port $INNER_PORT