import cloudsight,json

#Function to authenticate to access cloudsight API using ID and Key
def auth():
    auth = cloudsight.OAuth('ID', 'Key')
    api = cloudsight.API(auth)
    return api

#Function to print image data using cloudsight API
def get_data(title,n=1):
    api =auth()
    for i in xrange(1,n+1):
        name=str(title)+str(i)+'.jpg'
        with open(name, 'rb') as f:
            response = api.image_request(f,name,{'image_request[locale]': 'en-US',})
        status = api.image_response(response['token'])
        while status==cloudsight.STATUS_NOT_COMPLETED:
            status = api.wait(response['token'], timeout=30)
        print status['name']
