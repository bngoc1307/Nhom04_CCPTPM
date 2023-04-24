import pytest
import requests
import json
import random
import time
import binascii
import os
from type import *
from hash_video import *
class TestEditVideo:
    @pytest.mark.skip
    def get_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        print(json_data['_items'])

    @pytest.mark.skip
    def delete_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        _items = json_data['_items']
        ids = [x['_id'] for x in _items]
        print(f'------ DELETE {len(ids)} projects')
        for idx in ids:
            self.delete_project(idx)

    @pytest.mark.skip
    def delete_project(self, project_id):
        resp = requests.delete(URL_DELETE_PROJECT + str(project_id))
        if resp.status_code == 204:
            return True
        else:
            return json.loads(resp.text)

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
        return json.loads(resp.text)

    @pytest.mark.skip
    def retrieve_project(self, project_id) -> json:
        resp = requests.get(
            URL_RETRIEVE_PROJECT + str(project_id)
        )
        return json.loads(resp.text)

    @pytest.mark.skip
    def duplicate_project(self, project_id) -> json:
        resp = requests.post(
            URL_RETRIEVE_PROJECT + str(project_id) + '/duplicate'
        )
        return json.loads(resp.text)

    @pytest.mark.skip
    def edit_project(self, project_id, json_request) -> json:
        resp = requests.put(
            URL_RETRIEVE_PROJECT + str(project_id),
            json=json_request,
        )
        return json.loads(resp.text)

    @pytest.mark.skip
    def get_video(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/video'
        )
        return  resp.content, resp.status_code

    def test_01(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Edit video gốc vừa tạo
            3. Kiểm tra xem có thông báo không cho edit video gốc hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }
        
        resp_project = self.edit_project(_id_create, json_request)
        print(resp_project)

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        assert resp_project['project_id'] == ['Video with version 1 is not editable, use duplicated project instead.']


    def test_02(self):
        """
            `Test activity diagram: EDIT PROJECT DETAILS`
            1. Edit project với id không tồn tại
            2. Kiểm tra xem có thông báo lỗi hay không
        """
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8')    
        print(_id)    

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }

        resp_project = self.edit_project(_id, json_request)
        print(resp_project)
        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

    def test_03(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']

        json_request = {
                "scale": 1000
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)

        while (True):
            video, status_code = self.get_video(_id_dup)
            time.sleep(0.5)
            if status_code == 200:
                break

        with open('test_data/video-after-edit-03.mp4', 'rb') as file:
            video2 = file.read()
        video_hash = hashlib.sha256(video).hexdigest()
        video_samp = hashlib.sha256(video2).hexdigest()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        assert video_hash == video_samp

    def test_04(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']

        json_request = {
                "crop": "400,300,320,180"
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)

        while (True):
            video, status_code = self.get_video(_id_dup)
            time.sleep(0.5)
            if status_code == 200:
                break

        with open('test_data/video-after-edit-04.mp4', 'rb') as file:
            video2 = file.read()
        video_hash = hashlib.sha256(video).hexdigest()
        video_samp = hashlib.sha256(video2).hexdigest()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        assert video_hash == video_samp

    def test_05(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)

        while (True):
            video, status_code = self.get_video(_id_dup)
            time.sleep(0.5)
            if status_code == 200:
                break

        with open('test_data/video-after-edit-02.mp4', 'rb') as file:
            video2 = file.read()
        video_hash = hashlib.sha256(video).hexdigest()
        video_samp = hashlib.sha256(video2).hexdigest()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        assert video_hash == video_samp