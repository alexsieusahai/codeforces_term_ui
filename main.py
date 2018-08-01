from codeforcesClient import CodeforcesClient
from cursesInterface import CursesInterface

if __name__ == "__main__":
    client = CodeforcesClient()
    ci = CursesInterface()
    #creds = ci.login()
    #client.login(creds['email'], creds['pw'])
    (problems, problem_stats) = client.get_problem_metadata()
    ci.select_problem_flow(problems)
