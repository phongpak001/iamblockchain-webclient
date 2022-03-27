from base.models import Sharing, Task
import rules

# Predicates
@rules.predicate
def is_editable(user, task):
    if task.view_only == False:
        return True
    else:
        return False

@rules.predicate
def is_task_owner(user, task):
    return task.user == user

@rules.predicate
def is_share_owner(user, sharing):
    return sharing.user == user

@rules.predicate
def is_boss(user):
    return user.is_superuser

# Rules

rules.add_rule("change_task", is_task_owner | is_editable | is_boss)
rules.add_rule("delete_task", is_task_owner | is_boss)
rules.add_rule("change_sharing", is_share_owner | is_boss)
rules.add_rule("delete_sharing", is_share_owner| is_boss)

# Permissions
rules.add_perm("base.change_task", is_task_owner | is_editable | is_boss)
rules.add_perm("base.delete_task", is_task_owner | is_boss)
rules.add_perm("base.change_sharing", is_share_owner | is_boss)
rules.add_perm("base.delete_sharing", is_share_owner | is_boss)