import json
from chromadb.utils import embedding_functions
import chromadb
import uuid

class Food:
    def __init__(self, json_data) -> None:
        self.food = json_data
        self.food_id = json_data['food_id']
        self.food_name = json_data['food_name']
        self.food_description = json_data['food_description']
        self.food_calories_per_serving = json_data['food_calories_per_serving']
        self.food_nutritional_factors = json_data['food_nutritional_factors']
        self.food_ingredients = json_data.get('food_ingredients', [])
        self.food_health_benefits = json_data['food_health_benefits']
        self.cooking_method = json_data['cooking_method']
        self.cuisine_type = json_data['cuisine_type']
        self.food_features = json_data['food_features']
    
    def as_document (self) -> str:
        text = f"Name: {self.food_name}."
        text += f"Description: {self.food_description}"
        ingredients = ", ".join(self.food_ingredients)
        text += f"Ingredients: {ingredients}."
        text += f"Cuisine: {self.cuisine_type}."
        text += f"Cooking Method: {self.cooking_method}."
        return text
    
    def as_metadata(self):
        return {
            "food_id": self.food_id,
            "food_name": self.food_name
        } 

# Load Food Data
def load_food_data (path: str):
    """ 
    Load data set json from path, @TODO: Write a web loader
    """
    try:
        with open(file=path, mode='r', encoding='utf-8') as file:
            food_data = json.load(file)
    except Exception as e:
        print (f"Error loading data {e}")
    
    return food_data

def load_documents (json_data):
    ids = []
    documents = []
    metas =[]
    try:
        for index, _food in enumerate(json_data):
            food = Food(_food)
            documents.append(food.as_document())   
            ids.append(f"food_{food.food_id}_{str(uuid.uuid4().hex)}")
            metas.append(food.as_metadata())          
    except:
        pass

    return documents, ids, metas


def search (query: str):
    ef = embedding_functions.SentenceTransformerEmbeddingFunction('all-MiniLM-L6-v2')
    client = chromadb.Client()
    collection = client.create_collection(
        name="food_collection",
        metadata={"description": "Contains recipes and their "},
        configuration={
            "hnsw": {"space": "cosine"},
            "embedding_function": ef
        }
    )
    #Add Documents
    food_json = load_food_data("/home/aritra-mukherjee/projects/food-recommendation/dataset/FoodDataSet.json")
    docs, ids, metadatas = load_documents(food_json)
    #Adding into collection
    collection.add(
        documents=docs,
        ids=ids,
        metadatas=metadatas
    )
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results

print(search("Want to eat something asian"))
