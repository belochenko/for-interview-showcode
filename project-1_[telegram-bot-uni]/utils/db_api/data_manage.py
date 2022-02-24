from .models import User, Groups, PostApproval

# TODO Remove file and import all functions to utils.db_api.db


async def push_user(username, first_name,  # Temporary solution
                    last_name, phone_number, email,
                    learning_year, major, user_id,
                    role, is_approve):
    """
    Push user to database
    :param username:
    :param first_name:
    :param last_name:
    :param phone_number:
    :param email:
    :param learning_year:
    :param major:
    :param user_id:
    :param role:
    :param is_approve:
    :return:
    """
    row = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phoneNumber=phone_number,
        email=email,
        learningYear=learning_year,
        Major=major,
        user_id=user_id,
        role=role,
        is_approve=is_approve
    )
    row.save(force_insert=True)


async def db_user_check(col_name, value):  # Temporary solution
    """
    Checks if user preset in database
    :param col_name:
    :param value:
    :return query.exists():
    """
    query = User.select().where(getattr(User, col_name) == value)
    return query.exists()


async def push_group(group_id, group_title, group_major, group_user_id):
    """
    Push group to database
    :param group_id:
    :param group_title:
    :param group_major:
    :param group_user_id:
    :return:
    """
    row = Groups(
        group_id=group_id,
        group_title=group_title,
        group_major=group_major,
        group_user_id=group_user_id,
    )
    row.save(force_insert=True)


async def push_post_approval(user_id, message_id, chat_ids):
    """
    Push post request to database
    :param user_id:
    :param message_id:
    :param chat_ids:
    :return:
    """
    row = PostApproval(
        post_user_id=user_id,
        post_message_id=message_id,
        post_chat_ids=chat_ids
    )
    row.save(force_insert=True)
