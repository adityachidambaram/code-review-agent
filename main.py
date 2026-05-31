from dotenv import load_dotenv
import github
from github import Github, Auth
import os
from google import genai

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
api_key = os.getenv("GEMINI_KEY")
SKIP_EXTENSIONS = ('.md', '.txt', '.json', '.lock', '.png', '.svg', '.jpg')

g = Github(auth=github.Auth.Token(token))
client = genai.Client(api_key=api_key)

testRepo = g.get_repo("adityachidambaram/code-review-tester")
print(testRepo.full_name, '\n')

def call_gemini_api(patch):
    full_response = ""
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents="You are a skilled code reviewer. Review the following code changes and respond in exactly this format:\n\n"
                 "## Code Review\n\n"
                 "**Status:** Approved / Request changes\n\n"
                 "### Bugs\n"
                 "- List any bugs, or 'None found'\n\n"
                 "### Security Issues\n"
                 "- List any security issues, or 'None found'\n\n"
                 "### Style & Readability\n"
                 "- List any style issues, or 'None found'\n\n"
                 "### Summary\n"
                 "One sentence summary of the review.\n\n"
                 "Here are the changes to review:\n" + patch
    )
    for chunk in response:
        full_response += chunk.text
    return full_response

pr1 = testRepo.get_pull(1)
print("Title:", pr1.title)
print("Author:", pr1.user.login)
print("Files changed:")
reviews = {}

for file in pr1.get_files():
    print(" -", file.filename)
    if file.filename.endswith(SKIP_EXTENSIONS):
        continue
    patch = file.patch
    if patch:
        review = call_gemini_api(patch)
        reviews[file.filename] = review
        pass

for filename, review in reviews.items():
    print(f"\n--- Review for {filename} ---")
    print(review)
    print("\nPosting review as comment on the PR...")
    pr1.create_issue_comment(review)
    print(review)