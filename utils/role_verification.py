from fastapi import HTTPException


async def role_verification(user, function):
    allowed_functions_for_users = ["get_final", "get_final_final", "get_result", "create_result_t",
                                   "get_answer", "get_category", "get_question", "get_comment", "get_own",
                                   "update_user", "delete_user", "get_file"]

    if user.role == 'admin':
        return True
    elif user.role == "user" and function in allowed_functions_for_users:
        return True
    else:
        raise HTTPException(401, 'Sizga ruhsat berilmagan!')

