from django.db import models
from app.models.blog.article import BlogArticle
from app.models.blog.image import Image


class HomeRecommend(models.Model):

    share_id = models.IntegerField()
    reco_cover = models.IntegerField()
    reco_intro = models.CharField()
    weight = models.IntegerField()
    operator_id = models.IntegerField()
    status = models.IntegerField()
    created_time = models.CharField()
    updated_time = models.CharField()

    @staticmethod
    def query_recommend_list(page=0, per_page=10):
        recom_list = HomeRecommend.objects.filter(status=1).order_by("-weight")[page: per_page]
        result = []
        for recommend in recom_list:
            result.append(HomeRecommend.format_recommend(recommend))
        return result

    @staticmethod
    def query_recommend_by_share_id(share_id=0):
        try:
            recom = HomeRecommend.objects.get(share_id=share_id)
            return HomeRecommend.format_recommend(recom, False)
        except:
            return None

    @staticmethod
    def format_recommend(recommend, full_info=True):
        result = dict()
        result["id"] = recommend.id
        result["reco_into"] = recommend.reco_intro
        result["cover"] = Image.query_image_by_id(recommend.reco_cover)

        if full_info:
            article = BlogArticle.query_article_by_id(recommend.share_id)
            del article["content"]
            result["article_info"] = article

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "home_recommend"