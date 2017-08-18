import json
try:
    import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
    class analyze_image():
        def __init__(self, API_KEY, IMAGE_URL):
            self.api_key = API_KEY
            self.image_url = IMAGE_URL
            self.get_analyzed_data()

        def get_analyzed_data(self):
            headers = {
                # Request headers. Replace the placeholder key below with your subscription key.
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            body = ""

            # load image

            #filename = 'D:/9_Github/3_Github Samples/2_Scraping/microsoft-emotion-recognition/chris_young.jpg'
            filename = self.image_url

            f = open(filename, "rb")

            body = f.read()

            f.close()

            params = urllib.parse.urlencode({
            })

            # Replace the example URL below with the URL of the image you want to analyze.
            #body = "{ 'url': '" + self.image_url + "' }"

            try:
                # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
                #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
                #   URL below with "westcentralus".
                conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
                conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
                response = conn.getresponse().read()
                self.data = json.loads(response)[0]
                print(self.data)
                conn.close()
            except Exception as e:
                print(e.args)

except:
    import httplib, urllib, base64

    class analyze_image():
        def __init__(self, API_KEY, IMAGE_URL):
            self.api_key = API_KEY
            self.image_url = IMAGE_URL

            self.get_analyzed_data()

        def get_analyzed_data(self):
            headers = {
                # Request headers. Replace the placeholder key below with your subscription key.
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            params = urllib.parse.urlencode({
            })

            # Replace the example URL below with the URL of the image you want to analyze.
            body = "{ 'url': '" + self.image_url + "' }"

            try:
                # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
                #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
                #   URL below with "westcentralus".
                conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
                conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
                response = conn.getresponse().read()
                self.data = json.loads(response)[0]
                print(self.data)
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))



if __name__ == '__main__':
    API_KEY = '1b897276f50843f78412b3185b80afcd'
    IMAGE_URL = 'https://jbf-media.s3.amazonaws.com/production/event/2016/10/3/del_coro_ben1.jpg'
    app = analyze_image(API_KEY, IMAGE_URL)

