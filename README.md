**About this project**

The current project was developed as part of a challenge to apply to a position at ZEBRANDS. The challenge focus on developing an app that works as a catalogue for different products. In this app, we could have anonymous users and staff. Anonymous users could only see products, while staff users could edit or delete them, as well as editing or deleting other users and staff. Finally, whenever some of this changes were made, all staff should be notified by email.

**How it works**

This app works based on Django infraestructure. Basically, in each app we have a file named "view", which contains the functions that process HTTP requests and generate a response. The file named "urls" contains the links that users need to access the views. So, when a HTTP request is made, Django searchs for an URL that matches the request in the urls.py file. Once it finds it, it calls the view defined in the views.py file.

Also, running on a local enviroment, we are able to create a database with sqlite3 and interact with it through ORM. Django creates the tables based on the defined models in our apps, and each time a query is executed through ORM, Django translates it into an SQL query and  make the changes in our database.

We have defined two apps within our project, "productos" and "usuarios". The first one, with all code related to our products views, such as products list and views for editing, adding and deleting them. On the second one, we developed the code related to the users applications, such as login, logout, signup, staff definition and all actions on users such as editing, delete or adding them. 

In **users** app, this are the **views**:
- home: It is the main view displayed when entering the site. If the user is authenticated and is a staff member, the template users/index.html is rendered, otherwise the template users/index.html is rendered.

- signup: It is the view that is responsible for registering new users. If the request method is POST, the information provided by the user is validated and a new user instance is created. Then, the user is redirected to the home page. If the request method is GET, the template users/signup.html is rendered.

- signin: It is the view that is responsible for authenticating existing users. If the request method is POST, it is verified whether the user provided valid credentials. If the credentials are valid, the user is authenticated and redirected to the home page, otherwise the user is redirected to the login page (signin). If the request method is GET, the template users/signin.html is rendered.

- signout: It is the view that is responsible for logging out an authenticated user. Once the session is closed, the user is redirected to the home page.

- list_users: It is the view that is responsible for displaying a list of all users registered in the system. Only authenticated users can access this view. The template users/users_list.html is rendered.

- mod_user: It is the view that is responsible for modifying the information of an existing user. If the request method is POST, the user information is updated and the user is redirected to the list of users (list_users). If the request method is GET, the template users/mod_users.html is rendered.

- del_user: It is the view that is responsible for deleting an existing user. If the user exists, it is deleted and the user is redirected to the list of users (list_users). If the user does not exist, a 404 response is returned.

- create_users: It is the view that is responsible for creating a new user. If the request method is POST, the information provided by the user is validated and a new user instance is created. Then, the user is redirected to the list of users (list_users). If the request method is GET, the template users/create_user.html is rendered.

- enviar_correo_a_administradores: It is the view that is responsible for sending an email to the system administrators to notify them of the modification of an existing user. Currently, this view is not working due to an authentication error.

In **products** app, this are the **views**:
- tienda(request): This view retrieves all products from the database and returns them to the template productos/tienda.html, along with a query string parameter q.

- detalle_producto(request, sku): This view retrieves a single product with a given SKU and updates its click count before rendering the template productos/detalle_producto.html with the product's data.

- list_products(request): This view retrieves all products from the database and returns them to the template productos/prod_list.html.

- mod_products(request, prod_sku): This view retrieves a product with a given SKU and updates its attributes with data received from a form submission via POST request. It then saves the updated product and redirects to the list_products view on success. If the request method is not POST, it renders the productos/mod_products.html template with the product's data.

- del_products(request, prod_sku): This view retrieves a product with a given SKU and deletes it from the database. It then redirects to the list_products view on success or returns an error message if the product was not found.

- create_products(request): This view receives form data via POST request and creates a new product object with the data, saving it to the database. It then redirects to the list_products view on success, or renders the productos/create_products.html template if the request method is not POST.

- error_handler(request, exception=None): This view renders the error.html template with a message to prompt the user to sign in.

**How to deploy this app in your local enviroment**

To test this app in your PC, you should follow this steps:

Windows:
- Clone git repository locally
- Activate virtual enviroment with command venv\Scripts\activate
- Install dependencies of the proyect, pointed on requirement.txt file. You could use the following command:
pip install -r requirement.txt
- Set the databases (may be needed). Use the following command:
python manage.py migrate
- Start local Django server:
python manage.py runserver

MAC OS:
- Clone git repository locally
- Activate virtual enviroment with command
source venv/bin/activate
- Install dependencies of the proyect, pointed on requirement.txt file. You could use the following command:
pip install -r requirement.txt
- Set the databases (may be needed). Use the following command:
python manage.py migrate
- Start local Django server:
python manage.py runserver

You should now be able to see the app at http://localhost:8000

**Activate notification email functionality**

For security purposes, I'm not able to upload the api key in the final/settings.py file, so the function to send the notification to all admins has been commented (#). To activate it, you must have a user on SendGrid, create an API key and change the parameter EMAIL_HOST_PASSWORD in the settings.py file with your api key. Then remove the "#" sign before each call to enviar_correo_a_administradores() function.

