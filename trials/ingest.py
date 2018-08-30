import sys
import json
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import trials.utils as utils
import sqlite3


def get_assetId():
    assetId = None
    ingest_db_conn = utils.get_db_conn("/Users/karsomas/BITS/Project/data/sqlite_dbs/Ingest.db")
    ingest_cursor = ingest_db_conn.cursor()
    last_row_cmd = """SELECT AssetId from MovieInfo order by AssetId desc limit 1"""
    result = ingest_cursor.execute(last_row_cmd)
    for row in result:
        assetId = row[0]
    return int(assetId) + 1



def pos_tag_movie(movie_info):
    assetId = get_assetId()
    line_dict = {}
    captionPath = movie_info["SubtitlePath"]
    tagger = StanfordPOSTagger('data/models/wsj-0-18-bidirectional-distsim.tagger', '3rdparty_libs/stanford-postagger.jar')
    dialogues = utils.get_movie_dialogues(captionPath)
    for line in dialogues.split('\n'):
        print("Tagging line:", line)
        tagged_sent = tagger.tag(word_tokenize(line))
        line_dict[line] = tagged_sent
    
    fileName = "data/"+ assetId + "_tagged_lines.json"
    movie_info["TaggedSubtitlePath"] = fileName
    with open(fileName, "w") as fp:
        json.dump(line_dict, fp)
    
    try:
        ingest_cursor.execute('''Insert into MovieInfo(MovieName, MoviePath, SubtitlePath, PosterPath, TaggedSubtitlePath) values(?, ?, ?, ?, ?)''', (movie_info["MovieName"], movie_info["MoviePath"], movie_info["SubtitlePath"], movie_info["PosterPath"], movie_info["TaggedSubtitlePath"]))
        ingest_db_conn.commit()
    except sqlite3.IntegrityError as IE:
        for row in result:
            assetId = row[0]
    ingest_db_conn.close()

    print("Successfully tagged file:", captionPath, " Tagged file is present in :", fileName)
    

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: ingest.py <Movie Name> <Movie path> <webvtt path> <poster img path>")
    else:
        movie_info = {}
        movie_info["MovieName"] = sys.argv[1]
        movie_info["MoviePath"] = sys.argv[2]
        movie_info["SubtitlePath"] = sys.argv[3]
        movie_info["PosterPath"] = sys.argv[4]
        pos_tag_movie(movie_info)

        print("AssetId:", assetId, " Subtitle Path:", sys.argv[3])
        pos_tag_movie(assetId, sys.argv[3])
