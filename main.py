from dotenv import load_dotenv
import github
from github import Github, Auth
import os

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

g = Github(auth=github.Auth.Token(token))

testRepo = g.get_repo("adityachidambaram/code-review-tester")
print(testRepo.full_name, '\n')

pr1 = testRepo.get_pull(1)
print("Title:", pr1.title)
print("Author:", pr1.user.login)
print("Files changed:")
for file in pr1.get_files():
    print(" -", file.filename)