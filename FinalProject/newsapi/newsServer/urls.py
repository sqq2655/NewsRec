'''newsServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
'''
from django.contrib import admin
from django.urls import path

from newsServer.models.news import all_news, del_news, reconewsbytags, typenews, reconewsbysimilar, getpicture, \
    getNewsDetailByNewsid, all_news_to_page, newsHistory, getComments, gethotnews, updateGiveLike, \
    submitComments, \
    submitCommenttoUser, getManageHomeData, updateRecHis, searchNews

from newsServer.models.user import add_user, all_user, del_user, up_user, user_login, user_register, getHistory, \
    getRecNes, \
    getUserDetail, up_user_by_user, up_tags, getMessage, getTip, setMessageHadRead, getHotwordData, tourists_login, \
    setUserHeadPic, \
    getall_comments, del_comments, searchUser, searchComments

from newsServer.models.spider import beginUrlSpider, beginDetailSpider, closeSpiderThread, getSpiderPageData


from newsServer.models.recommends import beginRecommend, closeRecommendThread, beginAnalysis, getRecommendPageData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', all_news),
    path('news/search/', searchNews),
    path('user/allcomments/', getall_comments),#用户管理
    path('user/add/', add_user),
    path('user/all/', all_user),
    path('user/search/', searchUser),
    path('comments/search/', searchComments),
    path('user/del/', del_user),
    path('user/delcomment/', del_comments),
    path('user/up/', up_user),
    path('user/login/', user_login),
    path('user/tourists/', tourists_login),
    path('news/del/', del_news),
    path('news/recbt/', reconewsbytags),
    path('news/typ/', typenews),
    path('news/recbs/', reconewsbysimilar),  # 详细新闻下相似新闻轮播(左边通过相似度推荐)
    # path('news/nhr/', newsHotRec),  # 详细新闻下热点新闻轮播（哪个不空展示哪个）
    path('user/regis/', user_register),
    path('news/pict/', getpicture),  # 轮播图
    path('news/id/', getNewsDetailByNewsid),  # 通过id获取详细新闻
    path('news/all/', all_news_to_page),  # 首页新闻列表
    path('news/his/', newsHistory),
    path('news/updateRec/', updateRecHis),
    path('user/his/', getHistory),
    path('user/rec/', getRecNes),  # 获取为你推荐
    path('news/com/', getComments),
    path('user/det/', getUserDetail),#用户中心
    path('user/upb/', up_user_by_user),
    path('user/getHotwordData/', getHotwordData),#获取热词库用于词云展示
    path('user/uptags/', up_tags),
    path('news/hotnews/', gethotnews),  # 按照新闻热度获取50条展示（时事热点）
    path('news/updgivelike/', updateGiveLike),  # 更新点赞
    path('news/subcom/', submitComments),
    path('news/subcomtou/', submitCommenttoUser),
    path('user/message/', getMessage),
    path('user/gettip/', getTip),
    path('user/sethadread/', setMessageHadRead),
    path('user/updateheadpic/', setUserHeadPic),
    path('management/homedata/', getManageHomeData),
    path('spider/urlbegin/', beginUrlSpider),
    path('spider/detailbegin/', beginDetailSpider),
    path('spider/closeserve/', closeSpiderThread),
    path('spider/getspiderdata/', getSpiderPageData),
    path('recommend/getrecommenddata/', getRecommendPageData),
    path('recommend/startrecommend/', beginRecommend),
    path('recommend/startanalysis/', beginAnalysis),
    path('recommend/stopsystem/', closeRecommendThread),
    # path('download/logs/', download),
]
