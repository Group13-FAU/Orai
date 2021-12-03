from django.http import JsonResponse
from django.shortcuts import render, redirect

from fetch_api.alg import build_sprints, get_requirements
from fetch_api.forms import SprintForm
from fetch_api.models import Story


def index(request):
    context = {'form': SprintForm()}
    return render(request, 'sprint/index.html', context=context)


def results(request):
    if request.method == "POST":
        form = SprintForm(request.POST)
        if form.is_valid():
            min_sprints = form.cleaned_data['min_sprints']
            sprint_complexity = form.cleaned_data['sprint_complexity']
            specific_story_ids = form.cleaned_data['specific_stories']
            max_dependants = form.cleaned_data['max_dependants_per_story']
            if not max_dependants:
                max_dependants = -1
            required = []
            requested_stories = []
            if len(specific_story_ids) > 0:
                ids = list(map(lambda str_id: int(str_id), specific_story_ids))
                requested_stories = Story.nodes.filter(nodeID__in=ids).all()
                required = get_requirements(requested_stories)
            print(
                f"build_sprints(len(required)={len(required)}, min_sprints={min_sprints}, sprint_complexity={sprint_complexity})")
            # Generate story list from build_sprints algorithm
            sprints = build_sprints(required, min_sprints, sprint_complexity, max_dependants)
            context = {
                'sprints': sprints,
                'min_sprints': min_sprints,
                'sprint_complexity': sprint_complexity,
                'requested_stories': requested_stories,
                'required_stories': required
            }
            if max_dependants != -1:
                context['max_dependants'] = max_dependants
            return render(request, 'sprint/results.html', context=context)

        else:
            return render(request, 'sprint/index.html', context={'form': form})
    else:
        return redirect(to='fetch_api:index')


def view_story(request, node_id):
    story = Story.nodes.filter(nodeID=node_id).first()

    return render(request, 'sprint/story.html', context={'story': story})


def story_relationships(request, node_id):
    # main_story =

    nodes = []
    relationships = []
    stories = Story.nodes.filter(nodeID=node_id).all()
    i = 0
    for story in stories:
        nodes.append({'id': story.nodeID, 'name': story.name, 'approved': story.approved})

        target = i

        for required_story in story.requires:
            req_story_json = {'id': required_story.nodeID, 'name': required_story.name, 'approved': story.approved}

            try:
                source = nodes.index(req_story_json)
            except ValueError:
                nodes.append(req_story_json)
                source = i
                i += 1
            relationships.append({'source': source, 'target': target})
    return JsonResponse({"nodes": nodes, "links": relationships})
