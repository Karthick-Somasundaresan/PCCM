import sqlite3
conn = sqlite3.connect("/Users/karsomas/BITS/Project/data/sqlite_dbs/WordFrequency.db")

cursor = conn.cursor()
# results = cursor.execute(cmd).fetchall()
# print len(results)
# for rows in results:
#     print "Word:" + rows[0]
#     print "Freq:" + rows[1]


def get_freq_details(words):
    word_list = list(words)
    print "Number of words:", len(word_list)

    # formed_clause = ""
    # for word in word_list:
    #     if formed_clause == "":
    #         formed_clause = "Word=\"" + word +"\""
    #     else:
    #         formed_clause = formed_clause + " OR Word=\"" + word + "\""
    formed_clause = ""
    for word in word_list:
        print word
        if formed_clause == "":
            formed_clause = "\'" + word + "\'"
        else:
            formed_clause = formed_clause + ",\'" + word + "\'"

    print "formed_clause:", formed_clause
    formed_cmd = "".join("select Word, Lg10WF from SUBTLEX_US where Word in (")
    formed_cmd = formed_cmd + formed_clause
    formed_cmd = formed_cmd + ")"
    print formed_cmd


    print "Formed command:", formed_cmd
    results = cursor.execute(formed_cmd).fetchall()
    result_json = {}
    for rows in results:
        result_json[rows[0]] = float(rows[1])
        word_list.remove(rows[0])
    for word in word_list:
        result_json[word] = 0

    return result_json


words = ["create", "abbas", "body"]
res = get_freq_details(words)
print "Response:"
print res
print "Orig list:"
print words
