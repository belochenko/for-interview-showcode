from utils.db_api.models import User, PostApproval
from loader import db


def create_reg_list():
    """
    Creates list of register requests
    :return list_of_regs, regs_id:
    """
    query = User.select(User.first_name, User.last_name, User.user_id).where(User.is_approve == 0)
    rw = [row for row in query.tuples()]
    list_of_regs = [f'{name} {surname}'for name, surname, _ in rw]
    regs_id = [user_id for _, _, user_id in rw]
    return list_of_regs, regs_id


def create_post_list():
    """
        Creates list of post requests
        :return list_of_posts:
    """
    query = db.execute_sql(
        '''
        Select u.first_name,u.last_name,postapproval.post_user_id user_id,
        postapproval.post_message_id,postapproval.post_chat_ids
        from postapproval
        Left join "user" u on u.user_id = postapproval.post_user_id
        '''
    )
    return [row for row in query]
