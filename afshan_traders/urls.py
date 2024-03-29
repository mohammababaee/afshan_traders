"""
URL configuration for afshan_traders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from trades.views import PortfolioAPIView, TradesAPIView, StockAPIView, FetchPortfolioData, FetchTradeData,FetchPortfolioInfo

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/trades/', TradesAPIView.as_view(), name='trades_api'),
    path('api/stocks/', StockAPIView.as_view(), name='stocks_api'),
    path('api/portfolio/', PortfolioAPIView.as_view(), name='portfolio_api'),
    path('api/portfolio/id=<str:id>/', FetchPortfolioData.as_view(), name='portfolio_id'),
    path('api/trades/id=<str:id>/', FetchTradeData.as_view(), name='trades_id'),
    path('api/portfolio_info/id=<str:id>/', FetchPortfolioInfo.as_view(), name='portfolio_info'),
    ]
