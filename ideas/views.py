from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import DevToolForm, IdeaForm
from .models import DevTool, Idea, IdeaStar

# 정렬 기준 (기능2)
SORT_OPTIONS = {
    "latest": ("최신순", "-created_at"),
    "oldest": ("등록순", "created_at"),
    "name": ("이름순", "title"),
    "popular": ("찜하기순", "-num_stars"),
    "interest": ("관심도순", "-interest"),
}


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _starred_ids(request):
    if request.user.is_authenticated:
        return set(
            IdeaStar.objects.filter(user=request.user).values_list("idea_id", flat=True)
        )
    return set()


def idea_list(request):
    sort = request.GET.get("sort", "latest")
    if sort not in SORT_OPTIONS:
        sort = "latest"
    query = request.GET.get("q", "").strip()

    ideas = Idea.objects.select_related("devtool").annotate(num_stars=Count("stars"))

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) | Q(devtool__name__icontains=query)
        ).distinct()

    ideas = ideas.order_by(SORT_OPTIONS[sort][1])

    paginator = Paginator(ideas, 4)  # 한 페이지 4개
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "sort": sort,
        "query": query,
        "sort_options": SORT_OPTIONS,
        "starred_ids": _starred_ids(request),
    }

    if _is_ajax(request):
        return render(request, "ideas/_idea_grid.html", context)
    return render(request, "ideas/idea_list.html", context)


def idea_detail(request, pk):
    idea = get_object_or_404(
        Idea.objects.select_related("devtool").annotate(num_stars=Count("stars")), pk=pk
    )
    return render(
        request,
        "ideas/idea_detail.html",
        {"idea": idea, "is_starred": idea.is_starred_by(request.user)},
    )


def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect(idea)
    else:
        form = IdeaForm()
    return render(request, "ideas/idea_form.html", {"form": form, "mode": "create"})


def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect(idea)
    else:
        form = IdeaForm(instance=idea)
    return render(
        request, "ideas/idea_form.html", {"form": form, "mode": "update", "idea": idea}
    )


@require_POST
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect("idea_list")


@require_POST
def toggle_star(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "login_required", "login_url": "/accounts/login/"}, status=401
        )
    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)
    if not created:
        star.delete()
        starred = False
    else:
        starred = True
    return JsonResponse({"starred": starred, "count": idea.stars.count()})


@require_POST
def change_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get("action")
    if action == "increase":
        idea.interest += 1
    elif action == "decrease":
        idea.interest -= 1
    idea.save(update_fields=["interest"])
    return JsonResponse({"interest": idea.interest})


def devtool_list(request):
    devtools = DevTool.objects.annotate(num_ideas=Count("ideas"))
    return render(request, "ideas/devtool_list.html", {"devtools": devtools})


def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = devtool.ideas.all()
    return render(
        request, "ideas/devtool_detail.html", {"devtool": devtool, "ideas": ideas}
    )


def devtool_create(request):
    if request.method == "POST":
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect(devtool)
    else:
        form = DevToolForm()
    return render(request, "ideas/devtool_form.html", {"form": form, "mode": "create"})


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == "POST":
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect(devtool)
    else:
        form = DevToolForm(instance=devtool)
    return render(
        request,
        "ideas/devtool_form.html",
        {"form": form, "mode": "update", "devtool": devtool},
    )


@require_POST
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect("devtool_list")