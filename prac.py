import pyodbc
from datetime import datetime
# Global variables
connection = None
cursor = None
user_id = None

# Function to connect to the database
def connect_to_database():
    global connection, cursor
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-D89FSCV;DATABASE=Health_and_Fitness_Tracking_System;UID=sa;PWD=umair12'
        )
        cursor = connection.cursor()
        print("Successfully connected to the database!")
    except pyodbc.Error as ex:
        print("Failed to connect to the database.")
        print(f"Error: {ex}")

# Function to disconnect from the database
def disconnect_from_database():
    global connection, cursor
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Disconnected from the database.")

# View user id
def view_user_id():
    queryuser = "SELECT COUNT(UserID) AS TotalNumofUserID FROM Users"
    
    try:
        cursor.execute(queryuser)
        # Fetch the result (a single integer value)

        row = cursor.fetchone()
        if row:
            # Directly print the result as an integer (row is a tuple with one element)
            print(f"Total number of UserID: {row[0]}")
        else:
            print("No UserIDs found.")
    except pyodbc.Error as ex:
        print("Failed to retrieve the total number of UserIDs.")
        print(f"Error: {ex}")

# Add a new user
def add_user():
    global user_id
    user_id = int(input("Enter User ID: "))
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    height = float(input("Enter Height (in cm): "))
    weight = float(input("Enter Weight (in kg): "))
    goal = input("Enter Goal: ")

    query1 = "INSERT INTO Users (UserID,Name, Age, Gender, Height, Weight, Goal) VALUES (?, ?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(query1, (user_id,name, age, gender, height, weight, goal))
        connection.commit()
        print(f"User: {name} added successfully.")
    except pyodbc.Error as ex:
        print("Failed to add user.")
        print(f"Error: {ex}")

# Add a new goal
def add_goal():
    
    goal_type = input("Enter Goal Type: ")
    target_value = input("Enter Target Value (e.g: Lose 5 kg): ")
    start_date = input("Enter Start Date (YYYY-MM-DD): ")
    end_date = input("Enter End Date (YYYY-MM-DD): ")
    achieved_date = input("Enter Achieved Date (YYYY-MM-DD): ")

    query2 = "INSERT INTO Goal (UserID, GoalType, TargetValue, StartDate, EndDate, AchievedDate) VALUES (?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(query2, (user_id, goal_type, target_value, start_date, end_date, achieved_date))
        connection.commit()
        print("Goal added successfully.")
    except pyodbc.Error as ex:
        print("Failed to add goal.")
        print(f"Error: {ex}")

# View all goals
def view_goals():
    
    query3 = "SELECT GoalType, TargetValue, StartDate, EndDate, AchievedDate FROM Goal WHERE UserID = ?"

    try:
        cursor.execute(query3, (user_id,))
        rows = cursor.fetchall()
        if rows:
            print("\nGoals:")
            for row in rows:
                print(f"Goal Type: {row.GoalType}, Target Value: {row.TargetValue}, Start Date: {row.StartDate}, End Date: {row.EndDate}, Achieved Date: {row.AchievedDate}")
        else:
            print("No goals found for this user.")
    except pyodbc.Error as ex:
        print("Failed to retrieve goals.")
        print(f"Error: {ex}")


# Add a new workout
def add_workout():
    
    workout_type = input("Enter Workout Type: ")
    workout_date = input("Enter Workout Date (YYYY-MM-DD): ")
    workout_duration = int(input("Enter Duration (in minutes): "))
    calories_burned = float(input("Enter Calories Burned (kcal): "))

    query4 = "INSERT INTO Workout (UserID, WorkoutType, WorkoutDate, WorkoutDuration, CaloriesBurned) VALUES (?, ?, ?, ?, ?)"

    try:
        cursor.execute(query4, (user_id, workout_type,workout_date, workout_duration, calories_burned))
        connection.commit()
        print("Workout added successfully.")
    except pyodbc.Error as ex:
        print("Failed to add workout.")
        print(f"Error: {ex}")

