"""
Provide example of making a login to Threads via Instagram implementation.
"""
import json
import os

from threads import Threads


if __name__ == '__main__':
    # threads = Threads()
    # threads.load_settings('session.json')
    # threads.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'))
    # threads.set_proxy("http://spjibgcve0:T5l9fEpwSu2eY2qwdo@gate.smartproxy.com:10000")
    #
    # threads.post_thread()

    threads = Threads()
    threads.load_settings('session.json')
    # threads.set_proxy("http://spjibgcve0:T5l9fEpwSu2eY2qwdo@gate.smartproxy.com:10001")
    threads.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'))

    # threads.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'))
    # threads.dump_settings('session.json')







    # user = threads.get_user_by_username(username='zuck')
    # print(json.dumps(user, indent=4))


    def post_thread(self):
        data = {
            'publish_mode': "text_post",
            'text_post_app_info': {
                'reply_control': 0,
            },
            'caption': 'Hello it is my first thread!'
        }

        res = self.private_request(endpoint='media/configure_text_only_post/', data=self.with_default_data(data))

        print(res)

        return res
