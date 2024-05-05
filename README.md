<h1 align="center"> Vendor Management System </h1>
<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<img alt="django" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img alt="django-rest-framework" src="https://img.shields.io/badge/Django_REST_Framework-092E20?style=for-the-badge&logo=django&logoColor=white">
<a href="https://god.gw.postman.com/run-collection/21642540-6f7d7afb-dc55-4b27-9b6b-6889be198efc?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21642540-6f7d7afb-dc55-4b27-9b6b-6889be198efc%26entityType%3Dcollection%26workspaceId%3D9ffaf628-1f4e-428b-b9ca-b884cd968d0a"><img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;"></a>
<img alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</p>


**API Documentation**: [bump.sh/akshaygdev/doc/vendor-management-system](https://bump.sh/akshaygdev/doc/vendor-management-system)  
**Source Code**: [github.com/akshay-g-dev/vendor-management-system](https://github.com/akshay-g-dev/vendor-management-system/)
**Run on Postman**: [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/21642540-6f7d7afb-dc55-4b27-9b6b-6889be198efc?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21642540-6f7d7afb-dc55-4b27-9b6b-6889be198efc%26entityType%3Dcollection%26workspaceId%3D9ffaf628-1f4e-428b-b9ca-b884cd968d0a)


---

<!--intro-start-->
Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.
To get started, jump to the [installation](#installation) section or keep reading to learn more about the included
features.
<!--intro-end-->


## ✨ Features
**Vendor Profile Management:**
   - Efficiently manage vendor profiles with features to create, update, retrieve, and delete vendor information.
   - Store comprehensive vendor details including their name, contact information, physical address, and a unique identifier code for easy reference and identification.

**Purchase Order Tracking:**
   - Seamlessly track purchase orders with detailed information such as purchase order number, vendor reference, order date, items included in the order, quantity, and current status of the order.
   - Keep a comprehensive record of all purchase orders, facilitating effective order management and tracking throughout the procurement process.

**Vendor Performance Evaluation:**
   - Evaluate vendor performance through key performance metrics such as On-Time Delivery Rate, Quality Rating, Response Time, and Fulfillment Rate.
   - Store and analyze vendor performance metrics within the system, providing insights into vendor reliability, product quality, responsiveness, and overall fulfillment capabilities.


### 📦️ Django Packages

* [Django 5](https://www.djangoproject.com/) - Latest version of Django
* [Django REST Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs


## Installation

### Requirements

* Python 3.10.0

### Setup

#### Clone the repository

``` bash
git clone https://github.com/akshay-g-dev/vendor-management-system.git
```
#### Install dependencies

``` bash
pip install -r requirements.txt
```

#### Make migrations

``` bash
python manage.py makemigrations
python manage.py migrate
```

#### Collect static files

``` bash
python manage.py collectstatic
```

#### Run the server

``` bash
python manage.py runserver
```

Access the server at `https://vendorms.pythonanywhere.com/`