# View workouts
def view_workouts():
    
    query5 = "SELECT WorkoutType, WorkoutDate, WorkoutDuration, CaloriesBurned FROM Workout WHERE UserID = ?"

    try:
        cursor.execute(query5, (user_id,))
        rows = cursor.fetchall()
        if rows:
            print("\nWorkouts:")
            for row in rows:
                print(f"Workout Type: {row.WorkoutType}, Workout Date: {row.WorkoutDate}, Workout Duration: {row.WorkoutDuration} mins, Calories Burned: {row.CaloriesBurned}")
        else:
            print("No workouts found for this user.")
    except pyodbc.Error as ex:
        print("Failed to retrieve workouts.")
        print(f"Error: {ex}")

# Add nutrition entry
def add_nutrition():
    
    nutrition_date = input("Enter Date (YYYY-MM-DD): ")
    food_item = input("Enter Food Item: ")
    calories = float(input("Enter Calories (kcal): "))
    protein = float(input("Enter Protein (g): "))
    fat = float(input("Enter Fat (g): "))
    carbohydrates = float(input("Enter Carbohydrates (g): "))

    query6 = "INSERT INTO Nutrition (UserID, NutritionDate, FoodItem, Calories, Protein, Fat, Carbohydrates) VALUES (?, ?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(query6, (user_id, nutrition_date, food_item, calories, protein, fat, carbohydrates))
        connection.commit()
        print("Nutrition entry added successfully.")
    except pyodbc.Error as ex:
        print("Failed to add nutrition entry.")
        print(f"Error: {ex}")

# View nutrition information
def view_nutrition():
    
    query7 = "SELECT NutritionDate, FoodItem, Calories, Protein, Fat, Carbohydrates FROM Nutrition WHERE UserID = ?"

    try:
        cursor.execute(query7, (user_id,))
        rows = cursor.fetchall()
        if rows:
            print("\nNutrition:")
            for row in rows:
                print(f"Nutrition Date: {row.NutritionDate}, Food Item: {row.FoodItem} Calories: {row.Calories}, Protein: {row.Protein}, Fat: {row.Fat}, Carbohydrates: {row.Carbohydrates}")
        else:
            print("No nutrition entries found for this user.")
    except pyodbc.Error as ex:
        print("Failed to retrieve nutrition information.")
        print(f"Error: {ex}")

