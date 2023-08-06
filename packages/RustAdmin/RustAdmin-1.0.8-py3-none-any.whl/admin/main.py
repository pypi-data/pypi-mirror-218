import sys
import os

def create_project(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir)

    app_dir = os.path.join(project_dir, "app")
    os.makedirs(app_dir)

    errors_dir = os.path.join(app_dir, "errors")
    os.makedirs(errors_dir)

    templates_dir = os.path.join(app_dir, "views")
    os.makedirs(templates_dir)

    public_dir = os.path.join(app_dir, "public")
    os.makedirs(public_dir)

    with open(os.path.join(project_dir, "manage.py"), "w") as f:
        f.write(''' # Add your manage code here:
# Example usage

from app.app import app

@app.route("/", methods=['GET'], secure=False)
async def home(request):
    return Response("welcome to VeloWeb") ''')

    with open(os.path.join(app_dir, "wsgi.py"), "w") as f:
        f.write('''from app import app


if __name__ == "__main__":
    app.run() ''')

    with open(os.path.join(app_dir, "app.py"), "w") as f:
        f.write('''from Ruster import Rust, render_template, Response
app = Rust()

@app.route("/", methods=["GET", "POST"], secure=False)
async def home(request):
    return render_template("index.html")
''')

    with open(os.path.join(app_dir, "settings.py"), "w") as f:
        f.write(''' # settings.py config

HOST = "127.0.0.1"  # default host by rustWEB on localhost
PORT = 8000 # default port by rustWEB on 8000
DEBUG = True # default debug value True for development

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0'] # You can add more hosts as per your requirements

# Ruster provides a inbuild database engine @nexus, NexusDB developed by @PyDev using Json/Application.
# @nexus is a fully manage and structured database and also compatible for production usage with,
# app.config['SET_APP_MODE'] = "Production"
# db.set_app(app.config['SET_APP_MODE'])

# Default configuration for @nexus 

DATABASES = {
        'default': {
            'ENGINE': 'rust.db.backends.nexus', # default database engine Nexus
            'NAME': 'YOUR_DB_NAME',
            'USER': 'USERNAME',
            'PASSWORD': 'PASSWORD_FOR_DB',
            'HOST': 'localhost'
        }
    }

MEDIA_URL = '/media/'
STATIC_URL = '/public/'
TEMPLATE_ENGINE = '/templates'
        ''')

    with open(os.path.join(app_dir, "__init__.py"), "w") as f:
        pass

    with open(os.path.join(app_dir, ".env"), "w") as f:
        f.write(''' SECRET_KEY = "your_secret_key" ''')

    with open(os.path.join(app_dir, "rust.json"), "w") as f:
        f.write(f'''{{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "Description of your project",
    "author": "Your Name",
    "email": "your@email.com",
    "app": {{
        "name": "Your App Name",
        "description": "Description of your app",
        "server": [
        {{ 
            "server": "alice conf.app.py",
            "server:prod": "bind 127.0.0.0:8000 *conf",
            "server:static": "ruster @admin.commit *server static()",
            "server:daemon": "**config(daemon) --lts"
        }}
        ],
        "routes": [
        {{
            "url": "/",
            "methods": ["GET", "POST"],
            "secure": true,
            "handler": "app.home"
        }}
        ],
        "dependencies": [
        {{
            "RusterAdmin": "2.0.2 -2.0988 byte",
            "Ruster": "2.0.1 -36910 byte",
            "Ruster.hasher": "1.1.2 -36445 byte",
            "Ruster.session": "1.1.1 -35446 byte",
            "Ruster.jwt": "1.1.5 -78263 byte",
            "Ruster.blueprint": "1.1.0 -89366 byte",
            "Ruster.sanitizer": "1.1.0 -102235 byte",
            "Ruster.wtf": "1.1.0 -988765 byte",
            "nexusdb": "2.2.6 -500983349 byte" 
        }}
        ]
    }}
    }}''')

    with open(os.path.join(templates_dir, "index.html"), "w") as f:
        f.write(''' <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ruster Documentation</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.7/dist/tailwind.min.css" rel="stylesheet">
  <style>
    /* Custom CSS styles for the documentation page */
    /* Add your custom styles here */
  </style>
</head>
<body class="bg-gray-100">
  <header class="bg-indigo-600 text-white py-4">
    <div class="container mx-auto px-4">
      <h1 class="text-2xl font-bold">Ruster Documentation</h1> <br><p>For more documantation visit <a href="http://ruster.vvfin.in/docs"> Ruster </a>
    </div>
  </header>

  <main class="container mx-auto px-4 py-8">
    <section class="mb-8">
      <h2 class="text-2xl font-bold mb-4">Introduction</h2>
      <p>
        Ruster is a Python web framework that provides a simple and efficient way to build web applications.
        It leverages the power of Rust to ensure high performance and reliability.
      </p>
    </section>

    <section class="mb-8">
      <h2 class="text-2xl font-bold mb-4">Getting Started</h2>
      <p>
        To get started with Ruster, you need to install it using pip:
      </p>
      <pre class="bg-gray-800 text-white rounded p-4 mt-4"><code>pip install ruster</code></pre>
    </section>

    <section class="mb-8">
      <h2 class="text-2xl font-bold mb-4">Example Code</h2>
      <p>
        Here are a few example code snippets that demonstrate the usage of Ruster:
      </p>

      <h3 class="text-xl font-bold mt-6">Routing</h3>
      <p>
        Define routes and their corresponding handler functions:
      </p>
      <pre class="bg-gray-800 text-white rounded p-4 mt-4"><code>from Ruster import Rust, render_template

app = Rust()

@app.route("/", methods=["GET"])
async def home(request):
    return "Welcome to the homepage"

@app.route("/about", methods=["GET"])
async def about(request):
    return "This is the about page"

if __name__ == "__main__":
    app.run()</code></pre>

      <h3 class="text-xl font-bold mt-6">Templates</h3>
      <p>
        Render HTML templates using the <code>render_template</code> function:
      </p>
      <pre class="bg-gray-800 text-white rounded p-4 mt-4"><code>from Ruster import Rust, render_template

app = Rust()

@app.route("/", methods=["GET"])
async def home(request):
    return render_template("index.html", name="John")

if __name__ == "__main__":
    app.run()</code></pre>

      <h3 class="text-xl font-bold mt-6">Form Handling</h3>
      <p>
        Handle form submissions with the <code>POST</code> method:
      </p>
      <pre class="bg-gray-800 text-white rounded p-4 mt-4"><code>from Ruster import Rust, render_template

app = Rust()

@app.route("/signup", methods=["GET", "POST"])
async def signup(request):
    if request.method == "POST":
        # Process form data
        name = request.form.get("name")
        email = request.form.get("email")
        # Save data to the database
        # ...
        return "Thanks for signing up!"
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    app.run()</code></pre>
    </section>
  </main>

  <footer class="bg-gray-900 text-white py-4">
    <div class="container mx-auto px-4 text-center">
      &copy; 2023 Ruster. All rights reserved.
    </div>
  </footer>

  <script src="https://cdn.tailwindcss.com/"></script>
  <script>
    // Add your custom JavaScript here
  </script>
</body>
</html>


''')
        
    with open(os.path.join(errors_dir, "400.html"), "w") as f:
      f.write('''<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Your request was invalid.</p>
</body>
</html>

      ''')

      with open(os.path.join(errors_dir, "401.html"), "w") as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>401</title>
  <style>
    .error-card {
  margin: 50px 0 0 50px;
}

