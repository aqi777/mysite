from django.shortcuts import render
from django .contrib.contenttypes.models import ContentType
from read_statistics.utils import get_week_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from django.core.cache import cache
from django.db.models import Sum
import datetime
from django.utils import timezone

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter\
        (read_details__date__lt=today,read_details__date__gte=date)\
        .values('id','title').\
        annotate(read_num_sum = Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]




def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_week_read_data(blog_content_type)

# 获取缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_7_days_hot_blogs()
        cache.set('week_hot_data', week_hot_data, 3600)



    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['week_hot_data'] = week_hot_data
    return render(request,'home.html',context)


