import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
import uuid
import sys


def main(file_path, db_host, db_port, collection_name):
    with open(file_path) as f:
        s = f.read()
        
    json_data = json.loads(s).values()

    sentences = []
    for d in json_data:
        sentences.append(d["text"])
    
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = model.encode(sentences, convert_to_tensor=True)
    
    client = QdrantClient(db_host, port=db_port)

    collection = collection_name
    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    def to_point(vector, payload):
        return PointStruct(id = str(uuid.uuid4()), vector = vector, payload = payload)

    def create_points(vectors, data):
        points = []
        for i, item in enumerate(data):
            points.append(to_point(vectors[i], item))
        return points

    points = create_points(embeddings, list(json_data))

    client.upsert(
        collection_name=collection,
        wait=True,
        points=points
    )




if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])