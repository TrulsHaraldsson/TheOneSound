import webapp2
import os
from python.lib import cloudstorage as gcs
from google.appengine.api import app_identity
from python.api.exceptions import NotAuthorized, BadRequest
from python.util import loginhelper


class StorageHandler(webapp2.RequestHandler):
    def post(self):
        """
        Adds a picture to the google cloud bucket and link it to an entity with the given id.
        :param image: The image.
        :param type: The image format.
        :param id: Id of the entity this picture belongs to. Can be an band-, album- or track-id.
        """
        try:
            loginhelper.check_logged_in()
            post_params = self.request.POST
            image = post_params['image']
            type_ = post_params['type']
            id_ = post_params['id']
            if image == "" or type_ == "" or image == "":
                raise BadRequest("all parameters are needed.")
            bucket_name = os.environ.get('BUCKET_NAME',
                                         app_identity.get_default_gcs_bucket_name())
            filename = '/'+bucket_name+'/'+type_+'/'+id_
            self.write_data_to_file(filename, image)
        except NotAuthorized:
            self.response.set_status(401)
        except BadRequest:
            self.response.set_status(400)
        except Exception:
            self.response.set_status(400)

    def write_data_to_file(self, filename, image):
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type='image/png',
                            retry_params=write_retry_params)

        gcs_file.write(image.file.read())
        gcs_file.close()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/storage', StorageHandler),
], debug=True)
# [END app]
