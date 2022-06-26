from lang_api import app, api, add_resources

if __name__ == '__main__':
    add_resources(api)
    
    app.run(host="localhost", port=3001, debug=True)
