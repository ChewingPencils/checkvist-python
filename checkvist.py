#!/usr/bin/env python
# Title:     Checkvist API Wrapper
# Author:    Sean Korzdorfer
# Date:      Tue Nov 20 2012
#
# All documentation found here involves this wrapper. For complete API docs, please see
# https://checkvist.com/auth/api
#
# This wrapper was designed to be simple enough for use with the Pythonista app: 
# https://itunes.apple.com/us/app/pythonista/id528579881?mt=8
# 
# Considering iOS usage, I chose to use a print debugger instead of logging.
# See the documentation below to turn it on.
#
  
import requests
import json 
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)



auth_url = 'https://checkvist.com/auth/login.json'


class user_account:
    """ Create Instance """
    def __init__(self, user_id, api_key, bugger=0):
        """Assign user credentials.
        
        Example: 
        cl = checkvist.user_account('account@email.com', 'akdjfdfhoihhg')
        
        To turn on Debugger:
        cl = checkvist.user_account('account@email.com', 'akdjfdfhoihhg', bugger=1)

        
        """
        self.username = user_id
        self.remote_key = api_key
        if bugger == 1:
            self.bugger = True
        else:
            self.bugger = False

    
    
    def send_auth(self):
        """ Get authenication token.
       
        Example: 
        cl.send_auth()
        
        """
        r = requests.post(auth_url, {'username': self.username, 'remote_key': self.remote_key})
        if r.status_code is 200:
           self.api_token = r.text.replace('"', '').strip()
           return True
        else: 
            return False
     
    
    def get_user(self):
        """Get user information.
        
        Example:     
        user = cl.get_user()
        print user['username']            
        
        """
        user_url = 'http://checkvist.com/auth/curr_user.json'
        payload = {'token': self.api_token}
        r = requests.get(user_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: 
            return False

    # Get users lists
    # 
    # my_lists = cl.get_lists()
    # for i in my_lists:
    #    print i['name']
        
    def get_lists(self):
        """Get all the user's lists
        
        Returns a list of dictionaries: https://checkvist.com/auth/api#checklist_data
        
        Example: 
        my_lists = cl.get_lists()
        for i in my_lists:
            print i['name']
            
        """
        list_url = 'http://checkvist.com/checklists.json'
        payload = {'token': self.api_token}
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: 
            return False
        
        
    def get_archive_lists(self):
        
        list_url = 'http://checkvist.com/checklists.json'
        payload = {'token': self.api_token, 'archived': 'true'}
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok:
            return parsed_json
        else: return False
        
    def get_list_info(self, list_id):
        """Get Checklist Information
        
        Argument: the id number of the list

        Example: 
        my_list_info = cl.get_list_info('155786')
        print my_list_info['name']    

        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '.json'
        payload = {'token': self.api_token}
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: return parsed_json
        else: return False
        
        
    def create_list (self, list_name, is_public=0):
        """Create a new checklist
        
        Arguments:
            name of list (string) Required
            if the list is public (0 or 1) optional; defaults to 0
        
        Example:
        Private Lists:
            new_list = cl.create_list('test list') 
            new_list = cl.create_list('test list', is_public=0)  
        Public Lists:
            new_list = cl.create_list('test list', is_public=1)
        """
        list_url = 'http://checkvist.com/checklists.json'
        payload = {'token': self.api_token, 'checklist[name]': list_name}
        if is_public == 1:
            payload['checklist[public]'] =1
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
        

    def update_list(self, list_id, list_name='', is_public=''):
        """Update an existing checklist
        
        Arguments:
            list id number Required
            name of list (string) Required
            if the list is public (0 or 1) optional. If the argument is not provided it is ignored
        
        Example:
        Change list name, but make no changes to public:
           my_list = cl.update_list('156984', list_name='test list') 
        Change List name and make the list private:
            new_list = cl.create_list('156984','test list', is_public=0)  
        Make list Public:
            new_list = cl.create_list('156984', is_public=1)
                
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '.json'
        payload = {'token': self.api_token,}
        if list_name:
            payload['checklist[name]'] = list_name
        if is_public == 1:
            payload['checklist[public]'] = 1 
        elif is_public == 0:
            payload['checklist[public]'] = 0
        r = requests.put(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False


    def delete_list(self, list_id):
        """Delete a list
        
        Arguments: 
            list_id
            
        Example:
        my_list = cl.delete_list('156984')
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '.json'
        payload = {'token': self.api_token}
        r = requests.delete(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False


#### Tasks ####


    def get_tasks(self, list_id, notes=''):
        """Get all tasks from a list (with or without notes)
        
        Arguments:
            list_id - The id number of the list
            notes   - Flag for receiving note information
        
        Example: 
        my_tasks = cl.get_tasks('156983')
        
        With notes:
            
        my_tasks = cl.get_tasks('156983' notes=1)
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks.json'
        if notes:
            payload = {'token': self.api_token, 'with_notes': notes}
        else:
            payload = {'token': self.api_token,}       
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok:
             return parsed_json
        else: return False



    def get_task(self, list_id, task_id, notes=''):
        """Get a specific task from a list (with or without notes)
        
        Arguments:
            list_id - The id number of the list
            task_id - the id of the task 
            notes   - Flag for receiving note information (optional)
        
        Example: 
        my_note = cl.get_task('156983')
        
        With notes:
            
        my_note = cl.get_task('156983' notes=1)
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '.json'
        if notes:
            payload = {'token': self.api_token, 'with_notes': notes}
        else:
            payload = {'token': self.api_token,}
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger:
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False


    def add_task(self, list_id, task_content, parent_id='', tags='', due_date='', position=0, status=''):
        """Add a new task to a specific list

        Arguments:
            list_id      - ID number of the list to receive the task   | string | Required
            task_content - Content of task                             | string | Required
            parent_id    - ID number of a parent task                  | string | Optional
            tags         - Task Tags. seperated by commas. NO SPACES.  | string | Optional
            due_date     - Task due date. Uses Checkvist smart syntax. | string | Optional
            position     - 1 for top of list. omit for bottom          | string | Optional
            status       - Task status                                 | string | Optional
            
        Status Valuse:
            1 - close
            2 - invalidate
            3 - reopen
            
        Examples:
        my_task = cl.add_task('156983', 'I just added a damn subtask!', parent_id='7290244', tags='hot-damn')

        my_task = cl.add_task('156983', 'I just added task to the top of the list!', tags='#1', due_date="2013-01-13", position=1)

        my_task = cl.add_task('156983', 'I created a closed task ...', tags='wtf', status=1)
            
        """
        list_url = 'http://checkvist.com/checklists/' + list_id+ '/tasks.json'
        payload = {'token': self.api_token}
        payload['task[content]'] = task_content
        if parent_id:
            print "I have ID:" + parent_id + '\n'
            payload['task[parent_id]'] = parent_id
        # Perform very basic check for comma delimited tags.
        if ' ' in tags and not ',' in tags:
            payload['task[tags]'] =  tags.replace(' ', ',').strip()
        else:
            payload['task[tags]'] = tags.strip()
  
        if due_date:
            payload['task[due_date]'] = due_date
        if position == 1:
            payload['task[position]'] = position
        if status:
           payload['task[status]'] = status
        
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False



    def import_tasks(self, list_id, import_content):
        """Add a task or tasks using the import feature.
        
        See doc: https://checkvist.com/auth/help#supportedFormats
        
        Arguments:
            list_id
            import_content - string formmatted according to the above doc.
        
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/import.json'
        payload = {'token': self.api_token, 'import_content': import_content}
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False



    def update_task(self, list_id, task_id, task_content='', parent_id='', tags='', due_date='', position=''):
        """Update a task

        Arguments:
            list_id      - ID number of the list to receive the task   | string | Required
            task_id      - ID number of the task to update             | string | Required
            task_content - Content of task                             | string | Optional
            parent_id    - ID number of a parent task                  | string | Optional
            tags         - Task Tags. seperated by commas. NO SPACES.  | string | Optional
            due_date     - Task due date. Uses Checkvist smart syntax. | string | Optional
            position     - 1 for top of list. omit for bottom          | string | Optional
            status       - Task status                                 | string | Optional
            
        Status Valuse:
            1 - close
            2 - invalidate
            3 - reopen
            
        Examples:
        Change task parent:
            my_task = cl.update_task('156983', '7290225', parent_id='7290244')
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '.json'
        payload = {'token': self.api_token}
        # Task content is optional. Test for existence.
        if task_content:
            payload['task[content]'] = task_content
        if parent_id:
            payload['task[parent_id]'] = parent_id
        
        if ' ' in tags and not ',' in tags:
            payload['task[tags]'] =  tags.replace(' ', ',').strip()
        else:
            payload['task[tags]'] = tags.strip()
  
        if due_date:
            payload['task[due_date]'] = due_date
        if position:
            payload['task[position]'] = position

        
        r = requests.put(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok:
            return parsed_json
        else: return False
        
    def close_task(self, list_id, task_id):
        """Close Task Status
            
        Both list_id and task_id are required    
        
        Example:
        my_task = cl.close_task('156983', '7291390')
            
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/close.json'
        payload = {'token': self.api_token}
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
   
    def reopen_task(self, list_id, task_id):
        """Reopen Task Status
            
        Both list_id and task_id are required    
        
        Example:
        my_task = cl.reopen_task('156983', '7291390')
            
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/reopen.json'
        payload = {'token': self.api_token}
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
    
    def invalidate_task(self, list_id, task_id):
        """invalidate Task Status
            
        Both list_id and task_id are required    
        Example:
        my_task = cl.invalidate_task('156983', '7291390')
            
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/invalidate.json'
        payload = {'token': self.api_token}
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
        
    
    
    def delete_task(self, list_id, task_id):
        """Delete
            
        Both list_id and task_id are required    
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '.json'
        payload = {'token': self.api_token}
        r = requests.delete(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
        



#### Notes ####


    def get_notes(self, list_id, task_id):
        """Get Notes
        
        list_id and task_id are Required
        
        Example:
        my_notes = cl.get_notes('156983', '7291617')
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/comments.json'
        payload = {'token': self.api_token}
        r = requests.get(list_url, params=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
        
    def add_note(self, list_id, task_id, comment):
        """Add a note to a task
        
        list_id and task_id and are Required
        
        comment - note text. string. Required
        
        Example:
        my_note = cl.add_note('156983', '7291617', 'this is a note.')
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/comments.json'
        payload = {'token': self.api_token, 'comment[comment]': comment}
        r = requests.post(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False

    def update_note(self, list_id, task_id, note_id, comment):
        """Update a specific note.
        
        list_id and task_id and note_id are Required.
        
        comment - note text. string. Required.
        
        Example:
        my_note = cl.update_note('156983', '7291617', '337056', 'I just updated the note text.')
        
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/comments/' + note_id + '.json'
        payload = {'token': self.api_token, 'comment[comment]': comment}
        r = requests.put(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False

    def delete_note(self, list_id, task_id, note_id):
        """Delete a specific note. 
                
        list_id and task_id and note_id are Required
          
          
        Example:
        my_note = cl.delete_note('156983', '7291617', '337056')
         
        """
        list_url = 'http://checkvist.com/checklists/' + list_id + '/tasks/' + task_id + '/comments/' + note_id + '.json'
        payload = {'token': self.api_token}
        r = requests.delete(list_url, data=payload)
        parsed_json = json.loads(r.content)
        if self.bugger: 
            pp.pprint(parsed_json)
        if r.status_code == requests.codes.ok: 
            return parsed_json
        else: return False
