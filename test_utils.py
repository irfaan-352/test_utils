from fastapi import FastAPI,Query
from typing import Optional
from pydantic import BaseModel
import re
app = FastAPI()

class Input_Required(BaseModel):
    paragraph:Optional[str] = Query(None, description="Enter the paragraph fully")
    para_file:Optional[str] = Query(None, description="Enter the file name that has a paragraph")

app.paragraph_data = ""
app.output = {}

@app.get("/output")
def output():
    return app.output

@app.post("/input-paragraph")
def input_paragraph(paragraph:Input_Required):
    if paragraph.para_file:
        data = open(paragraph.para_file,"r",encoding="utf-8")
        app.paragraph_data = data.read()
    else:
        app.paragraph_data = paragraph.paragraph
    app.output["paragraph"] = app.paragraph_data
    return app.paragraph_data

@app.get("/lowercase")
def to_lowercase():
    app.output['paragraph_lower'] = app.paragraph_data.lower()
    return app.paragraph_data.lower()

@app.get("/uppercase")
def to_uppercase():
    app.output['paragraph_upper'] = app.paragraph_data.upper()
    return app.paragraph_data.upper()

@app.get("/special-characters")
def get_special_chars():
    tot_spl_characters = re.findall(r"[.!,’'\"]", app.paragraph_data)
    app.output['special_characters'] = len(tot_spl_characters)
    return f"The total number of special characters in the given paragraph is {len(tot_spl_characters)}"

@app.get("/words")
def words_in_paragraph():
    total_words = app.paragraph_data.replace(".", "").replace("!", "").split(" ")
    total_words_length = len(total_words)
    app.output['total_words'] = total_words_length
    return f"Total words are {total_words}",f"Total length of individual words is {total_words_length}"

@app.get("/additional-spaces")
def get_additional_spaces():
    additional_space_regex = r"[ ]{2,}"
    required_matches = re.findall(additional_space_regex,app.paragraph_data)
    app.output['additional_spaces'] = len(required_matches)
    return f"The no of additional spaces is {len(required_matches)}"
