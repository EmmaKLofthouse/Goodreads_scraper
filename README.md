# Goodreads scraper

These scripts provide a simple method to pull data on books from Goodreads.com.

## Table of Contents

1. [Introduction](#introduction)
1. [Requirements](#requirements)
1. [Tutorial](#tutorial)
    1. [Output](#output)
    1. [Data Schema](#data-schema)


## Introduction

Goodreads is a social media platform for sharing books including quotes, 
ratings and reviews. This repository provides a web scraper to obtain a 
large dataset of books and outputs the results as a JSON file. 

## Requirements
The webscraper runs in python3 and the modules listed in requirements.txt 
must be installed. This can be easily done by running 
```
pip3 install -r requirements.txt
```

## Tutorial 
To run the web scraper use the command

```commandline
python3 goodreads_scraper.py <start> <end> <n_per_file>
```
Each book on the goodreads website is found at a separate address given by:
    www.goodreads.com/book/show/{bookID}

The scraper works by looping through successive bookIDs from the given 
 &lt;start&gt; value and ending when it reaches the given  &lt;end&gt; value. 

In addition, you can provide an optional  &lt;n_per_file&gt; value. This determines 
the number of books per output file. 

### Output

The web scraper outputs the data in JSON files with the name 

extracted_data_{i}_{j}.json 

where 

i = bookID of the first book

j = bookID of the last book

If a value for &lt;n_per_file&gt; is provided the code will output this many 
books 
per JSON file. This is used to ensure that, in the event of the 
scraper being interrupted, not all of the data is lost. 
The resulting files can then be combined into a single file by running 
```commandline
python3 combine_json.py
```

Alternatively, if &lt;n_per_file&gt; is not provided, the code will output a 
single file of the form extracted_data_{start}_{end}.json. 

### Data Schema 
The resulting data is in the form:

| Column             | Description                         |
|--------------------|-------------------------------------|
| title              | The book title                      |
| Number of pages    | number of pages in the book         |
| Language           | Language that the book is written in |
| Author             | Author's Name                       |
| Rating Value       | Average rating. From 0 to 5         |
| Rating Count       | Total number of ratings             |
| Review Count       | Total number of written reviews     |
| ISBN               | International Standard Book Number  |                       |
| Publication Date   | Date of publication                 |       