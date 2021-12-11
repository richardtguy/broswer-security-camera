# Browser Security Camera

To serve application using the eventlet web server:
`python app.py`

## TODO:
- Separate user connections using rooms
- Save media files in separate folders per user
- Page to view user's own media files
- Email alert when motion detected (with link and thumbnail)
- Serve application using production web server

## To set up database on production server
`flask db upgrade`

## To create new user
`flask create_user`
