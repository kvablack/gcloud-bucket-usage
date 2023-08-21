# if the directory data/ exists, print an error and exit
if [ -d "data" ]; then
    echo "data/ exists"
    exit 1
fi

# create the directory data/
mkdir data

gcloud storage ls | sed '/^gs:\/\//!d' | cut -d '/' -f 3 | parallel --bar --jobs 0 "gsutil du gs://{} | sed '/^0/d' | sed '/\/$/d' > data/{}.txt"
