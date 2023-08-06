import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class Commits(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Commits,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project(self, project_id):
		
		commit_list = []

		try:
			logging.info("Start function: get_commit_projeto")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_Commits:"+project.name )
			commits = project.commits.list(iterator=True,get_all=True)
			project = project.asdict()
			for	commit in commits:
				commitX = commit.asdict()
				commitX['project_id'] = project['id']
				#commitX['merge_requests'] = commit.merge_requests()
				commitX['refs'] = commit.refs() 
				#commitX['comments'] = commit.comments.list()
				#commitX['statuses '] = commit.statuses.list()

				commit_list.append(commitX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s Commits")
		
		return commit_list
	
	
	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: get_Commits")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				logging.info("Start function: get_Commits:"+project.name )
				commits = project.commits.list(iterator=True,get_all=True)
				project = project.asdict()
				for	commit in commits:
					commitX = commit.asdict()
					commitX['project_id'] = project['id']
					#commitX['merge_requests'] = commit.merge_requests()
					commitX['refs'] = commit.refs() 
					#commitX['comments'] = commit.comments.list()
					#commitX['statuses '] = commit.statuses.list()

					commit_list.append(commitX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Commits")
		
		return commit_list
