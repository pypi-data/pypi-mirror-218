import os
import pymongo
import pytest
import logging
import copy
from dotenv import load_dotenv, find_dotenv

from mongodb_python_manager import MongoDBManager

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="module")
def mongodb_manager():
    # Initialize the MongoDBManager with test database name and credentials
    mongodb_manager = MongoDBManager(
        mongo_db_user=os.environ.get('MONGO_DB_USER'),
        mongo_db_password=os.environ.get('MONGO_DB_PASSWORD'),
        mongo_db_cluster=os.environ.get('MONGO_DB_CLUSTER'),
        mongodb_db_name="MongoDBPythonManagerTest"
    )
    return mongodb_manager


class TestMongoDBManager:

    def test_os_env_variables(self):
        # Ensure the environment variables are set
        assert os.environ.get('MONGO_DB_USER') is not None
        assert os.environ.get('MONGO_DB_PASSWORD') is not None
        assert os.environ.get('MONGO_DB_CLUSTER') is not None

    def test_get_client(self, mongodb_manager):
        # Ensure the connection is successfully established
        client = mongodb_manager.get_client()
        assert client is not None
        assert isinstance(client, pymongo.MongoClient)

    def test_set_collection_name(self, mongodb_manager):
        # Ensure the collection name is set
        mongodb_manager.set_collection_name("test_collection")
        assert mongodb_manager.get_collection_name() == "test_collection"

    def test_get_db_name(self, mongodb_manager):
        # Ensure the database name is returned
        assert mongodb_manager.get_db_name() == "MongoDBPythonManagerTest"

    def test_get_collection_name(self, mongodb_manager):
        # Ensure the collection name is returned
        mongodb_manager.set_collection_name("test_collection")
        assert mongodb_manager.get_collection_name() == "test_collection"

    def test_get_collection(self, mongodb_manager):
        # Ensure the collection is returned
        mongodb_manager.set_collection_name("test_collection")
        collection = mongodb_manager.get_collection()
        assert collection is not None
        assert isinstance(collection, pymongo.collection.Collection)

    def test_get_collection_without_setting_collection_name(self):
        # Ensure ValueError is raised when collection name is not set
        mongodb_manager = MongoDBManager(
            mongo_db_user=os.environ.get('MONGO_DB_USER'),
            mongo_db_password=os.environ.get('MONGO_DB_PASSWORD'),
            mongo_db_cluster=os.environ.get('MONGO_DB_CLUSTER'),
            mongodb_db_name=None,
        )
        with pytest.raises(ValueError):
            mongodb_manager.get_collection()

    def test_get_collection_without_setting_db_name(self):
        # Ensure ValueError is raised when database name is not set
        mongodb_manager = MongoDBManager(
            mongo_db_user=os.environ.get('MONGO_DB_USER'),
            mongo_db_password=os.environ.get('MONGO_DB_PASSWORD'),
            mongo_db_cluster=os.environ.get('MONGO_DB_CLUSTER'),
            mongodb_db_name="MongoDBPythonManagerTest"
        )
        with pytest.raises(ValueError):
            mongodb_manager.get_collection()

    def test_get_distinct_documents_from_collection(self, mongodb_manager):
        # Ensure the distinct documents are returned
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"name": "Document 1", "type": "PDF"},
            {"name": "Document 2", "type": "Word"},
            {"name": "Document 1", "type": "PDF"},
            {"name": "Document 2", "type": "Word"},
        ]

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )

        collection = mongodb_manager.get_collection()

        data_doc_1 = [y for y in collection.find({"name": "Document 1"})]
        data_doc_2 = [y for y in collection.find({"name": "Document 2"})]

        assert data_doc_1 is not None
        assert isinstance(data_doc_1, list)
        assert len(data_doc_1) == 2

        assert data_doc_2 is not None
        assert isinstance(data_doc_2, list)
        assert len(data_doc_2) == 2

        distinct_documents = mongodb_manager.get_distinct_documents_from_collection(
            field="name"
        )

        assert distinct_documents is not None
        assert isinstance(distinct_documents, list)
        assert len(distinct_documents) == 2

    def test_get_uri(self, mongodb_manager):
        # Ensure the URI is returned
        uri = mongodb_manager.get_uri()
        assert uri is not None
        assert isinstance(uri, str)

    def test_insert_document_in_collection(self, mongodb_manager):
        # Ensure the document is inserted in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        item = {"test_one_item": "test_one_item"}

        mongodb_manager.insert_document_in_collection(
            item=item
        )

        collection = mongodb_manager.get_collection()

        data = collection.find_one({"test_one_item": "test_one_item"})

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item"] == "test_one_item"
        assert f"{collection_name}_id" in data.keys()
        # Ensure to have a date field in the collection
        assert "date" in data.keys()
        # Ensure the collection name is in the built-in collection id
        assert collection_name in data[f"{collection_name}_id"]

    def test_insert_many_document_in_collection(self, mongodb_manager):
        # Ensure the document is inserted in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"test_many_content_1": "test_many_content_1"},
            {"test_many_content_2": "test_many_content_2"}
        ]

        origin_items = copy.deepcopy(items)

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )
        collection = mongodb_manager.get_collection()

        for item in origin_items:
            for k, v in item.items():
                data = collection.find_one({k: v})
                assert data is not None
                assert isinstance(data, dict)
                assert data[k] == v
                assert f"{collection_name}_id" in data.keys()
                # Ensure to have a date field in the collection
                assert "date" in data.keys()
                # Ensure the collection name is in the built-in collection id
                assert collection_name in data[f"{collection_name}_id"]

    def test_update_document_in_collection(self, mongodb_manager):
        # Ensure the document is updated in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        item = {"test_one_item": "test_one_item"}

        mongodb_manager.insert_document_in_collection(
            item=item
        )

        collection = mongodb_manager.get_collection()

        data = collection.find_one({"test_one_item": "test_one_item"})

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item"] == "test_one_item"
        assert f"{collection_name}_id" in data.keys()
        # Ensure to have a date field in the collection
        assert "date" in data.keys()
        # Ensure the collection name is in the built-in collection id
        assert collection_name in data[f"{collection_name}_id"]

        data["test_one_item"] = "test_one_item_updated"

        # Update the document
        mongodb_manager.update_document_in_collection(
            item=data,
            collection_id=data[f"{collection_name}_id"],
        )

        data = collection.find_one({"test_one_item": "test_one_item_updated"})

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item"] == "test_one_item_updated"
        assert f"{collection_name}_id" in data.keys()
        # Ensure to have a date field in the collection
        assert "date" in data.keys()
        # Ensure the collection name is in the built-in collection id
        assert collection_name in data[f"{collection_name}_id"]

    def test_update_document_in_collection_based_on_id(self, mongodb_manager):
        # Ensure the document is updated in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        item = {
            "test_one_item_update_document_in_collection_based_on_id": "test_one_item_update_document_in_collection_based_on_id",
            "id_update_document_in_collection_based_on_id": "test_id_update_document_in_collection_based_on_id"
        }

        mongodb_manager.insert_document_in_collection(
            item=item
        )

        collection = mongodb_manager.get_collection()

        data = collection.find_one(
            {
                "id_update_document_in_collection_based_on_id": "test_id_update_document_in_collection_based_on_id"
            }
        )

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item_update_document_in_collection_based_on_id"] == "test_one_item_update_document_in_collection_based_on_id"
        assert data["id_update_document_in_collection_based_on_id"] == "test_id_update_document_in_collection_based_on_id"
        assert f"{collection_name}_id" in data.keys()
        # Ensure to have a date field in the collection
        assert "date" in data.keys()
        # Ensure the collection name is in the built-in collection id
        assert collection_name in data[f"{collection_name}_id"]

        data["test_one_item_update_document_in_collection_based_on_id"] = "test_one_item_update_document_in_collection_based_on_id_updated"
        print("data", data)

        # Update the document
        mongodb_manager.update_document_in_collection(
            item=data,
            collection_id_name="id_update_document_in_collection_based_on_id",
            collection_id=data["id_update_document_in_collection_based_on_id"],
        )

        data = collection.find_one(
            {
                "id_update_document_in_collection_based_on_id": "test_id_update_document_in_collection_based_on_id"
            }
        )

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item_update_document_in_collection_based_on_id"] == "test_one_item_update_document_in_collection_based_on_id_updated"
        assert f"{collection_name}_id" in data.keys()
        # Ensure to have a date field in the collection
        assert "date" in data.keys()
        # Ensure the collection name is in the built-in collection id
        assert collection_name in data[f"{collection_name}_id"]
        assert data["id_update_document_in_collection_based_on_id"] == "test_id_update_document_in_collection_based_on_id"

    def test_update_many_documents_in_collection(self, mongodb_manager):
        # Ensure the documents are updated in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"test_many_content_1_update_many": "test_many_content_1_update_many"},
            {"test_many_content_2_update_many": "test_many_content_2_update_many"}
        ]

        origin_items = copy.deepcopy(items)

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )
        collection = mongodb_manager.get_collection()

        for item in origin_items:
            for k, v in item.items():
                data = collection.find_one({k: v})
                assert data is not None
                assert isinstance(data, dict)
                assert data[k] == v
                assert f"{collection_name}_id" in data.keys()
                # Ensure to have a date field in the collection
                assert "date" in data.keys()
                # Ensure the collection name is in the built-in collection id
                assert collection_name in data[f"{collection_name}_id"]

        # Update the documents
        for item in items:
            for k, v in item.items():
                item[k] = f"{v}_updated"

        mongodb_manager.update_many_documents_in_collection(
            items=items,
        )
        collection = mongodb_manager.get_collection()
        items = mongodb_manager.get_all_documents_from_collection()

        for item in origin_items:
            for k, v in item.items():
                data = collection.find_one({k: f"{v}_updated"})
                assert data is not None
                assert isinstance(data, dict)
                assert data[k] == f"{v}_updated"
                assert f"{collection_name}_id" in data.keys()
                # Ensure to have a date field in the collection
                assert "date" in data.keys()
                # Ensure the collection name is in the built-in collection id
                assert collection_name in data[f"{collection_name}_id"]

    def test_update_many_documents_in_collection_based_on_id(self, mongodb_manager):
        # Ensure the documents are updated in the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"test_many_content_1_update_many": "test_many_content_1_update_many",
                "id_update_many": "test_many_content_1_update_many"},
            {"test_many_content_2_update_many": "test_many_content_2_update_many",
                "id_update_many": "test_many_content_2_update_many"}
        ]

        origin_items = copy.deepcopy(items)

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )
        collection = mongodb_manager.get_collection()

        for item in origin_items:
            for k, v in item.items():
                data = collection.find_one({k: v})
                assert data is not None
                assert isinstance(data, dict)
                assert data[k] == v
                assert f"{collection_name}_id" in data.keys()
                # Ensure to have a date field in the collection
                assert "date" in data.keys()
                # Ensure the collection name is in the built-in collection id
                assert collection_name in data[f"{collection_name}_id"]

        # Update the documents
        for item in items:
            for k, v in item.items():
                item[k] = f"{v}_updated"

        mongodb_manager.update_many_documents_in_collection(
            items=items,
            collection_id_name="id_update_many"
        )
        collection = mongodb_manager.get_collection()
        items = mongodb_manager.get_all_documents_from_collection()

        for item in origin_items:
            for k, v in item.items():
                data = collection.find_one({k: f"{v}_updated"})
                assert data is not None
                assert isinstance(data, dict)
                assert data[k] == f"{v}_updated"
                assert f"{collection_name}_id" in data.keys()
                # Ensure to have a date field in the collection
                assert "date" in data.keys()
                # Ensure the collection name is in the built-in collection id
                assert collection_name in data[f"{collection_name}_id"]

    def test_get_all_documents_from_collection(self, mongodb_manager):
        # Ensure the documents are returned from the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"test_many_content_1_to_get": "test_many_content_1_to_get"},
            {"test_many_content_2_to_get": "test_many_content_2_to_get"}
        ]

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )
        collection = mongodb_manager.get_all_documents_from_collection()

        assert collection is not None
        assert isinstance(collection, list)
        assert len(collection) > 0

    def test_delete_content_in_collection(self, mongodb_manager):
        # Ensure the content is deleted from the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        item = {"test_one_item_to_delete": "test_one_item_to_delete"}

        mongodb_manager.insert_document_in_collection(
            item=item
        )

        collection = mongodb_manager.get_collection()

        data = collection.find_one(
            {"test_one_item_to_delete": "test_one_item_to_delete"})

        assert data is not None
        assert isinstance(data, dict)
        assert data["test_one_item_to_delete"] == "test_one_item_to_delete"

        # Delete the document
        mongodb_manager.delete_content_in_collection(
            collection_id=data[f"{collection_name}_id"],
        )

        data = collection.find_one(
            {"test_one_item_to_delete": "test_one_item_to_delete"})

        assert data is None

    def test_delete_all_documents_from_collection(self, mongodb_manager):
        # Ensure the content is deleted from the collection
        collection_name = "test_collection"
        mongodb_manager.set_collection_name(collection_name)

        items = [
            {"test_many_content_1_to_delete": "test_many_content_1_to_delete"},
            {"test_many_content_2_to_delete": "test_many_content_2_to_delete"}
        ]

        mongodb_manager.insert_many_document_in_collection(
            items=items
        )

        mongodb_manager.delete_all_documents_from_collection()

        collection = mongodb_manager.get_all_documents_from_collection()

        assert collection is not None
        assert isinstance(collection, list)
        assert len(collection) == 0
