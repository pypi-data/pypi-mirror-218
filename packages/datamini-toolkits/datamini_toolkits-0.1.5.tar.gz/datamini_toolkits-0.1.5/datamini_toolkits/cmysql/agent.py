from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph

class ChatMySQLCLI(object):
    def __init__(self):
        self.graph = Neo4jGraph(
            url="bolt://localhost:32768", username="neo4j", password="Pass1234"
        )

        self.llm = ChatOpenAI()






