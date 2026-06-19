from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Count, Q, Avg
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from datetime import timedelta
from .models import Post, Like, SympathyVote, PainScore
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
from discussions.models import Topic
from users.models import CustomUser
from notifications.models import Notification


BELONGING_LABELS = dict(CustomUser.Belonging_CHOICES)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated:
        Notification.objects.filter(
            user=request.user,
            comment__post=post,
            read_at__isnull=True,
        ).update(read_at=timezone.now())
    return render(request, 'posts/post_detail.html', {'post': post})


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'new')
        qs = Post.objects.all()
        if sort == 'likes':
            qs = qs.annotate(like_count=models.Count('likes')).order_by('-like_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort', 'new')
        context['current_sort'] = sort
        if self.request.user.is_authenticated:
            liked_ids = set(Like.objects.filter(user=self.request.user).values_list('post_id', flat=True))
            context['liked_post_ids'] = liked_ids
        else:
            context['liked_post_ids'] = set()
        if sort == 'new':
            two_weeks_ago = timezone.now() - timedelta(weeks=2)
            trending = (
                Post.objects
                .annotate(recent_likes=Count('likes', filter=Q(likes__created_at__gte=two_weeks_ago)))
                .filter(recent_likes__gt=0)
                .order_by('-recent_likes', '-created_at')[:3]
            )
            context['trending_posts'] = list(trending)
            context['trending_ids'] = {p.pk for p in context['trending_posts']}
        else:
            context['trending_posts'] = []
            context['trending_ids'] = set()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('Posts:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).select_related('user')
        context['form'] = self.get_form()
        context['like_count'] = self.object.likes.count()
        context['user_liked'] = (
            self.request.user.is_authenticated and
            Like.objects.filter(user=self.request.user, post=self.object).exists()
        )
        sympathy_summary = _sympathy_summary(self.object)
        pain_summary = _pain_summary(self.object)
        context['sympathy_summary'] = sympathy_summary
        context['pain_summary'] = pain_summary

        top_topics = Topic.objects.filter(
            post=self.object
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count')[:3]

        for topic in top_topics:
            topic.latest_comment = Comment.objects.filter(
                topic=topic
            ).order_by('-created_at').first()

        context['top_topics'] = top_topics

        if self.request.user.is_authenticated:
            sv = SympathyVote.objects.filter(post=self.object, user=self.request.user).first()
            context['user_sympathy_vote'] = sv.vote_type if sv else None
            ps = PainScore.objects.filter(post=self.object, user=self.request.user).first()
            context['user_pain_score'] = ps.score if ps else None
            can_see_matrix = (
                self.request.user == self.object.user or
                _is_manager(self.request.user)
            )
            context['matrix'] = _matrix_data(sympathy_summary, pain_summary) if can_see_matrix else None
        else:
            context['user_sympathy_vote'] = None
            context['user_pain_score'] = None
            context['matrix'] = None
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('Posts:index')

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return redirect('Posts:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        if not self.request.FILES.get('image'):
            post.image = self.get_object().image
            post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Posts:detail', kwargs={'pk': self.object.pk})


MATRIX_SYMPATHY_THRESHOLD = 60
MATRIX_PAIN_THRESHOLD = 3.5
MATRIX_MIN_COUNT = 5


def _is_manager(user):
    return bool(user.role and 'マネージャー' in user.role)


def _matrix_data(sympathy_summary, pain_summary):
    if sympathy_summary['total'] < MATRIX_MIN_COUNT or pain_summary['total'] < MATRIX_MIN_COUNT:
        return None
    sympathy_rate = round(sympathy_summary['yes'] / sympathy_summary['total'] * 100, 1)
    pain_avg = pain_summary['avg']
    if sympathy_rate >= MATRIX_SYMPATHY_THRESHOLD and pain_avg >= MATRIX_PAIN_THRESHOLD:
        quadrant = 'immediate'
        label = '即推進'
        action = '課題も共感も高い。すぐに推進に移りましょう。'
    elif sympathy_rate >= MATRIX_SYMPATHY_THRESHOLD and pain_avg < MATRIX_PAIN_THRESHOLD:
        quadrant = 'refine_idea'
        label = 'アイデアを磨き直す'
        action = '共感は得られていますが、課題設定を見直すとさらに説得力が増します。'
    elif sympathy_rate < MATRIX_SYMPATHY_THRESHOLD and pain_avg >= MATRIX_PAIN_THRESHOLD:
        quadrant = 'rethink_solution'
        label = '解決策を練り直す'
        action = '課題は本物です。解決策のアプローチを変えることで支持が広がるかもしれません。'
    else:
        quadrant = 'hold'
        label = '保留 / 棄却'
        action = '課題感・共感ともに低め。いったん保留か棄却を検討してください。'
    return {
        'sympathy_rate': sympathy_rate,
        'pain_avg': pain_avg,
        'quadrant': quadrant,
        'label': label,
        'action': action,
        'x_pct': round(pain_avg / 5 * 100, 1),
        'y_pct': sympathy_rate,
    }


def _sympathy_summary(post):
    votes = SympathyVote.objects.filter(post=post)
    total = votes.count()
    yes = votes.filter(vote_type='yes').count()
    maybe = votes.filter(vote_type='maybe').count()
    no = votes.filter(vote_type='no').count()
    dept_raw = {}
    for v in votes.values('department', 'vote_type'):
        d = v['department'] or '未設定'
        dept_raw.setdefault(d, {'yes': 0, 'maybe': 0, 'no': 0})
        dept_raw[d][v['vote_type']] += 1
    dept_breakdown = {}
    for d, v in dept_raw.items():
        if sum(v.values()) >= 3:
            label = BELONGING_LABELS.get(d, d)
            dept_breakdown[label] = v
    return {'total': total, 'yes': yes, 'maybe': maybe, 'no': no, 'dept_breakdown': dept_breakdown}


def _pain_summary(post):
    scores = PainScore.objects.filter(post=post)
    total = scores.count()
    if total == 0:
        return {'total': 0, 'avg': None, 'high_rate': None, 'dept_breakdown': {}}
    avg = round(scores.aggregate(Avg('score'))['score__avg'], 1)
    high = scores.filter(score__gte=4).count()
    high_rate = round(high / total * 100)
    dept_raw = {}
    for s in scores.values('department', 'score'):
        d = s['department'] or '未設定'
        dept_raw.setdefault(d, [])
        dept_raw[d].append(s['score'])
    dept_breakdown = {}
    for d, sc_list in dept_raw.items():
        if len(sc_list) >= 3:
            label = BELONGING_LABELS.get(d, d)
            dept_breakdown[label] = round(sum(sc_list) / len(sc_list), 1)
    return {'total': total, 'avg': avg, 'high_rate': high_rate, 'dept_breakdown': dept_breakdown}


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        return JsonResponse({'error': 'forbidden'}, status=403)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})


@login_required
@require_POST
def submit_sympathy_vote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        return JsonResponse({'error': 'forbidden'}, status=403)
    vote_type = request.POST.get('vote_type')
    if vote_type not in ('yes', 'maybe', 'no'):
        return JsonResponse({'error': 'invalid'}, status=400)
    dept = request.user.belonging or '未設定'
    SympathyVote.objects.update_or_create(
        post=post, user=request.user,
        defaults={'vote_type': vote_type, 'department': dept}
    )
    return JsonResponse({'ok': True, 'summary': _sympathy_summary(post)})


@login_required
@require_POST
def submit_pain_score(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        return JsonResponse({'error': 'forbidden'}, status=403)
    try:
        score = int(request.POST.get('score', 0))
    except ValueError:
        return JsonResponse({'error': 'invalid'}, status=400)
    if score < 1 or score > 5:
        return JsonResponse({'error': 'invalid'}, status=400)
    dept = request.user.belonging or '未設定'
    PainScore.objects.update_or_create(
        post=post, user=request.user,
        defaults={'score': score, 'department': dept}
    )
    return JsonResponse({'ok': True, 'summary': _pain_summary(post)})