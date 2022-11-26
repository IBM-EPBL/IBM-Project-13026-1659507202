# from Application.constants import username, password
import pymongo

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

DB_URI = "mongodb+srv://{}:{}@customercareregistrydb.4ubajvz.mongodb.net/?retryWrites=true&w=majority".format('HLrahul', '<password>')
client = pymongo.MongoClient(DB_URI)
db = client.users


logger = []
for query in db['query_table'].find({ "email" : "hari@gmail.com" }):
    logger.append(query)

print(logger)