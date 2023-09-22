from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger
from posts.models import Post, Like
from comments.models import Comment


def PostScore():
    post = Post.objects.filter(is_activate=True, is_private=False)
    for i in post:
        comment_count = Comment.objects.filter(post_id=i.id).count()
        like_count = Like.objects.filter(post_id=i.id).count()

        t = (timezone.now() - i.created_at).days * 24
        t += (int(timezone.now().hour) - int(i.created_at.hour))
        i.score = (i.views + like_count * 2 + comment_count * 3) // (t+2) ** 1.8
        print(t)
        i.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(PostScore, 'interval', hours=1, id='times_postscore')
    scheduler.start()

    if __name__ == '__main__':
        start()
