import boto3
from collections.abc import Generator

class S3Operations:
    #####################################################################
    def __get_client(self, access_key_id=None, secret_access_key=None):
        client = None
        if access_key_id:
            client = boto3.Session().client(
                service_name='s3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
        else:
            client = boto3.Session().client('s3')
        return client

    #####################################################################
    def list_objects(  # analog to find_children_objects
        self,
        bucket_name,
        prefix,
        access_key_id=None,
        secret_access_key=None
    ):
        """Finds all child objects for a given prefix in a s3 bucket.

        Parameters
        ----------
        bucket_name : str
            Name of bucket to read from.
        prefix : str
            Prefix path to folder containing children objects.
        access_key_id : str
            AWS access key id. Optional.
        secret_access_key : str
            AWS access key secret. Optional.

        Returns
        -------
        objects : list
            List of object names as strings.
        """
        keys = []
        for page in self.__get_client(access_key_id, secret_access_key).get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=prefix):
            contents = page["Contents"]
            # for obj in contents:
            #     keys.append(obj["Key"])
            if 'Contents' in page.keys():
                keys.extend(page['Contents'])
        return keys

    #####################################################################
    def get_s3_files(self):
        # gets a set of files
        pass

    #####################################################################
    def download_file(
        self,
        bucket_name,
        key,
        file_name,
        access_key_id=None,  # This should always be a bucket we have aws credentials for
        secret_access_key=None
    ):
        self.__get_client(
            access_key_id,
            secret_access_key
        ).download_file(Bucket=bucket_name, Key=key, Filename=file_name)

    #####################################################################
    def __chunked(
            ll: list,
            n: int
    ) -> Generator:
        """Yields successively n-sized chunks from ll.

        Parameters
        ----------
        ll : list
            List of all objects.
        n : int
            Chunk size to break larger list down from.

        Returns
        -------
        Batches : Generator
            Breaks the data into smaller chunks for processing
        """
        for i in range(0, len(ll), n):
            yield ll[i:i + n]

    #####################################################################
    def delete(
        self,
        bucket_name,
        key,
        access_key_id=None,
        secret_access_key=None
    ):
        self.__get_client(access_key_id, secret_access_key).delete_object(
            Bucket=bucket_name,
            Key=key,
        )

    #####################################################################
    def delete_children_files(  # was "delete_remote_objects"
        self,
        raw_zarr_files: list,
        output_bucket: str,
        access_key_id: str = None,
        secret_access_key: str = None,
    ):
        # deletes all given keys in s3 bucket
        objects_to_delete = []
        for raw_zarr_file in raw_zarr_files:
            objects_to_delete.append({'Key': raw_zarr_file['Key']})
        # Delete in groups of 100 — Boto3 constraint
        for batch in self.__chunked(objects_to_delete, 100):
            deleted = self.__get_client(access_key_id, secret_access_key).delete_objects(
                Bucket=output_bucket,
                Delete={
                    "Objects": batch
                }
            )
            print(f"Deleted {len(deleted['Deleted'])} files")

    #####################################################################
    def upload_file(
        self,
        file_name,
        bucket_name,
        key,
        access_key_id=None,
        secret_access_key=None
    ):
        self.__get_client(
            access_key_id,
            secret_access_key
        ).upload_file(file_name, bucket_name, key)
