heroku login
git init
heroku git:remote -a led-land
git add .
git commit -am “first commit”
git push heroku master


https://medium.com/linedevth/%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87-line-chatbot-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2-python-84750b353fba

pip freeze > requirements.txt

heroku logs
heroku logs --tail



heroku config:set BOTPRESS_URL=https://led-land.herokuapp.com
heroku config:set EXTERNAL_URL=https://led-land.herokuapp.com
heroku config:set ASSET_URL=https://led-land.herokuapp.com