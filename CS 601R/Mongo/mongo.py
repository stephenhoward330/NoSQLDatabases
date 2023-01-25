import pymongo
from random import randint
from tqdm import tqdm


def gen_data(num_data):
    print("Generating data...")
    first_names = ["Saniya", "Esperanza", "Nathan", "Jaylin", "Kinsley", "Caleb", "Karly", "Nikhil", "Parker", "Mario",
                   "Nia", "Curtis", "Kristen", "Alena", "Itzel", "Heidi", "Dexter", "Olive", "Valentino", "Lauren"]
    last_names = ["Hays", "Wood", "Ross", "Evans", "Proctor", "Boyd", "Huang", "Hickman", "Wilcox", "Duffy",
                  "Villanueva", "Gilmore", "Frederick", 'Vaughn', "Maldonado", "Richard", "Jensen", "Zimmerman",
                  "Holder", "Larsen"]
    dogs = ["Zeus", "Oscar", "Bud", "Payton", "Winston", "Rufus", "Sammy", "Lola", "Astro", "Baxter", "Milo", "Polo",
            "Cash", "Thor", "Oreo", "Chester", "Ellie", "Bandit", "Honey", "Roxie"]
    jobs = ["Doctor", "Athlete", "Dog walker", "Driver", "Artist", "Programmer", "Chef", "Scientist", "Teacher", "Cop"]
    for _ in tqdm(range(num_data)):
        new_doc = {
            "Name": first_names[randint(0, 19)] + ' ' + last_names[randint(0, 19)],
            "Age": randint(18, 100),
            "Job": jobs[randint(0, 9)],
            "Salary": randint(5, 25) * 10000,
            "Dog": dogs[randint(0, 19)]
        }
        db.people.insert_one(new_doc)


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb+srv://stephenmongo:BvZvmHUd01nANkpT@cluster0.kycvh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.project

    # gen_data(1000)

    groups = db.people.aggregate(
        [
            {'$group':
                 {"_id": "$Job",
                  "count": {'$sum': 1},
                  "avgSal": {'$avg': "$Salary"},
                  "avgAge": {'$avg': "$Age"}
                  }
             },
            {"$sort":
                 {"avgSal": -1}
             }
        ])

    for group in groups:
        print(group['_id'])
        print('\tAverage Salary:', round(group['avgSal']))
        print('\tAverage Age:', round(group['avgAge']))
        print('\tCount:', group['count'])
