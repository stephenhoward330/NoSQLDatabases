from neo4j import GraphDatabase


# Browser: http://localhost:7474
class Neo4jDriver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_node(self, t, n):
        with self.driver.session() as session:
            result = session.run("CREATE (a:"+t+" {name: '"+n+"'}) RETURN a.name")
            print("\tAdded node:", result.single()[0])

    def add_relationship(self, rel, n1, n2):
        with self.driver.session() as session:
            result = session.run("MATCH (a), (b) "
                                 "WHERE a.name = '"+n1+"' AND b.name = '"+n2+"' "
                                 "CREATE (a)-[r:"+rel+"]->(b) RETURN type(r)")
            labels = result.value()
            if len(labels) > 0:
                print(f"\t{labels[0]} relationship added from {n1} to {n2}")
            else:
                print("\tFailed to add relationship!")

    def del_node(self, n):
        with self.driver.session() as session:
            session.run("MATCH (n) WHERE n.name = '"+n+"' DETACH DELETE n")
            print("\tDeleted:", n)

    def view(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            records = result.value()
            print(f"\tNODES ({len(records)})")
            for i, record in enumerate(records):
                n = record['name']
                t = list(record.labels).pop()
                print(f"\t {i+1}. {n}:{t}")

            result = session.run("MATCH (n1)-[r]->(n2) RETURN r, n1, n2")
            records = result.value()
            print(f"\n\tRELATIONSHIPS ({len(records)})")
            for i, rel in enumerate(records):
                n1 = rel.start_node['name']
                t = rel.type
                n2 = rel.end_node['name']
                print(f"\t {i+1}. {n1} \t--{t}--> \t{n2}")

    def clear(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("\tAll data cleared!")


def instruct():
    print("\nEnter 'a' to add a node")
    print("Enter 'r' to add a directed relationship between two existing nodes")
    print("Enter 'd' to delete a node (and all of its relationships)")
    print("Enter 'v' to view all nodes")
    print("Enter 'clear' to clear all nodes and relationships")
    print("Enter 'q' to quit")


if __name__ == "__main__":
    neo = Neo4jDriver("bolt://localhost:7687", "neo4j", "abc123")

    print("Welcome to my neo4j program!")
    print("Check out the browser!  http://localhost:7474")
    instruct()

    while True:
        x = input("\nEnter selection: ")
        if x == 'a':
            n_in = input("\tEnter name: ")
            t_in = input("\tEnter node type: ")
            neo.add_node(t_in.lower().capitalize(), n_in)
        elif x == 'r':
            thing1 = input("\tEnter first name: ")
            thing2 = input("\tEnter second name: ")
            r = input("\tEnter relationship: ")
            neo.add_relationship(r.upper(), thing1, thing2)
        elif x == 'd':
            n_in = input("\tEnter name: ")
            neo.del_node(n_in)
        elif x == 'v':
            neo.view()
        elif x == 'clear':
            neo.clear()
        elif x == 'q':
            print("Thanks!")
            break
        else:
            instruct()

    neo.close()
