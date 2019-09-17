from py_seranking import SERanking

TOKEN = "paste your SERanking token here"

seranking = SERanking(TOKEN)

sites = seranking.get_sites()

print(sites)
