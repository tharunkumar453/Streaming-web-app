"""
URL configuration for payments project.
t views
    2. Add a URL to urlpatterns:  path(m  '', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLc   onf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from .views import planList,CreateOrder,VerifyPayment,razorpay_webhook 

urlpatterns = [
    path("plans/", planList.as_view(), name="plan-list"),
    path("create-order/<str:plan_id>", CreateOrder.as_view(), name="create-order"),
    path("verify-payment/", VerifyPayment.as_view(), name="verify-payment"),
    path("webhook/",razorpay_webhook, name="webhook"),
]

