# gcloud-bucket-usage

## Usage:
Make sure the Google Cloud SDK is installed and configured.

Install requirements:
```
pip install flask gunicorn tqdm
```

First, collect raw sizes for every object in every bucket. The following script does that and stores the results to the `data/` directory.
```
bash collect_usage.sh
```

Now, run the Flask app, which reads from `data/`, builds a tree data structure in memory, and serves a simple interactive explorer of that tree. For debugging, you can use `python app.py`. For slightly more productionized serving, I use gunicorn with the `--preload` option, which shares the data structure between workers to save memory.
```
gunicorn "app:app" --preload -w <num_workers>
```