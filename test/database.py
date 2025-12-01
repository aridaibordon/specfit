from logic.database import SpecFitDatabase


database = SpecFitDatabase(db_path="/home/aridai/Data/database/omega2006")

print(database.get_info())
