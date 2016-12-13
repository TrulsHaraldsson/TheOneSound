import webapp2;

import os
from python.lib import cloudstorage as gcs
from google.appengine.api import app_identity


class StorageHandler(webapp2.RequestHandler):
    def post(self):

        post_params = self.request.POST
        data = post_params['data']
        type_ = post_params['type']
        id_ = post_params['id']
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        filename = '/'+bucket_name+'/'+type_+'/'+id_
        self.write_data_to_file(filename, data)

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        print("Bucket name = ", bucket_name)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: '
                            + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')
        bucket = '/'+bucket_name;
        self.write(bucket + '/foo')
        self.list_bucket(bucket)

    def write_data_to_file(self, filename, data):
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type='text/plain',
                            options={'x-goog-meta-foo': 'foo',
                                     'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.write(data)
        gcs_file.close()

    def write(self, filename):
        self.response.write('Creating file %s\n' % filename)
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type='text/plain',
                            options={'x-goog-meta-foo': 'foo',
                                     'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.write('abcde\n')
        gcs_file.write('f'*1024*4 + '\n')
        gcs_file.close()

    def list_bucket(self, bucket):
        self.response.write("Listing files \n")
        page_size = 1
        stats = gcs.listbucket(bucket, max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')

            if count != page_size or count == 0:
                break
            stats = gcs.listbucket(bucket, max_keys=page_size,
                                   marker=stat.filename)

# [START app]
app = webapp2.WSGIApplication([
    ('/api/storage', StorageHandler),
], debug=True)
# [END app]