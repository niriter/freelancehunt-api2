import requests
from pprint import pprint


class Freelancehunt():
    def __init__(self, token='', api_url='https://api.freelancehunt.com/v2/'):
        if not token: raise NoApiToken("Api Token is not defined")
        self.token = token
        self.api_url = api_url
        self.api = self.API(token, api_url)

    class API:
        def __init__(self, token, api_url):
            self.token = token
            self.api_url = api_url
            self.init_classes()

        def init_classes(self):
            self.projects = self.Projects(self)
            self.projects.create = self.Projects.Create(self)
            self.projects.update = self.Projects.Update(self)
            self.projects.bids = self.Projects.Bids(self)
            self.projects.workspaces = self.Projects.Workspaces(self)
            self.projects.workspaces.conditions = self.Projects.Workspaces.Conditions(self)
            self.projects.workspaces.close = self.Projects.Workspaces.Close(self)

            self.profiles = self.Profiles(self)
            self.profiles.reviews = self.Profiles.Reviews(self)

            self.threads = self.Threads(self)
            self.threads.create = self.Threads.Create(self)

            self.skills = self.Skills(self)

            self.contests = self.Contests(self)
            self.contests.workspaces = self.Contests.Workspaces(self)
            self.contests.update = self.Contests.Update(self)

        def request(self, url, data='', type='POST'):
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer %s' % self.token
            }
            query = requests.request(type, self.api_url+url, data=data, headers = headers, allow_redirects=False, timeout=None)
            return query.json()

        class Projects:
            def __init__(self, API):
                self.api = API

            class Create:
                def __init__(self, API):
                    self.api = API

                def public(self, name, budget, safe_type, description_html, skills, expire_time, tags=False):
                    url = 'projects'
                    type = 'POST'
                    data = {
                        'name': name,
                        'budget': {
                            'amount': budget['amount'],
                            'currency': budget['currency']
                        },
                        'safe_type': safe_type,
                        'description_html': description_html,
                        'skills': skills,
                        'expire_time': expire_time
                    }
                    if tags: data['tags']=tags
                    return self.api.request(url, data, type)

                def personal(self, name, freelancer_id, is_personal, budget, safe_type, description_html, skills, expire_time, tags=False):
                    url = "projects"
                    type = "POST"
                    data = {
                        'name': name,
                        'freelancer_id': freelancer_id,
                        'is_personal': is_personal,
                        'budget': {
                            'amount': budget['amount'],
                            'currency': budget['currency']
                        },
                        'safe_type': safe_type,
                        'description_html': description_html,
                        'skills': skills,
                        'expire_time': expire_time
                    }
                    if tags: data['tags'] = tags
                    return self.api.request(url, data, type)

            class Update:
                def __init__(self, API):
                    self.api = API

                def without_bids(self, project_id, name, budget, safe_type, description_html, skills, expire_time, tags=False):
                    url = 'projects/'+project_id
                    type = 'PATCH'
                    data = {
                        'name': name,
                        'budget': {
                            'amount': budget['amount'],
                            'currency': budget['currency']
                        },
                        'safe_type': safe_type,
                        'description_html': description_html,
                        'skills': skills,
                        'expire_time': expire_time
                    }
                    if tags: data['tags'] = tags
                    return self.api.request(url, data, type)

                def with_bids(self, project_id, budget, update_html, skills):
                    url = 'projects/' + project_id + '/amend'
                    type = 'POST'
                    data = {
                        'budget': {
                            'amount': budget['amount'],
                            'currency': budget['currency']
                        },
                        'update_html': update_html,
                        'skills': skills
                    }
                    return self.api.request(url, data, type)

                def expire_date(self, project_id, expire_time):
                    url = 'projects/' + project_id + '/extend'
                    type = 'POST'
                    data = {
                        'expire_time': expire_time
                    }
                    return self.api.request(url, data, type)

            class Bids:
                def __init__(self, API):
                    self.api = API

                def get(self, project_id, is_winner=False, status=False):
                    url = 'projects/' + project_id + '/bids'
                    type = 'GET'
                    data = {}
                    if is_winner: data['is_winner'] = is_winner
                    if status: data['status'] = status
                    return self.api.request(url, data, type)

                def get_my(self, project_id=False, status=False):
                    url = 'projects/my/bids'
                    type = 'GET'
                    data = {}
                    if project_id: data['project_id'] = project_id
                    if status: data['status'] = status
                    return self.api.request(url, data, type)

                def revoke(self, project_id, bid_id):
                    url = 'projects/'+project_id+'/bids/'+bid_id+'/revoke'
                    type = 'POST'
                    return self.api.request(url, type)

                def restore(self, project_id, bid_id):
                    url = 'projects/' + project_id + '/bids/' + bid_id + '/restore'
                    type = 'POST'
                    return self.api.request(url, type)

                def reject(self, project_id, bid_id):
                    url = 'projects/' + project_id + '/bids/' + bid_id + '/reject'
                    type = 'POST'
                    return self.api.request(url, type)

                def choose_winner(self, project_id, bid_id, comment):
                    url = 'projects/' + project_id + '/bids/' + bid_id + '/choose'
                    type = 'POST'
                    data = {'comment':comment}
                    return self.api.request(url, data, type)

                def add(self, project_id, days, budget, safe_type, comment, is_hidden=False):
                    url = 'projects/' + project_id + '/bids'
                    type = 'POST'
                    data = {
                        'days': days,
                        'budget': {
                            'amount': budget['amount'],
                            'currency': budget['currency']
                        },
                        'safe_type': safe_type,
                        'comment': comment,
                        'is_hidden': is_hidden
                    }
                    return self.api.request(url, data, type)

            class Workspaces:
                def __init__(self, API):
                    self.api = API

                def get_list(self, project_id=False):
                    url = "my/workspaces/projects"
                    type = "GET"
                    if project_id: data={'project_id':project_id}
                    return self.api.request(url, data, type)

                def get_details(self, project_id):
                    url = "my/workspaces/projects/"+project_id
                    type = "GET"
                    return self.api.request(url, type)

                class Conditions:
                    def __init__(self, API):
                        self.api = API

                    def new(self, project_id, days, budget, safe_type, comment):
                        url = "workspaces/projects/"+project_id+"/propose-conditions"
                        type = "POST"
                        data = {
                            'days': days,
                            'budget': {
                                'amount': budget['amount'],
                                'currency': budget['currency']
                            },
                            'safe_type': safe_type,
                            'comment': comment
                        }
                        return self.api.request(url, data, type)

                    def accept(self, project_id):
                        url = "workspaces/projects/" + project_id + "/accept-conditions"
                        type = "POST"
                        return self.api.request(url, type)

                    def reject(self, project_id):
                        url = "workspaces/projects/" + project_id + "/reject-conditions"
                        type = "POST"
                        return self.api.request(url, type)

                def update_expire_date(self, project_id, days):
                    url = "workspaces/projects/" + project_id + "/extend"
                    type = "POST"
                    data = {'days': days}
                    return self.api.request(url, data, type)

                def request_arbitrage(self, project_id, comment):
                    url = "workspaces/projects/" + project_id + "/request-arbitrage"
                    type = "POST"
                    data = {'comment_html': comment}
                    return self.api.request(url, data, type)

                class Close:
                    def __init__(self, API):
                        self.api = API

                    def as_complete(self, project_id, grades, review):
                        url = "workspaces/projects/" + project_id + "/complete"
                        type = "POST"
                        data = {'grades': grades, 'review': review}
                        return self.api.request(url, data, type)

                    def as_incomplete(self, project_id, grades, review):
                        url = "workspaces/projects/" + project_id + "/incomplete"
                        type = "POST"
                        data = {'grades': grades, 'review': review}
                        return self.api.request(url, data, type)

                    def without_review(self, project_id, review):
                        url = "workspaces/projects/" + project_id + "/close"
                        type = "POST"
                        data = {'review': review}
                        return self.api.request(url, data, type)

                def write_review(self, project_id, grades, review):
                    url = "workspaces/projects/" + project_id + "/review"
                    type = "POST"
                    data = {'grades': grades, 'review': review}
                    return self.api.request(url, data, type)

            def get_projects(self, only_my_skills=False, skill_id='', employer_id=''):
                url = 'projects'
                type = 'GET'
                data = {'only_my_skills': only_my_skills}
                if skill_id: data['skill_id'] = skill_id
                if employer_id: data['employer_id'] = employer_id
                return self.api.request(url, data, type)

            def get_project(self, project_id):
                url = 'projects/'+project_id
                type = 'GET'
                return self.api.request(url, type)

            def get_my_projects(self, project_id, skill_id, status_id):
                url = 'projects/'+project_id
                type = 'GET'
                data = {}
                if skill_id: data['skill_id'] = skill_id
                if status_id: data['status_id'] = status_id
                return self.api.request(url, data, type)

            def close(self, project_id):
                url = 'projects/' + project_id + '/close'
                type = 'POST'
                return self.api.request(url, type)

            def reopen(self, project_id, expire_time):
                url = 'projects/' + project_id + '/reopen'
                type = 'POST'
                data = {'expire_time': expire_time}
                return self.api.request(url, data, type)

        class Profiles:
            def __init__(self, API):
                self.api = API

            class Reviews:
                def __init__(self, API):
                    self.api = API

                def freelancer(self, profile_id):
                    url = 'freelancers/' + profile_id + '/reviews'
                    type = 'GET'
                    return self.api.request(url, type)

                def employer(self, profile_id):
                    url = 'employers/' + profile_id + '/reviews'
                    type = 'GET'
                    return self.api.request(url, type)

                def my(self):
                    url = 'my/reviews'
                    type = 'GET'
                    return self.api.request(url, type)

            def feed(self):
                url = 'my/feed'
                type = 'GET'
                return self.api.request(url, type)

            def freelancers(self, country_id=False, city_id=False, skill_id=False, login=False):
                url = 'freelancers'
                type = 'GET'
                data = {}
                if country_id: data['country_id'] = country_id
                if city_id: data['city_id'] = city_id
                if skill_id: data['skill_id'] = skill_id
                if login: data['login'] = login
                return self.api.request(url, data, type)

            def employers(self, country_id=False, city_id=False, login=False):
                url = 'employers'
                type = 'GET'
                data = {}
                if country_id: data['country_id'] = country_id
                if city_id: data['city_id'] = city_id
                if login: data['login'] = login
                return self.api.request(url, data, type)

            def my(self):
                url = 'my/profile'
                type = 'GET'
                return self.api.request(url, type)

            def get_freelancer(self, profile_id):
                url = 'freelancers/'+profile_id
                type = 'GET'
                return self.api.request(url, type)

            def get_employer(self, profile_id):
                url = 'employers/'+profile_id
                type = 'GET'
                return self.api.request(url, type)

        class Threads:
            def __init__(self, API):
                self.api = API

            def all(self):
                url = 'threads'
                type = 'GET'
                return self.api.request(url, type)

            def add_message(self, thread_id, message_html):
                url = 'threads/'+thread_id
                type = 'POST'
                data = {'message_html': message_html}
                return self.api.request(url, data, type)

            def get(self, thread_id):
                url = 'threads/'+thread_id
                type = 'GET'
                return self.api.request(url, type)

            def delete(self, thread_id):
                url = 'threads/'+thread_id
                type = 'DEL'
                return self.api.request(url, type)

            class Create:
                def __init__(self, API):
                    self.api = API

                def support(self, subject, message_html):
                    url = 'threads/actions/support'
                    type = 'POST'
                    data = {'subject': subject, 'message_html': message_html}
                    return self.api.request(url, data, type)

                def to_user(self, subject, message_html, to_profile_id):
                    url = 'threads'
                    type = 'POST'
                    data = {'subject': subject, 'message_html': message_html, 'to_profile_id': to_profile_id}
                    return self.api.request(url, data, type)

        class Skills:
            def __init__(self, API):
                self.api = API

            def list(self):
                url = 'skills'
                type = 'GET'
                return self.api.request(url, type)

        class Contests:
            def __init__(self, API):
                self.api = API

            class Workspaces:
                def __init__(self, API):
                    self.api = API

                def list(self, contest_id=False):
                    url = 'my/workspaces/contests/'
                    type = 'GET'
                    data = {}
                    if contest_id: data = {'contest_id': contest_id}
                    return self.api.request(url, data, type)

                def details(self, workspace_id):
                    url = 'my/workspaces/contests/'+workspace_id
                    type = 'GET'
                    return self.api.request(url, type)

                def close(self, workspace_id, comment):
                    url = 'my/workspaces/contests/'+workspace_id+"/complete"
                    type = 'POST'
                    data = {'comment': comment}
                    return self.api.request(url, data, type)

            def list(self, skill_id=False, employer_id=False):
                url = 'contests/'
                type = 'GET'
                data = {}
                if skill_id: data['skill_id'] = skill_id
                if employer_id: data['employer_id'] = employer_id
                return self.api.request(url, data, type)

            def my_list(self, skill_id=False, status_id=False):
                url = 'my/contests/'
                type = 'GET'
                data = {}
                if skill_id: data['skill_id'] = skill_id
                if status_id: data['status_id'] = status_id
                return self.api.request(url, data, type)

            def details(self, contest_id):
                url = 'contests/'+contest_id
                type = 'GET'
                return self.api.request(url, type)

            class Update:
                def __init__(self, API):
                    self.api = API
                #TODO optional parameters
                def before_publication(self, contest_id, name, budget, duration_days, description_html):
                    url = 'contests/'+contest_id
                    type = 'PATCH'
                    data = {'name': name, 'budget': budget, 'duration_days': duration_days, 'description_html': description_html}
                    return self.api.request(url, data, type)

                def after_publication(self, contest_id, update_html):
                    url = 'contests/'+contest_id+'/amend'
                    type = 'POST'
                    data = {'update_html': update_html}
                    return self.api.request(url, data, type)

if __name__ == "__main__":
    freelance = Freelancehunt()
    pprint(freelance.api.projects.get_projects())