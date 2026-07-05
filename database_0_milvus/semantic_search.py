import numpy as np
from pymilvus import MilvusClient, model

client = MilvusClient(uri="milvus-demo.db")

# encoding_fn = model.DefaultEmbeddingFunction()
# query_vector = encoding_fn.encode_queries(["a cat"])[0]
query_vector = np.random.rand(768).tolist()

results = client.search(
    collection_name="multi_vector_demo",
    data=[query_vector],
    anns_field="text_dense",
    limit=3,
    output_fields=["id", "filename"],
)

print(results)