import numpy as np
from pathlib import Path
import json
import logging

from pymilvus import MilvusClient, DataType, model
from pymilvus.bulk_writer import LocalBulkWriter

logger = logging.getLogger(__name__)

# local database
client = MilvusClient(uri="milvus-demo.db")

### remote database service
# client = MilvusClient(uri="http://localhost:19530")
# client.create_database(db_name="milvus-demo.db")
# client.use_database(db_name="milvus-demo.db")


# define the schema of the collection
schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="filename", datatype=DataType.VARCHAR, max_length=255, description="File name")
schema.add_field(field_name="text_dense", datatype=DataType.FLOAT_VECTOR, dim=768, description="Text embedding")
schema.add_field(field_name="image_dense", datatype=DataType.FLOAT_VECTOR, dim=512, description="Image embedding")
schema.verify()
logger.info("Schema: %s", json.dumps(schema.to_dict(), indent=2, ensure_ascii=False))

# create the collection
if client.has_collection(collection_name="multi_vector_demo"):
    client.drop_collection(collection_name="multi_vector_demo")
client.create_collection(
    collection_name="multi_vector_demo",
    schema=schema,
)

### insert items
image_desc = [
    "This image contains a cat.",
    "This picture shows a dog.",
    "This image is a landscape of a mountain.",
    "to be deleted.",
    "to be deleted.",
]
# encoding_fn = model.DefaultEmbeddingFunction()
# text_embeddings = encoding_fn(image_desc)

text_embeddings = np.random.rand(len(image_desc), 768).tolist()
image_embeddings = np.random.rand(len(image_desc), 512).tolist()
data_items = [
    {
        "id": i,
        "filename": f"image_{i}.png",
        "text_dense": text_embeddings[i],
        "image_dense": image_embeddings[i],
    } for i in range(len(image_desc))
]

BATCH_SIZE = 1000
for start in range(0, len(data_items), BATCH_SIZE):
    end = start + BATCH_SIZE
    batch_data = data_items[start:end]
    client.insert(
        collection_name="multi_vector_demo",
        data = batch_data,
    )


# 
logger.info("Collections: %s", client.list_collections())
info = client.describe_collection(collection_name="multi_vector_demo")
logger.info("Information: %s", json.dumps(info, indent=2, ensure_ascii=False))
stats = client.get_collection_stats(collection_name="multi_vector_demo")
logger.info("Stats: %s", json.dumps(stats, indent=2, ensure_ascii=False))
# print("Row count:", stats["row_count"])

# update an item: update and insert -> upsert
client.upsert(
    collection_name="multi_vector_demo",
    data=[{
        "id": 0,
        "filename": "image_0.png",
        "text_dense": np.random.rand(768).tolist(),
        "image_dense": np.random.rand(512).tolist(),
    }],
    partial_update=True,
)


# delete items
res = client.delete(collection_name="multi_vector_demo", ids=[3,4])

stats = client.get_collection_stats(collection_name="multi_vector_demo")
logger.info("Stats: %s", json.dumps(stats, indent=2, ensure_ascii=False))