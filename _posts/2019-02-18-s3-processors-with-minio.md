---
title: Using the S3 Processors with Minio
---

Minio is a small S3-compatible server that can be really useful for internal use. To set it up with NiFi, download it an run it with this command:

```
./minio server ./minio_data
```

It will then print out some information that looks like this:

```
Endpoint:  http://192.168.1.151:9000  http://127.0.0.1:9000            
AccessKey: <ACCESS_KEY_HERE> 
SecretKey: <SECRET_KEY_HERE>

Browser Access:
   http://192.168.1.151:9000  http://127.0.0.1:9000            

```

At that point, you can connect with your browser and create a bucket.

![New Bucket](/post_assets/2019-02-18-s3-processors-with-minio/minio_new_bucket.png)

Now all you have to do is drag one or more S3 processors onto the NiFi canvas and configure them with the bucket name, secret key, access key and then set the "Endpoint Override URL" to the Endpoint value that is printed out in the console.

![PutS3 Configuration](/post_assets/2019-02-18-s3-processors-with-minio/puts3.png)