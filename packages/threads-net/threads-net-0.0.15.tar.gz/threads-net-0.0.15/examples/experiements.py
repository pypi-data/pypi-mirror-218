"""
Provide example of creating a thread implementation.
"""
import json

from threads import Threads


if __name__ == '__main__':
    threads = Threads(username='dmytro.striletskyi', password='dwnG58UfYf111')

    user_id = threads.get_user_id(username='dmytro.striletskyi')
    print(user_id)

    created_thread = threads.create_thread(caption='tasya i love you! 1 ')
    print(json.dumps(created_thread, indent=4))

    user = threads.get_user(id=user_id)
    print(user)

    created_thread = threads.create_thread(caption='tasya i love you! 2 ')
    print(json.dumps(created_thread, indent=4))

#
# import json
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, ensure_ascii=False, indent=4)
