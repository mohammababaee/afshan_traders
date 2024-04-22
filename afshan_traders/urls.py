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

from consult.views import ConsultAPIView
from trades.views import (
    PortfolioAPIView,
    TradeAPIView,
    StockAPIView,
    FetchPortfolioData,
    FetchTradeData,
    FetchPortfolioInfo,
)
from users.views import LoginAPIView, SignupAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/trades/", TradeAPIView.as_view(), name="trades_api"),
    path("api/stocks/", StockAPIView.as_view(), name="stocks_api"),
    path("api/portfolio/", PortfolioAPIView.as_view(), name="portfolio_api"),
    path(
        "api/portfolio/id=<str:id>/", FetchPortfolioData.as_view(), name="portfolio_id"
    ),
    path("api/trades/id=<str:id>/", FetchTradeData.as_view(), name="trades_id"),
    path(
        "api/portfolio_info/id=<str:id>/",
        FetchPortfolioInfo.as_view(),
        name="portfolio_info",
    ),
    path(
        "api/portfolio_info/id=<str:id>/",
        FetchPortfolioInfo.as_view(),
        name="portfolio_info",
    ),
    path(
        "api/signup/",
        SignupAPIView.as_view(),
        name="signup",
    ),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("api/consult/", ConsultAPIView.as_view(), name="login"),
]
