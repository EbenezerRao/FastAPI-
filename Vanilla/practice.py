import uuid

class ProjectManager:
    def __init__(self):
        self.database = {}

    def add_project(self, title : str, tech_stack : str):
        proj_id = str(uuid.uuid4())[:6]
        self.database[proj_id] = {
            'title' : title,
            'tech_stack' : tech_stack
        }

        return {"message" : "Project added!", "project_id" : proj_id}
    
    def get_project(self):
        return self.database

manager = ProjectManager()

print("Adding projects...")
manager.add_project(title="AI Chatbot", tech_stack="Python, OpenAI")
manager.add_project(title="Portfolio Website", tech_stack="React, Tailwind")

print("\nAll Projects:")
print(manager.get_project())