import pytest
import requests
from type import *
import json
import random
import time

class TestBase:

    ids = []

    @pytest.mark.skip
    def get_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        print(json_data['_items'])
        return json_data['_items']

    @pytest.mark.skip
    def delete_all_projects(self, del_all=False):
        if del_all:
            resp = requests.get(URL_LIST_PROJECTS)
            json_data = json.loads(resp.text)
            _items = json_data['_items']
            ids = [x['_id'] for x in _items]
            for idx in ids:
                self.delete_project(idx)
            counter = 0
            while self.get_all_projects() and counter < 120:
                counter += 1
                print('Waiting for delete project')
                time.sleep(0.5)
        else:
            for idx in self.ids:
                self.delete_project(idx)

    @pytest.mark.skip
    def delete_project(self, project_id):
        try:
            resp = requests.delete(URL_DELETE_PROJECT + str(project_id))
            print(f"DEL PROJECT {project_id} SUCCESSFULLY")
            if resp.status_code == 404:
                return json.loads(resp.text)
        except Exception as e:
            print(f"DEL PROJECT ERROR: {e}")

    @pytest.mark.skip
    def create_project(self, video: str) -> json:
        with open(video, 'rb') as f:
            buffer = f.read()
        resp = requests.post(
            url=URL_CREATE_PROJECT,
            files={
                'file': (str(random.random()) + '.mp4', buffer, 'video/mp4')
            }
        )
        j = json.loads(resp.text)

        self.ids.append(j['_id'])

        return j
    
    @pytest.mark.skip
    def calc_hash_class(self, stream) -> bytes:
        return stream.__class__.__name__.encode('utf-8')
    
    @pytest.mark.skip
    def waiting_for_processing(self, project_id):
        while True:
            resp = requests.get(URL_LIST_PROJECTS + project_id)
            assert resp.status_code == 200
            j = json.loads(resp.text)
            processing = j['processing']
            is_processing = False
            is_processing = is_processing or processing['video']
            is_processing = is_processing or processing['thumbnail_preview']
            is_processing = is_processing or processing['thumbnails_timeline']

            if not is_processing:
                break

            time.sleep(0.25)
            print('Waiting for ...', project_id, time.time())