.error-card .error-card-icon {
  width: 100px;
  border-radius: 8px 0 0 8px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #eee;
}

.error-card .error-card-content {
  width: 400px;
  border-radius: 0 8px 8px 0;
  border: 1px solid #ddd;
  padding: 10px 20px;
}

  </style>
</head>
<body>
  <div class="error-card d-flex flex-row">
    <div class="error-card-icon">
      <h4 class="display-4"><i class="bi bi-x-octagon-fill text-danger"></i></h4>
    </div>
    <div class="error-card-content">
      <h2>Error 401</h2>
      <p>You are not authrorized to view this page</p>
    </div>
  </div>
</body>
</html>
        ''')

      with open(os.path.join(errors_dir, "404.html"), "w") as f:
        f.write(''' <html>
<head>
    <title>404 Not Found</title>
</head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Arvo">
<style>
    
/*======================
    404 page
=======================*/


.page_404{ padding:40px 0; background:#fff; font-family: 'Arvo', serif;
}

.page_404  img{ width:100%;}

.four_zero_four_bg{
 
 background-image: url(https://cdn.dribbble.com/users/285475/screenshots/2083086/dribbble_1.gif);
    height: 400px;
    background-position: center;
 }
 
 
 .four_zero_four_bg h1{
 font-size:80px;
 }
 
  .four_zero_four_bg h3{
			 font-size:80px;
			 }
			 
			 .link_404{			 
	color: #fff!important;
    padding: 10px 20px;
    background: #39ac31;
    margin: 20px 0;
    display: inline-block;}
	.contant_box_404{ margin-top:-50px;}
</style>
<body>
    <section class="page_404">
        <div class="container">
            <div class="row">	
            <div class="col-sm-12 ">
            <div class="col-sm-10 col-sm-offset-1  text-center">
            <div class="four_zero_four_bg">
                <h1 class="text-center ">404</h1>
            
            
            </div>
            
            <div class="contant_box_404">
            <h3 class="h2">
            Look like you're lost
            </h3>
            
            <p>the page you are looking for not avaible!</p>
            
        </div>
            </div>
            </div>
            </div>
        </div>
    </section>
</body>
</html>

      ''')

    with open(os.path.join(errors_dir, "403.html"), "w") as f:
      f.write(''' <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403</title>
</head>
<style>
    @import url("https://fonts.googleapis.com/css?family=Montserrat:400,400i,700");
/* sorry for the scrambled mess */
 body {
	 display: flex;
	 align-items: center;
	 justify-content: center;
	 height: 100vh;
	 width: 100vw;
	 background: #eceff1;
	 font-family: Montserrat, sans-serif;
}
 .container {
	 background: white;
	 height: auto;
	 width: 40vw;
	 padding: 1.5rem;
	 box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.2);
	 border-radius: 0.5rem;
	 text-align: center;
}
 .container h1 {
	 font-size: 1.25rem;
	 margin: 0;
	 margin-top: 1rem;
	 color: #263238;
	 opacity: 0;
	 transform: translateX(-0.1rem);
	 animation: fadeIn 1s forwards 1.5s;
}
 .container p {
	 margin: 0;
	 margin-top: 0.5rem;
	 color: #546e7a;
	 opacity: 0;
	 transform: translateX(-0.1rem);
	 animation: fadeIn 1s forwards 1.75s;
}
 @media screen and (max-width: 768px) {
	 .container {
		 width: 50vw;
	}
}
 @media screen and (max-width: 600px) {
	 .container {
		 width: 60vw;
	}
}
 @media screen and (max-width: 500px) {
	 .container {
		 width: 80vw;
	}
}
 @keyframes fadeIn {
	 from {
		 transform: translateY(1rem);
		 opacity: 0;
	}
	 to {
		 transform: translateY(0rem);
		 opacity: 1;
	}
}
 .forbidden-sign {
	 margin: auto;
	 width: 4.6666666667rem;
	 height: 4.6666666667rem;
	 border-radius: 50%;
	 display: flex;
	 align-items: center;
	 justify-content: center;
	 background-color: #ef5350;
	 animation: grow 1s forwards;
}
 @keyframes grow {
	 from {
		 transform: scale(1);
	}
	 to {
		 transform: scale(1);
	}
}
 .forbidden-sign::before {
	 position: absolute;
	 background-color: white;
	 border-radius: 50%;
	 content: "";
	 width: 4rem;
	 height: 4rem;
	 transform: scale(0);
	 animation: grow2 0.5s forwards 0.5s;
}
 @keyframes grow2 {
	 from {
		 transform: scale(0);
	}
	 to {
		 transform: scale(1);
	}
}
/* slash */
 .forbidden-sign::after {
	 content: "";
	 z-index: 2;
	 position: absolute;
	 width: 4rem;
	 height: 0.3333333333rem;
	 transform: scaley(0) rotateZ(0deg);
	 background: #ef5350;
	 animation: grow3 0.5s forwards 1s;
}
 @keyframes grow3 {
	 from {
		 transform: scaley(0) rotateZ(0deg);
	}
	 to {
		 transform: scaley(1) rotateZ(-45deg);
	}
}
 