#View Progress Informaton
def view_progress():
    user_id = int(input("Enter User ID to view progress: "))

    # SQL for creating the stored procedure if it doesn't exist
    create_procedure_query = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'GetUserProgress')
        EXEC('
            CREATE PROCEDURE GetUserProgress (@UserID INT)
            AS
                SELECT 
                    Users.Name, Users.Age, Users.Gender, Users.Height, Users.Weight, Users.Goal,
                    Workout.WorkoutType, Workout.WorkoutDate, Workout.WorkoutDuration, Workout.CaloriesBurned, 
                    Nutrition.NutritionDate, Nutrition.FoodItem, Nutrition.Calories AS NutritionCalories, 
                    Nutrition.Protein, Nutrition.Fat, Nutrition.Carbohydrates, 
                    Goal.GoalType, Goal.TargetValue, Goal.StartDate, Goal.EndDate, Goal.AchievedDate
                FROM Users 
                LEFT JOIN Workout ON Users.UserID = Workout.UserID
                LEFT JOIN Nutrition ON Users.UserID = Nutrition.UserID
                LEFT JOIN Goal ON Users.UserID = Goal.UserID
                WHERE Users.UserID = @UserID;
        ')
    """

    try:
        # Step 1: Create the procedure if it doesn't already exist
        cursor.execute(create_procedure_query)
        connection.commit()

        # Step 2: Call the stored procedure with the User ID as a parameter
        execquery = "EXEC GetUserProgress ?"
        cursor.execute(execquery, (user_id,))
        rows = cursor.fetchall()

        if rows:
            print(f"\nProgress for User ID {user_id}: ")
            current_goal = None

            for row in rows:
                print(f"\nUser: {row.Name}, (Age: {row.Age}, Gender: {row.Gender}, Height: {row.Height}, Weight: {row.Weight}, Goal: {row.Goal})")
                
                # Display goals information
                if row.GoalType is not None:
                    if current_goal != row.GoalType:
                        print(f"\nGoal Type: {row.GoalType}, (Target Value: {row.TargetValue}, Start Date: {row.StartDate}, End Date: {row.EndDate}, Achieved Date: {row.AchievedDate})")
                        current_goal = row.GoalType
                else:
                    print("\nNo active goals found.")

                # Display workout information
                if row.WorkoutType is not None:
                    print(f"\nWorkout Type: {row.WorkoutType}, Workout Date: {row.WorkoutDate}, Workout Duration: {row.WorkoutDuration} mins, Calories Burned: {row.CaloriesBurned} kcal")
                else:
                    print("\nNo workout information available.")

                # Display nutrition information
                if row.NutritionDate is not None:
                    print(f"\nNutrition Date: {row.NutritionDate}, Food Item: {row.FoodItem}, Calories: {row.NutritionCalories} kcal, Protein: {row.Protein}g, Fat: {row.Fat}g, Carbs: {row.Carbohydrates}g")
                else:
                    print("\nNo nutrition information available.")

        else:
            print("No data found for the user or no progress available.")

    except pyodbc.Error as ex:
        print("Failed to retrieve progress.")
        print(f"Error: {ex}")


# SELECT Query: Fetch high-calorie foods
def view_high_calorie_foods():
    query9 = "SELECT FoodItem, Calories FROM Nutrition WHERE Calories > 500;"
    try:
        cursor.execute(query9)
        rows = cursor.fetchall()
        if rows:
            print("\nHigh-Calorie Foods:")
            for row in rows:
                print(f"Food Item: {row.FoodItem}, Calories: {row.Calories}")
        else:
            print("No high-calorie foods found.")
    except pyodbc.Error as ex:
        print("Failed to fetch high-calorie foods.")
        print(f"Error: {ex}")

# SELECT Query with Date Range
def view_recent_workouts():
    query10 = """
    SELECT WorkoutType, WorkoutDate, WorkoutDuration, CaloriesBurned
    FROM Workout
    WHERE WorkoutDate BETWEEN '2024-01-01' AND GETDATE();
    """
    try:
        cursor.execute(query10)
        rows = cursor.fetchall()
        if rows:
            print("\nRecent Workouts:")
            for row in rows:
                print(f"Workout Type: {row.WorkoutType}, Date: {row.WorkoutDate}, Duration: {row.WorkoutDuration} mins, Calories: {row.CaloriesBurned}")
        else:
            print("No recent workouts found.")
    except pyodbc.Error as ex:
        print("Failed to fetch recent workouts.")
        print(f"Error: {ex}")

# Aggregate Functions: Average workout duration and total calories consumed
def view_aggregated_data():
    
    try:
        # Average workout duration
        askuserid1 = int(input("\nEnter UserID to find out your average Workout Duration in minutes: "))
        query11 = "SELECT AVG(WorkoutDuration) AS AvgDuration FROM Workout WHERE UserID = ?;"
        cursor.execute(query11, (askuserid1,))
        avg_duration = cursor.fetchone()
        print(f"\nAverage Workout Duration: {avg_duration[0]} minutes")
    

        # Total calories in the last week
        askuserid2 = int(input("\nEnter UserID to find out your total consumed calories in the last week: "))
        query12 = """
        SELECT SUM(Calories) AS TotalCalories
        FROM Nutrition
        WHERE UserID = ? AND NutritionDate > DATEADD(DAY, -7, GETDATE());
        """
        cursor.execute(query12, (askuserid2,))
        total_calories = cursor.fetchone()
        print(f"Total Calories Consumed in the Last Week: {total_calories[0]} kcal")
    except pyodbc.Error as ex:
        print("Failed to fetch aggregated data.")
        print(f"Error: {ex}")

# Additional JOIN: Workout and Goal
def view_goal_and_workout():
    askuserid3 = int(input("Enter UserID to find out your calories burned according to your goal type: "))

    query13 = """
    SELECT Goal.GoalType, SUM(Workout.CaloriesBurned) AS TotalCaloriesBurned
    FROM Goal
    INNER JOIN Workout ON Goal.UserID = Workout.UserID
    WHERE Goal.UserID = ?
    GROUP BY Goal.GoalType;
    """
    try:
        cursor.execute(query13, (askuserid3,))
        rows = cursor.fetchall()
        if rows:
            print("\nGoals and Workouts:")
            for row in rows:
                print(f"Goal Type: {row.GoalType}, Total Calories Burned: {row.TotalCaloriesBurned} kcal")
        else:
            print("No goals and workout data found.")
    except pyodbc.Error as ex:
        print("Failed to fetch goals and workouts.")
        print(f"Error: {ex}")

# Subqueries: Find users with highest calories burned in a single workout
def find_user_with_max_calories():
    query14 = """
    SELECT Name 
    FROM Users 
    WHERE UserID = (SELECT TOP 1 UserID FROM Workout ORDER BY CaloriesBurned DESC);
    """
    try:
        cursor.execute(query14)
        user = cursor.fetchone()
        if user:
            print(f"\nUser with Maximum Calories Burned: {user[0]}")
        else:
            print("No data found.")
    except pyodbc.Error as ex:
        print("Failed to fetch user with max calories burned.")
        print(f"Error: {ex}")

#View Single User Summary
def view_single_row_user_summary():
    askuserid4 = int(input("Enter UserID to view a detailed user summary: "))
    
    # SQL for dropping and creating the view
    drop_view_query = "IF OBJECT_ID('SingleUserSummary', 'V') IS NOT NULL DROP VIEW SingleUserSummary;"
    
    create_view_query = """
    CREATE VIEW SingleUserSummary AS
    SELECT 
        Users.UserID, 
        LTRIM(RTRIM(Users.Name)) AS TrimmedUserName,
        FORMAT(Goal.StartDate, 'MMM dd, yyyy') AS FormattedStartDate,
        COALESCE(SUM(Workout.WorkoutDuration), 0) AS TotalWorkoutMinutes,
        COALESCE(SUM(Nutrition.Calories), 0) AS TotalCaloriesConsumed,
        COALESCE(AVG(Workout.WorkoutDuration), 0) AS AvgWorkoutDuration
    FROM Users 
    LEFT JOIN Goal ON Users.UserID = Goal.UserID
    LEFT JOIN Workout ON Users.UserID = Workout.UserID
    LEFT JOIN Nutrition ON Users.UserID = Nutrition.UserID
    GROUP BY Users.UserID, Users.Name, Goal.StartDate;
    """
    
    # SQL to fetch data from the view
    query_view = """
    SELECT 
        UserID, 
        TrimmedUserName, 
        FormattedStartDate, 
        TotalWorkoutMinutes, 
        TotalCaloriesConsumed, 
        AvgWorkoutDuration
    FROM SingleUserSummary
    WHERE UserID = ?
    """
    
    try:
        # Step 1: Drop the view if it exists
        cursor.execute(drop_view_query)
        connection.commit()
        
        # Step 2: Create the view
        cursor.execute(create_view_query)
        connection.commit()
        
        # Step 3: Query the view for the specified UserID
        cursor.execute(query_view, (askuserid4,))
        row = cursor.fetchone()
        
        # Step 4: Display the result
        if row:
            print("\nUser Summary:")
            print(f"User ID: {row.UserID}")
            print(f"User Name: {row.TrimmedUserName}")
            print(f"Start Date: {row.FormattedStartDate}")
            print(f"Total Workout Time: {row.TotalWorkoutMinutes} minutes")
            print(f"Total Calories Consumed: {row.TotalCaloriesConsumed} kcal")
            print(f"Average Workout Duration: {row.AvgWorkoutDuration:.2f} minutes")
        else:
            print("No data found for the provided UserID.")
    
    except pyodbc.Error as ex:
        print("Failed to fetch or create user summary.")
        print(f"Error: {ex}")

#Update any User Details
def update_user_details():
    print(f"Your Registered User ID: {user_id}")
    print("What would you like to update?")
    print("1. User Details (Name, Age, Gender, Height, Weight, Goal)")
    print("2. Goal Details")
    print("3. Workout Details")
    print("4. Nutrition Details")
    
    choice = int(input("Enter your choice (1-4): "))
    
    try:
        if choice == 1:
            # Update User Details
            name = input("Enter new Name: ")
            age = int(input("Enter new Age: "))
            gender = input("Enter new Gender: ")
            height = float(input("Enter new Height (in cm): "))
            weight = float(input("Enter new Weight (in kg): "))
            goal = (input("Enter new Goal: "))
            
            update_user_query = """
                UPDATE Users
                SET Name = ?, Age = ?, Gender = ?, Height = ?, Weight = ?, Goal = ?
                WHERE UserID = ?
            """
            cursor.execute(update_user_query, (name, age, gender, height, weight, goal, user_id))
            connection.commit()
            print("\nUser details updated successfully.")
        
        elif choice == 2:
            # Update Goal Details
            goal_type = input("Enter new Goal Type (e.g., Weight Loss, Muscle Gain): ")
            target_value = input("Enter new Target Value (e.g., 70 kg, 10 kg Muscle): ")
            start_date = input("Enter new Start Date (YYYY-MM-DD): ")
            end_date = input("Enter new End Date (YYYY-MM-DD): ")
            achieved_date = input("Enter new End Date (YYYY-MM-DD): ")

            update_goal_query = """
                UPDATE Goal
                SET GoalType = ?, TargetValue = ?, StartDate = ?, EndDate = ?, AchievedDate = ?
                WHERE UserID = ?
            """
            cursor.execute(update_goal_query, (goal_type, target_value, start_date, end_date, achieved_date, user_id))
            connection.commit()
            print("\nGoal details updated successfully.")
        
        elif choice == 3:
            # Update Workout Details
            workout_type = input("Enter new Workout Type (e.g., Cardio, Strength): ")
            workout_date = input("Enter new Workout Date (YYYY-MM-DD): ")
            workout_duration = int(input("Enter new Workout Duration (in minutes): "))
            calories_burned = float(input("Enter new Calories Burned: "))

            update_workout_query = """
                UPDATE Workout
                SET WorkoutType = ?, WorkoutDate = ?, WorkoutDuration = ?, CaloriesBurned = ?
                WHERE UserID = ? 
            """
            cursor.execute(update_workout_query, (workout_type, workout_date, workout_duration, calories_burned, user_id))
            connection.commit()
            print("\nWorkout details updated successfully.")
        
        elif choice == 4:
            # Update Nutrition Details
            nutrition_date = input("Enter new Nutrition Date (YYYY-MM-DD): ")
            food_item = input("Enter new Food Item: ")
            calories = float(input("Enter new Calories: "))
            protein = float(input("Enter new Protein (g): "))
            fat = float(input("Enter new Fat (g): "))
            carbohydrates = float(input("Enter new Carbohydrates (g): "))

            update_nutrition_query = """
                UPDATE Nutrition
                SET NutritionDate = ?, FoodItem = ?, Calories = ?, Protein = ?, Fat = ?, Carbohydrates = ?
                WHERE UserID = ? 
            """
            cursor.execute(update_nutrition_query, (nutrition_date, food_item, calories, protein, fat, carbohydrates, user_id))
            connection.commit()
            print("\nNutrition details updated successfully.")
        
        else:
            print("\nInvalid choice. Please select a valid option.")
    
    except pyodbc.Error as ex:
        print("An error occurred while updating.")
        print(f"Error: {ex}")

#Delete a User 
def delete_user():
    print(f"Your Registered User ID: {user_id}")
    surity = int(input("Are you sure you want to delete your registration? 1. Yes 2. No: "))

    try:
        if surity == 1:
            # Step 1: Log deletion for Goal data with clearer separation
            log_goal_query = """
            INSERT INTO UserDeletionLog (UserID, DataType, DataDetails, DeletedBy)
            SELECT UserID, 'Goal', 
                   CONCAT('GoalType: ', GoalType, ' | TargetValue: ', TargetValue, ' | StartDate: ', StartDate, 
                          ' | EndDate: ', EndDate, ' | AchievedDate: ', AchievedDate), 'User'
            FROM Goal WHERE UserID = ?"""
            cursor.execute(log_goal_query, (user_id,))

            # Step 2: Log deletion for Workout data with clearer separation
            log_workout_query = """
            INSERT INTO UserDeletionLog (UserID, DataType, DataDetails, DeletedBy)
            SELECT UserID, 'Workout', 
                   CONCAT('WorkoutType: ', WorkoutType, ' | WorkoutDate: ', WorkoutDate, ' | WorkoutDuration: ', WorkoutDuration,
                          ' mins | CaloriesBurned: ', CaloriesBurned), 'User'
            FROM Workout WHERE UserID = ?"""
            cursor.execute(log_workout_query, (user_id,))

            # Step 3: Log deletion for Nutrition data with clearer separation
            log_nutrition_query = """
            INSERT INTO UserDeletionLog (UserID, DataType, DataDetails, DeletedBy)
            SELECT UserID, 'Nutrition', 
                   CONCAT('NutritionDate: ', NutritionDate, ' | FoodItem: ', FoodItem, ' | Calories: ', Calories, 
                          ' | Protein: ', Protein, 'g | Fat: ', Fat, 'g | Carbohydrates: ', Carbohydrates, 'g'), 'User'
            FROM Nutrition WHERE UserID = ?"""
            cursor.execute(log_nutrition_query, (user_id,))

            # Step 4: Now delete the actual data from Goal, Workout, Nutrition tables
            delete_goal_query = "DELETE FROM Goal WHERE UserID = ?"
            delete_workout_query = "DELETE FROM Workout WHERE UserID = ?"
            delete_nutrition_query = "DELETE FROM Nutrition WHERE UserID = ?"
            cursor.execute(delete_goal_query, (user_id,))
            cursor.execute(delete_workout_query, (user_id,))
            cursor.execute(delete_nutrition_query, (user_id,))

            # Step 5: Log deletion for the User account
            log_user_query = "INSERT INTO UserDeletionLog (UserID, DataType, DataDetails, DeletedBy) VALUES (?, 'User', 'Account Deleted', 'User')"
            cursor.execute(log_user_query, (user_id,))

            # Step 6: Finally, delete the user from the Users table
            delete_user_query = "DELETE FROM Users WHERE UserID = ?"
            cursor.execute(delete_user_query, (user_id,))

            # Commit all changes
            connection.commit()
            print(f"\nUser {user_id} and their related data deleted successfully.")
        
        elif surity == 2:
            print("\nNo deletion performed.")
        else:
            print("\nInvalid choice. Please select 1 or 2.")
    
    except pyodbc.Error as ex:
        print("An error occurred while deleting the user.")
        print(f"Error: {ex}")

# Main function
def main():
    connect_to_database()

    print("\n------------SMU Health and Fitness Tracking System------------")
    print("\nView Total Number of Registered User IDs (Mandatory to determine your next User ID)\n") 
    if connection:
        while True:
            print("\nSMU Health and Fitness Tracking System") 
            print("1. View Total Number of UserID (Compulsory)")  #COUNT function, Aggregate Function Concept
            print("2. Add User")  #Insert Concept
            print("3. Add Goal")  #Insert Concept
            print("4. View Goals")  #SELECT Concept
            print("5. Add Workout")   #Insert Concept
            print("6. View Workouts")  #SELECT Concept
            print("7. Add Nutrition")  #Insert Concept
            print("8. View Nutrition") #SELECT Concept
            print("9. View Progress")  #Left Join, Multiple row and Procedure Concept
            print("10. View High-Calorie Foods (Calories > 500)")  #SELECT Concept
            print("11. View Recent Workouts")  #SELECT Concept with date range (e.g: Between)
            print("12. View Aggregated Data")  #AVG function and SUM function, Aggregate Function Concept
            print("13. View Goal and Workout") #Inner Join, Multiple row and SUM function, Aggregate Function Concept
            print("14. Find User with Max Calories Burned") #Subquery Concept
            print("15. View Single User Data Summary")  #Left Join, Multiple row and View Concept 
            print("16. Update your registered information")  #Update Concept
            print("17. Permanently delete your registration")  #DELETE and Trigger Concept
            print("18. Exit")

            choice = int(input("Enter your choice: "))  

            if choice == 1:
                view_user_id()    
            elif choice == 2:
                add_user()
            elif choice == 3:
                add_goal()
            elif choice == 4:
                view_goals()
            elif choice == 5:
                add_workout()
            elif choice == 6:
                view_workouts()
            elif choice == 7:
                add_nutrition()
            elif choice == 8:
                view_nutrition()
            elif choice == 9:
                view_progress()
            elif choice == 10:
                view_high_calorie_foods()
            elif choice == 11:
                view_recent_workouts()
            elif choice == 12:
                view_aggregated_data()
            elif choice == 13:
                view_goal_and_workout()
            elif choice == 14:
                find_user_with_max_calories()
            elif choice == 15:
                view_single_row_user_summary()
            elif choice == 16:
                update_user_details()    
            elif choice == 17:
                delete_user()
            elif choice == 18:
                print("Thank You for using SMU Health and Fitness Tracking System. Have a great day!")
                break
            else:
                print("Invalid choice. Try again.")

        disconnect_from_database()

# Run the main function
if __name__ == "__main__":

    main()
