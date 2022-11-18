import json

def credit_filter(people_dict, credit_dict):
    credit_list = []
    print(people_dict)
    for person in people_dict:
        print(person)
        if person['pk'] in credit_dict:
            credit_list.append(person)

    with open("credit_list.json", "w", encoding="utf-8") as w:
        json.dump(credit_list, w, indent="\t", ensure_ascii=False)


people_json = open("people_list.json", encoding="utf-8")
people_dict = json.load(people_json)

credit_json = open("credit.json", encoding="utf-8")
credit_dict = json.load(credit_json)

credit_filter(people_dict, credit_dict)