</style>
<body>
    <div class="container">
        <div class="forbidden-sign"></div>
        <h1><b>403</b></h1>
        <h1>Access to this page is restricted.</h1>
        <p>Ensure you have sufficient permissions to access the same.</p>
    </div>
</body>
</html>''')
      
    with open(os.path.join(errors_dir, "405.html"), "w") as f:
      f.write(''' <html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<style>
    * {
	font-family: Verdana;
	text-align:center;
}

h1 {
	font-size:4em;
}

</style>
<body>
    <br><br><br><br>
<br><h1>Error 405</h1><h2>Method not allowed.</h2>
    <p>The requested method is not allowed for this URL.</p>
</body>
</html>
''')

      js_dir = os.path.join(public_dir, "js")
      os.makedirs(js_dir)

      css_dir = os.path.join(public_dir, "css")
      os.makedirs(css_dir)


def runserver_prod(project_name):
    app_path = os.path.join(project_name, "app")
    wsgi_path = os.path.join(app_path, "wsgi.py")
    if os.path.exists(wsgi_path):
        os.system(f"python {wsgi_path}")
    else:
        print("Error: wsgi.py file not found in the app folder.")

def main():
    if len(sys.argv) < 3:
        print("Invalid command")
        return

    command = sys.argv[1]

    if command == "runserver" and sys.argv[2] == "prod":
        if len(sys.argv) < 4:
            print("Invalid command")
            return
        project_name = sys.argv[3]
        runserver_prod(project_name)
    elif command == "startproject":
        if len(sys.argv) < 3:
            print("Invalid command")
            return
        project_name = sys.argv[2]
        create_project(project_name)
        print(f"Project '{project_name}' created successfully!")
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()

