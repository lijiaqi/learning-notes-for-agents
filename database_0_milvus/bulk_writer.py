from pathlib import Path
import numpy as np

from pymilvus import MilvusClient, DataType
from pymilvus.bulk_writer import LocalBulkWriter, bulk_import, BulkFileType

# define the schema
schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="filename", datatype=DataType.VARCHAR, max_length=255, description="File name")
schema.add_field(field_name="text_dense", datatype=DataType.FLOAT_VECTOR, dim=768, description="Text embedding")
schema.add_field(field_name="image_dense", datatype=DataType.FLOAT_VECTOR, dim=512, description="Image embedding")
schema.verify()
print(schema)

data_path = Path("bulk_data")

### write data to local files
if not data_path.exists():
    writer = LocalBulkWriter(schema=schema, local_path="bulk_data", file_type=BulkFileType.PARQUET)
    for i in range(1000000):
        writer.append_row(
            {
                "id": i,
                "filename": f"file_{i}.png",
                "text_dense": np.random.rand(768),
                "image_dense": np.random.rand(512),
            }
        )
    writer.flush()
else:
    bulk_import(collection_name="milvus-demo")