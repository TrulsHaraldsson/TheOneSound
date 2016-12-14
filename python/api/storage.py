import webapp2
import os
from python.lib import cloudstorage as gcs
from google.appengine.api import app_identity


class StorageHandler(webapp2.RequestHandler):
    def post(self):
        post_params = self.request.POST
        image = post_params['image']
        type_ = post_params['type']
        id_ = post_params['id']
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        filename = '/'+bucket_name+'/'+type_+'/'+id_
        self.write_data_to_file(filename, image)
        # band = common.get_entity_by_id(Band, id_)
        # band.description.picture_url = "https://storage.googleapis.com/theonesound-148310.appspot.com" + filename
        # self.response.out.write(json.dumps())

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        print("Bucket name = ", bucket_name)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: '
                            + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')
        bucket = '/'+bucket_name
        self.write(bucket + '/foo')
        self.list_bucket(bucket)

    def write_data_to_file(self, filename, image):
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type='image/png',
                            # options={'x-goog-meta-foo': 'foo',
                            #          'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)

        gcs_file.write(image.file.read())
        gcs_file.close()
        stat = gcs.stat(filename)


# [START app]
app = webapp2.WSGIApplication([
    ('/api/storage', StorageHandler),
], debug=True)
# [END app]