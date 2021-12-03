from fetch_api.models import Story
from fetch_api.utils import Sprint


def get_requirements(stories: list[Story], solved=None) -> list[Story]:
    if solved is None:
        solved = []
    if len(stories) == 0:
        return solved
    new_requirements = []
    for story in stories:
        requirements = story.requires.all()
        unique_requirements = list(filter(lambda s: s not in stories and s not in solved, requirements))
        new_requirements += unique_requirements
    new_solved = stories + solved
    return get_requirements(new_requirements, new_solved)


def get_story_ids(stories: list[Story]) -> list[int]:
    return list(map(lambda story: story.nodeID, stories))


def get_all_stories_not_in(list1: list[Story], list2: list[Story]) -> list[Story]:
    return list(filter(lambda s: s not in list2, list1))


# order by highest priority with lowest complexity
def order_filter(order_list: list[Story]) -> list[Story]:
    order_list.sort(key=lambda story: int(story.priority) - int(story.complexity))
    for i in range(len(order_list)):
        for j in range(i + 1, len(order_list)):
            if (order_list[i].priority - order_list[i].complexity) < (
                    order_list[j].priority - order_list[j].complexity):
                temp = order_list[i]
                order_list[i] = order_list[j]
                order_list[j] = temp

    return order_list


def order_stories(required_stories: list[Story]) -> list[Story]:
    scheduled_stories = []

    # Loop until we schedule everything
    while len(scheduled_stories) < len(required_stories):
        scheduled_ids = get_story_ids(scheduled_stories)

        # Get a list of all the stories we haven't scheduled yet
        unscheduled = list(filter(lambda s: s not in scheduled_stories, required_stories))

        print(f"There are {len(unscheduled)} unscheduled stories")
        # If there are no tasks left to schedule then we're done
        if len(unscheduled) == 0:
            print('Nothing left to schedule breaking the loop')
            break

        # Get a list of all the stories we haven't scheduled yet
        #   but have their requirements met by stories that are scheduled
        can_work = []
        for story in unscheduled:
            requirements = story.requires.all()
            if len(requirements) == 0:
                can_work.append(story)
            else:
                requirement_ids = get_story_ids(requirements)
                if all(nodeID in scheduled_ids for nodeID in requirement_ids):
                    can_work.append(story)

        # If we can_work is only 1 story then schedule it
        if len(can_work) == 1:
            print('Only 1 story can be scheduled, scheduling it now')
            scheduled_stories += can_work

        # Else if can_work is a list of stories we need to
        #   figure out how to order them and then add them to scheduled
        elif len(can_work) > 1:
            can_work.sort(key=lambda s: int(s.priority) - int(s.complexity))

            for story in can_work:
                scheduled_stories.append(story)

        # Else there are no stories in can_work that we can schedule.
        #   This should probably throw an error if scheduled is empty
        else:
            raise Exception("No tasks in can be scheduled due to dependencies")
    return scheduled_stories


def partition_sprints(ordered_stories: list[Story],
                      min_sprints: int,
                      max_complexity: int,
                      max_dependants: int) -> list[Sprint]:
    dependant_count = 0
    sprints = []
    scheduled_stories = []
    if len(ordered_stories) > 0:
        highest_complexity = max(map(lambda s: s.complexity, ordered_stories))
        if highest_complexity > max_complexity:
            print(f"WARNING: provided max_complexity is less than the largest story")
            max_complexity = highest_complexity

    # Loop until we have build min_sprint number of sprints and until all the ordered stories have been put into sprints
    while len(sprints) < min_sprints or not all(story in scheduled_stories for story in ordered_stories):
        # Create a new sprint
        sprint = Sprint(f"Sprint #{len(sprints) + 1}")

        # Get all of the stories we haven't put into sprints yet
        unscheduled_stories = get_all_stories_not_in(ordered_stories, scheduled_stories)

        # Loop through all of the unscheduled stories until adding
        #   the next one would make the sprint complexity > max_complexity
        for unscheduled_story in unscheduled_stories:
            if sprint.total_complexity() + unscheduled_story.complexity <= max_complexity:
                if max_dependants != -1 and dependant_count < max_dependants:

                    sprint.append(unscheduled_story)
                    scheduled_stories.append(unscheduled_story)
                    dependant_count += 1
                elif max_dependants == -1:
                    sprint.append(unscheduled_story)
                    scheduled_stories.append(unscheduled_story)
            else:
                break

        # If the sprint's total complexity is less than the max add a story from the filler list
        if sprint.total_complexity() < max_complexity:
            missing_complexity = max_complexity - sprint.total_complexity()
            scheduled_ids = get_story_ids(scheduled_stories)
            unscheduled_fillers = Story.nodes.exclude(nodeID__in=scheduled_ids) \
                .has(requires=False) \
                .filter(complexity__lte=missing_complexity) \
                .order_by('-complexity') \
                .all()
            for unscheduled_filler in unscheduled_fillers:
                if sprint.total_complexity() + unscheduled_filler.complexity <= max_complexity:
                    sprint.append(unscheduled_filler)
                    scheduled_stories.append(unscheduled_filler)
                else:
                    if sprint.total_complexity() < max_complexity:
                        print("WARNING: no filler available to fill the sprint")
                    break

        # If we added stories to this sprint add it to the end result
        if len(sprint) > 0:
            sprints.append(sprint)
            dependant_count = 0

        # Otherwise we should probably handle this error
        else:
            raise Exception("Failed to schedule all of the stories")

    return sprints


def build_sprints(required: list[Story],
                  min_sprints: int,
                  sprint_complexity: int,
                  max_dependants: int) -> list[Sprint]:
    scheduled = order_stories(required)
    return partition_sprints(scheduled, min_sprints, sprint_complexity, max_dependants)
